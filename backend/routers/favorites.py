from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from core.database import get_db
from core.security import get_current_user

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)

class FavoriteRequest(BaseModel):
    query_name: str
    generated_sql: str

class FavoriteResponse(BaseModel):
    id: int
    query_name: str
    generated_sql: str

@router.post("/add")
async def add_favorite(
    payload: FavoriteRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    asha_id = current_user.get("asha_id")

    if not asha_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ASHA users can save favorites"
        )

    try:
        query = text("""
            INSERT INTO favorite_queries (asha_id, query_name, generated_sql, is_system)
            VALUES (:asha_id, :query_name, :generated_sql, FALSE)
            ON CONFLICT (asha_id, query_name) DO UPDATE SET generated_sql = :generated_sql
        """)

        await db.execute(query, {
            "asha_id": asha_id,
            "query_name": payload.query_name,
            "generated_sql": payload.generated_sql
        })

        await db.commit()

        return {
            "message": "Query added to favorites"
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add favorite: {str(e)}"
        )

@router.get("/list")
async def list_favorites(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    asha_id = current_user.get("asha_id")

    if not asha_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ASHA users can access favorites"
        )

    try:
        query = text("""
            SELECT id, query_name, generated_sql, created_at, is_system
            FROM favorite_queries
            WHERE (asha_id = :asha_id OR asha_id = 0)
            ORDER BY is_system DESC, created_at DESC
        """)

        result = await db.execute(query, {"asha_id": asha_id})
        favorites = [dict(row) for row in result.mappings().all()]

        return {
            "favorites": favorites
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch favorites: {str(e)}"
        )

@router.delete("/remove/{favorite_id}")
async def remove_favorite(
    favorite_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    asha_id = current_user.get("asha_id")

    if not asha_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ASHA users can remove favorites"
        )

    try:
        check_query = text("""
            SELECT is_system FROM favorite_queries
            WHERE id = :id AND asha_id = :asha_id
        """)

        result = await db.execute(check_query, {
            "id": favorite_id,
            "asha_id": asha_id
        })

        favorite = result.mappings().first()

        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found"
            )

        if favorite["is_system"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot delete system queries"
            )

        delete_query = text("""
            DELETE FROM favorite_queries
            WHERE id = :id AND asha_id = :asha_id
        """)

        await db.execute(delete_query, {
            "id": favorite_id,
            "asha_id": asha_id
        })

        await db.commit()

        return {
            "message": "Favorite removed"
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove favorite: {str(e)}"
        )
