DROP TABLE IF EXISTS job_skills CASCADE;
DROP TABLE IF EXISTS skill_skill_types CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS skill_types CASCADE;
DROP TABLE IF EXISTS locations CASCADE;
DROP TABLE IF EXISTS companies CASCADE;

-----------------------------------------------------
-- Companies
-----------------------------------------------------

CREATE TABLE companies(

    company_id SERIAL PRIMARY KEY,

    company_name TEXT UNIQUE NOT NULL

);

-----------------------------------------------------
-- Locations
-----------------------------------------------------

CREATE TABLE locations(

    location_id SERIAL PRIMARY KEY,

    job_location TEXT,

    job_country TEXT,

    UNIQUE(job_location,job_country)

);

-----------------------------------------------------
-- Skills
-----------------------------------------------------

CREATE TABLE skills(

    skill_id SERIAL PRIMARY KEY,

    skill_name TEXT UNIQUE NOT NULL

);

-----------------------------------------------------
-- Skill Types
-----------------------------------------------------

CREATE TABLE skill_types(

    skill_type_id SERIAL PRIMARY KEY,

    skill_type_name TEXT UNIQUE NOT NULL

);

-----------------------------------------------------
-- Jobs
-----------------------------------------------------

CREATE TABLE jobs(

    job_id SERIAL PRIMARY KEY,

    raw_job_id BIGINT,

    company_id INTEGER REFERENCES companies(company_id),

    location_id INTEGER REFERENCES locations(location_id),

    job_title TEXT,

    job_title_short TEXT,

    job_via TEXT,

    job_schedule_type TEXT,

    search_location TEXT,

    job_posted_date TIMESTAMP,

    job_work_from_home BOOLEAN,

    job_no_degree_mention BOOLEAN,

    job_health_insurance BOOLEAN,

    salary_rate TEXT,

    salary_year_avg NUMERIC,

    salary_hour_avg NUMERIC

);

-----------------------------------------------------
-- Job Skills
-----------------------------------------------------

CREATE TABLE job_skills(

    job_id INTEGER REFERENCES jobs(job_id),

    skill_id INTEGER REFERENCES skills(skill_id),

    PRIMARY KEY(job_id,skill_id)

);

-----------------------------------------------------
-- Skill Skill Types
-----------------------------------------------------

CREATE TABLE skill_skill_types(

    skill_id INTEGER REFERENCES skills(skill_id),

    skill_type_id INTEGER REFERENCES skill_types(skill_type_id),

    PRIMARY KEY(skill_id,skill_type_id)

);