import sqlite3

#initialize the database function
def init_db():
    # connect to the database file
    conn = sqlite3.connect("jobs.db")
    #if table not created make it
    conn.execute("""CREATE TABLE IF NOT EXISTS jobs( 
    id INTEGER PRIMARY KEY,
    company TEXT,
    title TEXT, 
    location TEXT,
    url TEXT,
    description TEXT,
    updated_at TEXT) """)

    #save the changes
    conn.commit()
    #close the conncection
    conn.close()

#save the jobs
def save_jobs(jobs):

    conn = sqlite3.connect("jobs.db")

    for job in jobs:
        conn.execute(""" INSERT OR REPLACE INTO jobs (id, company, title, location, url, description, updated_at) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)""", (job["id"], 
                                                       job["company"], 
                                                       job["title"], 
                                                       job["location"]["name"], 
                                                       job["absolute_url"], 
                                                       job["description"], 
                                                       job["updated_at"]))
        
    conn.commit()
    conn.close()

#count the jobs
def count_jobs():
    conn = sqlite3.connect("jobs.db")

    #run a query to count all the jobs get the first row and only value (fetchone)
    count = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    
    conn.close()
    return count

