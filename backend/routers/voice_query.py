import re
import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.llm import generate_sql, transcribe_audio
from core.database import get_db
from core.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["Voice Query"],
)


_FORBIDDEN_PATTERN = re.compile(
    r"^\s*(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|REPLACE|GRANT|REVOKE"
    r"|MERGE|CALL|EXEC|EXECUTE|COPY|VACUUM|ANALYZE|COMMENT|LOCK)\b",
    re.IGNORECASE | re.MULTILINE,
)

_INLINE_MUTATION_PATTERN = re.compile(
    r"\b(INSERT\s+INTO|UPDATE\s+\w|DELETE\s+FROM|DROP\s+TABLE|DROP\s+DATABASE"
    r"|TRUNCATE\s+TABLE|ALTER\s+TABLE|CREATE\s+TABLE|GRANT\s+|REVOKE\s+)\b",
    re.IGNORECASE,
)

_SENSITIVE_COLUMNS = re.compile(
    r"\b(password_hash|reset_otp|otp_expiry)\b",
    re.IGNORECASE,
)


def _is_safe_sql(sql: str) -> tuple[bool, str]:
    sql_stripped = sql.strip()

    if not re.match(r"^\s*SELECT\b", sql_stripped, re.IGNORECASE):
        return False, "Only SELECT queries are allowed."

    if _FORBIDDEN_PATTERN.search(sql_stripped):
        return False, "Query contains forbidden operation."

    if _INLINE_MUTATION_PATTERN.search(sql_stripped):
        return False, "Query contains a forbidden data-modification statement."

    inner = sql_stripped.rstrip(";")
    if ";" in inner:
        return False, "Multiple statements are not allowed."

    if _SENSITIVE_COLUMNS.search(sql_stripped):
        return False, "Query attempts to access restricted columns."

    return True, ""



_ALLOWED_CONTENT_TYPES = {
    "audio/mpeg",        # .mp3
    "audio/mp3",
    "audio/wav",         # .wav
    "audio/x-wav",
    "audio/ogg",         # .ogg
    "audio/webm",        # .webm
    "audio/flac",        # .flac
    "audio/x-flac",
    "audio/mp4",         # .m4a
    "audio/x-m4a",
}

_MAX_AUDIO_BYTES = 25 * 1024 * 1024  # Groq's 25 MB limit



class VoiceQueryResponse(BaseModel):
    transcribed_text: str       
    generated_sql: str
    row_count: int
    results: list[dict]



@router.post("/voice-query", response_model=VoiceQueryResponse)
async def voice_query(
    audio: UploadFile = File(..., description="Audio file in Telugu, Hindi, or English"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Pipeline:
      audio file  →  Groq Whisper (translate → English)  →  generate_sql()  →  execute  →  results
    """

    content_type = (audio.content_type or "").lower()
    if content_type not in _ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported audio format: {content_type}. "
                   f"Accepted: mp3, wav, ogg, webm, flac, m4a",
        )

    audio_bytes = await audio.read()

    if len(audio_bytes) > _MAX_AUDIO_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Audio file exceeds 25 MB limit.",
        )

    if len(audio_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty audio file.",
        )

    role: str = current_user.get("role", "")
    asha_id: int | None = current_user.get("asha_id")
    area_id: int | None = None

    if role == "ASHA":
        if not asha_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ASHA account has no linked asha_id.",
            )

        result = await db.execute(
            text("SELECT area_id FROM asha_worker WHERE asha_id = :asha_id"),
            {"asha_id": asha_id},
        )
        row = result.mappings().first()

        if not row or not row["area_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ASHA worker has no assigned health area.",
            )

        area_id = row["area_id"]

    logger.info(
        "Voice query from user_id=%s role=%s | file=%s size=%d bytes",
        current_user.get("user_id"),
        role,
        audio.filename,
        len(audio_bytes),
    )

    try:
        english_text = transcribe_audio(audio_bytes, audio.filename or "audio.mp3")
    except Exception as e:
        logger.error("Whisper transcription failed: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Audio transcription failed : {str(e)}",
        )

    if not english_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Transcription returned empty text. Speak clearly and try again.",
        )

    logger.info("Transcribed text: %s", english_text)

    try:
        generated_sql = generate_sql(
            natural_language_query=english_text,
            area_id=area_id,
        )
    except Exception as e:
        logger.error("SQL generation failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="SQL generation failed. Please try rephrasing your question.",
        )

    logger.info("Generated SQL: %s", generated_sql)

    is_safe, reason = _is_safe_sql(generated_sql)
    if not is_safe:
        logger.warning(
            "Unsafe SQL blocked for user_id=%s: %s | reason: %s",
            current_user.get("user_id"),
            generated_sql,
            reason,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Query blocked: {reason}",
        )

    if role == "ASHA" and area_id is not None:
        if str(area_id) not in generated_sql:
            logger.error(
                "SQL missing area scope for asha_id=%s. SQL: %s",
                asha_id,
                generated_sql,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not generate a properly scoped query for your area. "
                       "Please rephrase your question.",
            )

    try:
        result = await db.execute(text(generated_sql))
        rows = result.mappings().all()
        results = [dict(row) for row in rows]
    except Exception as e:
        logger.error("SQL execution error: %s | SQL: %s", e, generated_sql)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Query execution failed: {str(e)}",
        )

    return VoiceQueryResponse(
        transcribed_text=english_text,
        generated_sql=generated_sql,
        row_count=len(results),
        results=results,
    )