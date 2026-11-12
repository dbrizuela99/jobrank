import sqlite3


#since using foreign keys need to always enable foreing keys, so a helper method that connects and enables everytime
def get_connection():
    conn = sqlite3.connect("jobs.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#initialize the database function
def init_db():
    # connect to the database file
    conn = get_connection()
    #if table not created make it
    conn.execute("""CREATE TABLE IF NOT EXISTS jobs( 
    id INTEGER PRIMARY KEY,
    company TEXT,
    title TEXT, 
    location TEXT,
    url TEXT,
    description TEXT,
    updated_at TEXT,
    last_seen_at TEXT,
    is_active INTEGER) """)

    #table for users resumes
    conn.execute("""CREATE TABLE IF NOT EXISTS resumes(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    content TEXT,
    created_at TEXT)""") 

     #table for jobs labeled in terms with a resume (training data / eval)
    conn.execute("""CREATE TABLE IF NOT EXISTS labels(
    resume_id INTEGER,
    job_id INTEGER,
    label INTEGER,
    labeled_at TEXT,
    CHECK (label IN (0, 1, 2)),
    FOREIGN KEY (resume_id) REFERENCES resumes(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    PRIMARY KEY (resume_id, job_id))""") 

    #save the changes
    conn.commit()
    #close the conncection
    conn.close()

#save the jobs
def save_jobs(jobs):

    conn = get_connection()

    for job in jobs:
        #save the job by inserting it if it already exist then just replace the value using ON CONFLICT so it does nto delete it 
        conn.execute(""" INSERT INTO jobs (id, company, title, location, url, description, updated_at, last_seen_at, is_active) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                     ON  CONFLICT(id) DO UPDATE SET
                        company = excluded.company,
                        title = excluded.title,
                        location = excluded.location,
                        url = excluded.url,
                        description = excluded.description,
                        updated_at = excluded.updated_at,
                        last_seen_at = excluded.last_seen_at,
                        is_active = excluded.is_active""", (job["id"], 
                                                       job["company"], 
                                                       job["title"], 
                                                       job["location"]["name"], 
                                                       job["absolute_url"], 
                                                       job["description"], 
                                                       job["updated_at"],
                                                       job["last_seen_at"],
                                                       job["is_active"]))
        
    conn.commit()
    conn.close()

#count the jobs
def count_jobs():
    conn = get_connection()

    #run a query to count all the jobs that are active get the first row and only value (fetchone)
    count = conn.execute(""" SELECT COUNT(*) FROM jobs 
                             WHERE is_active = 0""").fetchone()[0]
    
    conn.close()
    return count

#mark inactive jobs to hide from the query
def mark_inactive(companies, time):
    conn = get_connection()

    #loop for every company
    for company in companies:
        conn.execute("""UPDATE jobs SET is_active = 1 
                        WHERE company = ? 
                        AND last_seen_at < ?""", (company,time))
        
    #commit the chnages and close the connection
    conn.commit()
    conn.close()

