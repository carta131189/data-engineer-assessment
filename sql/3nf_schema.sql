DROP TABLE IF EXISTS job_type_skills CASCADE;
DROP TABLE IF EXISTS job_skills CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS locations CASCADE;
DROP TABLE IF EXISTS companies CASCADE;


CREATE TABLE companies (

    company_id SERIAL PRIMARY KEY,

    company_name TEXT NOT NULL UNIQUE

);


CREATE TABLE locations (

    location_id SERIAL PRIMARY KEY,

    job_location TEXT NOT NULL,

    job_country TEXT,

    UNIQUE(job_location, job_country)

);


CREATE TABLE skills (

    skill_id SERIAL PRIMARY KEY,

    skill_name TEXT NOT NULL UNIQUE

);


CREATE TABLE jobs (

    job_id SERIAL PRIMARY KEY,

    raw_job_id INTEGER NOT NULL UNIQUE,

    company_id INTEGER NOT NULL,

    location_id INTEGER NOT NULL,

    job_title TEXT,

    job_title_short TEXT,

    job_via TEXT,

    job_schedule_type TEXT,

    work_from_home BOOLEAN,

    search_location TEXT,

    posted_date TIMESTAMP,

    no_degree_mention BOOLEAN,

    health_insurance BOOLEAN,

    salary_rate TEXT,

    salary_year_avg NUMERIC(12,2),

    salary_hour_avg NUMERIC(12,2),

    CONSTRAINT fk_company
        FOREIGN KEY(company_id)
        REFERENCES companies(company_id),

    CONSTRAINT fk_location
        FOREIGN KEY(location_id)
        REFERENCES locations(location_id),

    CONSTRAINT fk_raw_job
        FOREIGN KEY(raw_job_id)
        REFERENCES raw_jobs(raw_job_id)

);


CREATE TABLE job_skills (

    job_id INTEGER NOT NULL,

    skill_id INTEGER NOT NULL,

    PRIMARY KEY(job_id, skill_id),

    CONSTRAINT fk_js_job
        FOREIGN KEY(job_id)
        REFERENCES jobs(job_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_js_skill
        FOREIGN KEY(skill_id)
        REFERENCES skills(skill_id)
        ON DELETE CASCADE

);


CREATE TABLE job_type_skills(

    job_id INTEGER  NOT NULL,

    skill_id INTEGER NOT NULL,

    PRIMARY KEY(job_id,skill_id),

    CONSTRAINT fk_jobtypeskills_job
        FOREIGN KEY(job_id)
        REFERENCES jobs(job_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_jobtypeskills_skill
        FOREIGN KEY(skill_id)
        REFERENCES skills(skill_id)

);

CREATE INDEX idx_jobs_company
ON jobs(company_id);

CREATE INDEX idx_jobs_location
ON jobs(location_id);

CREATE INDEX idx_jobs_posted_date
ON jobs(posted_date);

CREATE INDEX idx_jobskills_job
ON job_skills(job_id);

CREATE INDEX idx_jobskills_skill
ON job_skills(skill_id);

CREATE INDEX idx_jobtypeskills_job
ON job_type_skills(job_id);

CREATE INDEX idx_jobtypeskills_skill
ON job_type_skills(skill_id);

CREATE INDEX idx_jobs_raw_job
ON jobs(raw_job_id);