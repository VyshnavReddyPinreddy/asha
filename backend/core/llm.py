from groq import Groq
from core.config import settings

client = Groq(
    api_key=settings.GROQ_API_KEY
)

def ask_llm(prompt : str) -> str : 
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages=[
            {
                "role" : "system",
                "content" : "You are a health care assistant for ASHA workers."
            },
            {
                "role" : "user",
                "content" : prompt
            }
        ],
        temperature=0.3,
        max_tokens=1024
    )

    return response.choices[0].message.content or ""

_SCHEMA = """
TABLE: anm_worker
  anm_id SERIAL PK
  employee_code VARCHAR(20) UNIQUE
  first_name VARCHAR(100)
  last_name VARCHAR(100)
  phone_number VARCHAR(15)
  sub_center_name VARCHAR(150)
  date_of_joining DATE
  status VARCHAR(20)  -- 'ACTIVE','INACTIVE','TRANSFERRED','RETIRED'
 
TABLE: health_area
  area_id SERIAL PK
  area_name VARCHAR(150)
  area_type VARCHAR(20)  -- 'VILLAGE','WARD','COLONY','SLUM'
  mandal VARCHAR(100)
  district VARCHAR(100)
  anm_id INTEGER FK→anm_worker.anm_id
 
TABLE: asha_worker
  asha_id SERIAL PK
  employee_code VARCHAR(20) UNIQUE
  first_name VARCHAR(100)
  last_name VARCHAR(100)
  phone_number VARCHAR(15)
  date_of_joining DATE
  status VARCHAR(20)  -- 'ACTIVE','INACTIVE','TRANSFERRED','RETIRED'
  area_id INTEGER UNIQUE FK→health_area.area_id  -- each ASHA covers exactly one area
 
TABLE: family
  family_id SERIAL PK
  area_id INTEGER FK→health_area.area_id
  house_number VARCHAR(50)
  house_type VARCHAR(50)
  has_toilet BOOLEAN
  socio_economic_category VARCHAR(50)
 
TABLE: person
  person_id SERIAL PK
  first_name VARCHAR(100)
  last_name VARCHAR(100)
  date_of_birth DATE
  gender CHAR(1)  -- 'M','F','O'
  phone_number VARCHAR(15)
  blood_group VARCHAR(5)
  marital_status VARCHAR(20)  -- 'SINGLE','MARRIED','DIVORCED','WIDOWED'
  status VARCHAR(20)  -- 'ALIVE','DECEASED'
  family_id INTEGER FK→family.family_id
  father_id INTEGER FK→person.person_id
  mother_id INTEGER FK→person.person_id
 
TABLE: pregnancy
  pregnancy_id SERIAL PK
  mother_id INTEGER FK→person.person_id
  father_id INTEGER FK→person.person_id
  lmp_date DATE
  expected_delivery_date DATE
  pregnancy_status VARCHAR(20)  -- 'ONGOING','COMPLETED','ABORTED'
  risk_category VARCHAR(20)  -- 'NORMAL','HIGH_RISK'
 
TABLE: anc_visit
  visit_id SERIAL PK
  pregnancy_id INTEGER FK→pregnancy.pregnancy_id
  visit_date DATE
  weight_kg DECIMAL(5,2)
  blood_pressure VARCHAR(20)
  hemoglobin_level DECIMAL(4,2)
  remarks TEXT
 
TABLE: birth_record
  birth_id SERIAL PK
  pregnancy_id INTEGER FK→pregnancy.pregnancy_id
  child_id INTEGER UNIQUE FK→person.person_id
  birth_weight_kg DECIMAL(5,2)
  delivery_type VARCHAR(20)  -- 'NORMAL','C_SECTION'
  remarks TEXT
 
TABLE: disease
  disease_id SERIAL PK
  disease_name VARCHAR(100) UNIQUE
  disease_category VARCHAR(50)
 
TABLE: person_disease
  person_disease_id SERIAL PK
  person_id INTEGER FK→person.person_id
  disease_id INTEGER FK→disease.disease_id
  diagnosis_date DATE
  disease_status VARCHAR(20)  -- 'ACTIVE','RECOVERED','CONTROLLED'
  remarks TEXT
 
TABLE: vaccine
  vaccine_id SERIAL PK
  vaccine_name VARCHAR(100) UNIQUE
 
TABLE: vaccine_schedule
  schedule_id SERIAL PK
  vaccine_id INTEGER FK→vaccine.vaccine_id
  minimum_age_days INTEGER
  maximum_age_days INTEGER
  dose_number INTEGER
 
TABLE: vaccination_record
  vaccination_id SERIAL PK
  person_id INTEGER FK→person.person_id
  schedule_id INTEGER FK→vaccine_schedule.schedule_id
  vaccination_date DATE
 
TABLE: medicine
  medicine_id SERIAL PK
  medicine_name VARCHAR(100) UNIQUE
  medicine_type VARCHAR(50)
 
TABLE: medicine_distribution
  distribution_id SERIAL PK
  person_id INTEGER FK→person.person_id
  medicine_id INTEGER FK→medicine.medicine_id
  quantity INTEGER
  distribution_date DATE
 
TABLE: death_record
  death_id SERIAL PK
  person_id INTEGER UNIQUE FK→person.person_id
  date_of_death DATE
  cause_of_death TEXT
 
TABLE: user_account
  user_id SERIAL PK
  username VARCHAR(100) UNIQUE
  role VARCHAR(20)  -- 'ASHA','ANM','ADMIN'
  asha_id INTEGER FK→asha_worker.asha_id
  anm_id INTEGER FK→anm_worker.anm_id
  email VARCHAR(255) UNIQUE
  -- NOTE: password_hash, reset_otp, otp_expiry must NEVER appear in SELECT output
"""

_SYSTEM_PROMPT = """You are a PostgreSQL SQL generator for the ASHA Healthcare System.
 
## YOUR ONLY JOB
Convert the user's natural-language question into a single, valid PostgreSQL SELECT statement.
 
## DATABASE SCHEMA
{schema}
 
## STRICT RULES — NEVER VIOLATE THESE
 
1. OUTPUT FORMAT
   - Return ONLY the raw SQL query. No markdown, no backticks, no explanation, no preamble.
   - The output must start with SELECT and end with a semicolon.
   - One query only. No multiple statements.
 
2. READ-ONLY
   - Only SELECT statements are allowed.
   - Never generate INSERT, UPDATE, DELETE, DROP, TRUNCATE, ALTER, CREATE, GRANT, or any other DDL/DML.
   - Never use CTEs (WITH) that contain DML.
 
3. AREA SCOPING — CRITICAL
   - The querying ASHA has area_id = {area_id}.
   - ALL queries that touch person, family, pregnancy, birth_record, death_record,
     anc_visit, person_disease, vaccination_record, medicine_distribution
     MUST filter by the ASHA's area.
   - The join chain for area scoping is:
       person → family → (family.area_id = {area_id})
     OR for pregnancy:
       pregnancy → person (mother) → family → (family.area_id = {area_id})
   - Never return data from other ASHA areas under any circumstance.
   - If the question cannot be answered without crossing area boundaries, return data
     only for area_id = {area_id}.
 
4. SENSITIVE COLUMNS — NEVER SELECT THESE
   - user_account.password_hash
   - user_account.reset_otp
   - user_account.otp_expiry
 
5. SCHEMA BOUNDARIES
   - Only reference tables and columns that exist in the schema above.
   - Do not invent columns or tables.
   - If the question references something not in the schema, generate the closest valid query
     that answers the intent using available columns.
 
6. AGGREGATIONS & SAFETY
   - Use LIMIT 200 by default on non-aggregated queries to prevent runaway results.
   - Use proper JOINs; never use implicit cross joins.
   - Cast types explicitly where needed (e.g. EXTRACT, DATE_PART).
 
## EXAMPLES
 
User: "Show me all pregnant women in my area"
SQL: SELECT p.person_id, p.first_name, p.last_name, p.phone_number,
            pr.expected_delivery_date, pr.risk_category, pr.pregnancy_status
     FROM person p
     JOIN family f ON p.family_id = f.family_id
     JOIN pregnancy pr ON pr.mother_id = p.person_id
     WHERE f.area_id = {area_id}
       AND pr.pregnancy_status = 'ONGOING'
     LIMIT 200;
 
User: "How many children under 5 are unvaccinated?"
SQL: SELECT COUNT(DISTINCT p.person_id) AS unvaccinated_children
     FROM person p
     JOIN family f ON p.family_id = f.family_id
     WHERE f.area_id = {area_id}
       AND p.status = 'ALIVE'
       AND AGE(p.date_of_birth) < INTERVAL '5 years'
       AND p.person_id NOT IN (
           SELECT DISTINCT person_id FROM vaccination_record
       );
 
User: "List high-risk pregnancies"
SQL: SELECT p.first_name, p.last_name, p.phone_number,
            pr.lmp_date, pr.expected_delivery_date
     FROM pregnancy pr
     JOIN person p ON pr.mother_id = p.person_id
     JOIN family f ON p.family_id = f.family_id
     WHERE f.area_id = {area_id}
       AND pr.risk_category = 'HIGH_RISK'
       AND pr.pregnancy_status = 'ONGOING'
     LIMIT 200;
"""

def generate_sql(natural_language_query : str, area_id : int | None) -> str : 

    if area_id is not None : 
        system = _SYSTEM_PROMPT.format(schema=_SCHEMA,area_id=area_id)
    else : 
        system = _SYSTEM_PROMPT.format(schema=_SCHEMA, area_id="<ALL AREAS — no filter needed>")
        system = system.replace(
            "3. AREA SCOPING — CRITICAL",
            "3. AREA SCOPING — NOT APPLICABLE (ANM/ADMIN role — access all areas)",
        )
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": natural_language_query},
        ],
        temperature=0.0,   
        max_tokens=1024,
    )

    return (response.choices[0].message.content or "").strip()

def transcribe_audio(audio_bytes:bytes,filename:str)->str:
    import io 

    transcription = client.audio.transcriptions.create(
        model = "whisper-large-v3",
        file = (filename,io.BytesIO(audio_bytes)),
        response_format="text",
        temperature=0.0,
    )

    raw_text = transcription.strip() if isinstance(transcription,str) else transcription.text.strip()

    if not raw_text : 
        return ""
    
    translation_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a translator. "
                    "Translate the following text to English. "
                    "If it is already in English, return it exactly as-is. "
                    "Output only the translated text, nothing else."
                ),
            },
            {"role": "user", "content": raw_text},
        ],
        temperature=0.0,
        max_tokens=1024,
    )

    return (translation_response.choices[0].message.content or "").strip()
