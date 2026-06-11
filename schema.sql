-- ===========================================================================
-- DATABASE SCHEMA: asha_healthcare_system (3NF Optimized)
-- TARGET: PostgreSQL Engine
-- ACCESS: Read-Only for ASHA users, Full Maintainer Access for ANM users
-- ===========================================================================

-- 1. ANM Worker Table
CREATE TABLE anm_worker (
    anm_id SERIAL PRIMARY KEY,
    employee_code VARCHAR(20) UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    phone_number VARCHAR(15) UNIQUE,
    sub_center_name VARCHAR(150),
    date_of_joining DATE,
    status VARCHAR(20) CHECK (status IN ('ACTIVE', 'INACTIVE', 'TRANSFERRED', 'RETIRED'))
);

-- 2. Health Area Table
CREATE TABLE health_area (
    area_id SERIAL PRIMARY KEY,
    area_name VARCHAR(150) NOT NULL,
    area_type VARCHAR(20) CHECK (area_type IN ('VILLAGE', 'WARD', 'COLONY', 'SLUM')),
    mandal VARCHAR(100),
    district VARCHAR(100),
    anm_id INTEGER REFERENCES anm_worker(anm_id) ON DELETE SET NULL
);

-- 3. ASHA Worker Table
CREATE TABLE asha_worker (
    asha_id SERIAL PRIMARY KEY,
    employee_code VARCHAR(20) UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    phone_number VARCHAR(15) UNIQUE,
    date_of_joining DATE,
    status VARCHAR(20) CHECK (status IN ('ACTIVE', 'INACTIVE', 'TRANSFERRED', 'RETIRED')),
    area_id INTEGER UNIQUE REFERENCES health_area(area_id) ON DELETE SET NULL
);

-- 4. Family Table
CREATE TABLE family (
    family_id SERIAL PRIMARY KEY,
    area_id INTEGER REFERENCES health_area(area_id) ON DELETE SET NULL,
    house_number VARCHAR(50),
    house_type VARCHAR(50),
    has_toilet BOOLEAN,
    socio_economic_category VARCHAR(50)
);

-- 5. Person Table (With Demographic Optimizations)
CREATE TABLE person (
    person_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    date_of_birth DATE NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F', 'O')),
    phone_number VARCHAR(15),
    blood_group VARCHAR(5),
    marital_status VARCHAR(20) CHECK (marital_status IN ('SINGLE', 'MARRIED', 'DIVORCED', 'WIDOWED')),
    status VARCHAR(20) DEFAULT 'ALIVE' CHECK (status IN ('ALIVE', 'DECEASED')),
    family_id INTEGER REFERENCES family(family_id) ON DELETE SET NULL,
    father_id INTEGER REFERENCES person(person_id) ON DELETE SET NULL,
    mother_id INTEGER REFERENCES person(person_id) ON DELETE SET NULL
);

-- 6. Pregnancy Table
CREATE TABLE pregnancy (
    pregnancy_id SERIAL PRIMARY KEY,
    mother_id INTEGER REFERENCES person(person_id) ON DELETE CASCADE,
    father_id INTEGER REFERENCES person(person_id) ON DELETE SET NULL,
    lmp_date DATE,
    expected_delivery_date DATE,
    pregnancy_status VARCHAR(20) CHECK (pregnancy_status IN ('ONGOING', 'COMPLETED', 'ABORTED')),
    risk_category VARCHAR(20) CHECK (risk_category IN ('NORMAL', 'HIGH_RISK'))
);

-- 7. ANC Visit Table
CREATE TABLE anc_visit (
    visit_id SERIAL PRIMARY KEY,
    pregnancy_id INTEGER REFERENCES pregnancy(pregnancy_id) ON DELETE CASCADE,
    visit_date DATE,
    weight_kg DECIMAL(5,2),
    blood_pressure VARCHAR(20),
    hemoglobin_level DECIMAL(4,2),
    remarks TEXT
);

-- 8. Birth Record Table (With Mismatch Optimization)
CREATE TABLE birth_record (
    birth_id SERIAL PRIMARY KEY,
    pregnancy_id INTEGER REFERENCES pregnancy(pregnancy_id) ON DELETE SET NULL,
    child_id INTEGER UNIQUE REFERENCES person(person_id) ON DELETE CASCADE,
    birth_weight_kg DECIMAL(5,2),
    delivery_type VARCHAR(20) CHECK (delivery_type IN ('NORMAL', 'C_SECTION')),
    remarks TEXT
);

-- 9. Disease Table
CREATE TABLE disease (
    disease_id SERIAL PRIMARY KEY,
    disease_name VARCHAR(100) UNIQUE,
    disease_category VARCHAR(50)
);

-- 10. Person Disease Mapping Table
CREATE TABLE person_disease (
    person_disease_id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES person(person_id) ON DELETE CASCADE,
    disease_id INTEGER REFERENCES disease(disease_id) ON DELETE CASCADE,
    diagnosis_date DATE,
    disease_status VARCHAR(20) CHECK (disease_status IN ('ACTIVE', 'RECOVERED', 'CONTROLLED')),
    remarks TEXT,
    CONSTRAINT unique_person_disease UNIQUE (person_id, disease_id)
);

-- 11. Vaccine Table
CREATE TABLE vaccine (
    vaccine_id SERIAL PRIMARY KEY,
    vaccine_name VARCHAR(100) UNIQUE
);

-- 12. Vaccine Schedule Table
CREATE TABLE vaccine_schedule (
    schedule_id SERIAL PRIMARY KEY,
    vaccine_id INTEGER REFERENCES vaccine(vaccine_id) ON DELETE CASCADE,
    minimum_age_days INTEGER,
    maximum_age_days INTEGER,
    dose_number INTEGER
);

-- 13. Vaccination Record Table
CREATE TABLE vaccination_record (
    vaccination_id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES person(person_id) ON DELETE CASCADE,
    schedule_id INTEGER REFERENCES vaccine_schedule(schedule_id) ON DELETE CASCADE,
    vaccination_date DATE,
    CONSTRAINT unique_person_schedule UNIQUE (person_id, schedule_id)
);

-- 14. Medicine Table
CREATE TABLE medicine (
    medicine_id SERIAL PRIMARY KEY,
    medicine_name VARCHAR(100) UNIQUE,
    medicine_type VARCHAR(50)
);

-- 15. Medicine Distribution Table
CREATE TABLE medicine_distribution (
    distribution_id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES person(person_id) ON DELETE CASCADE,
    medicine_id INTEGER REFERENCES medicine(medicine_id) ON DELETE CASCADE,
    quantity INTEGER,
    distribution_date DATE
);

-- 16. Death Record Table
CREATE TABLE death_record (
    death_id SERIAL PRIMARY KEY,
    person_id INTEGER UNIQUE REFERENCES person(person_id) ON DELETE CASCADE,
    date_of_death DATE,
    cause_of_death TEXT
);

-- 17. User Account Table
CREATE TABLE user_account (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    password_hash TEXT,
    role VARCHAR(20) CHECK (role IN ('ASHA', 'ANM', 'ADMIN')),
    asha_id INTEGER REFERENCES asha_worker(asha_id) ON DELETE SET NULL,
    anm_id INTEGER REFERENCES anm_worker(anm_id) ON DELETE SET NULL,
    email VARCHAR(255) UNIQUE,
    reset_otp VARCHAR(6),
    otp_expiry TIMESTAMPTZ
);

-- 18. Favorite Queries Table
CREATE TABLE IF NOT EXISTS favorite_queries (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    asha_id INT NOT NULL,
    query_name VARCHAR(255) NOT NULL,
    generated_sql TEXT NOT NULL,
    is_system BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_query UNIQUE (asha_id, query_name)
);

-- Insert 5 system queries (asha_id = 0 reserved for system)
INSERT INTO favorite_queries (query_name, generated_sql, is_system, asha_id) VALUES 
('Pregnant women in my area', 'SELECT p.person_id, p.first_name, p.last_name, p.phone_number, pr.lmp_date, pr.expected_delivery_date, pr.risk_category FROM pregnancy pr JOIN person p ON pr.mother_id = p.person_id JOIN family f ON p.family_id = f.family_id WHERE f.area_id = {area_id} AND pr.pregnancy_status = ''ONGOING'';', TRUE, 0), 
('Vaccination pending - Children', 'SELECT p.person_id, p.first_name, p.last_name, p.date_of_birth FROM person p JOIN family f ON p.family_id = f.family_id WHERE f.area_id = {area_id} AND p.status = ''ALIVE'' AND EXTRACT(YEAR FROM AGE(CURRENT_DATE, p.date_of_birth)) < 5 AND p.person_id NOT IN (SELECT DISTINCT person_id FROM vaccination_record);', TRUE, 0), 
('High-risk pregnancies', 'SELECT p.first_name, p.last_name, p.phone_number, pr.lmp_date, pr.expected_delivery_date, pr.risk_category FROM pregnancy pr JOIN person p ON pr.mother_id = p.person_id JOIN family f ON p.family_id = f.family_id WHERE f.area_id = {area_id} AND pr.risk_category = ''HIGH_RISK'' AND pr.pregnancy_status = ''ONGOING'';', TRUE, 0), 
('Recent births (last 30 days)', 'SELECT p.person_id, p.first_name, p.last_name, br.birth_weight_kg, br.delivery_type, br.birth_id FROM birth_record br JOIN person p ON br.child_id = p.person_id JOIN family f ON p.family_id = f.family_id WHERE f.area_id = {area_id} AND br.birth_id IN (SELECT birth_id FROM birth_record WHERE CURRENT_DATE - INTERVAL ''30 days'' <= CURRENT_DATE);', TRUE, 0), 
('Children under 5 years', 'SELECT p.person_id, p.first_name, p.last_name, p.date_of_birth, p.gender FROM person p JOIN family f ON p.family_id = f.family_id WHERE f.area_id = {area_id} AND p.status = ''ALIVE'' AND EXTRACT(YEAR FROM AGE(CURRENT_DATE, p.date_of_birth)) < 5;', TRUE, 0);