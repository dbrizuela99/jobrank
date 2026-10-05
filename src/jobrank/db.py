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
    updated_at TEXT,
    last_seen_at TEXT,
    is_active INTEGER) """)

    #save the changes
    conn.commit()
    #close the conncection
    conn.close()

#save the jobs
def save_jobs(jobs):

    conn = sqlite3.connect("jobs.db")

    for job in jobs:
        conn.execute(""" INSERT OR REPLACE INTO jobs (id, company, title, location, url, description, updated_at, last_seen_at, is_active) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (job["id"], 
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
    conn = sqlite3.connect("jobs.db")

    #run a query to count all the jobs that are active get the first row and only value (fetchone)
    count = conn.execute(""" SELECT COUNT(*) FROM jobs 
                             WHERE is_active = 1""").fetchone()[0]
    
    conn.close()
    return count

#mark inactive jobs to hide from the query
def mark_inactive(companies, time):
    conn = sqlite3.connect("jobs.db")

    #loop for every company
    for company in companies:
        conn.execute("""UPDATE jobs SET is_active = 0 
                        WHERE company = ? 
                        AND last_seen_at < ?""", (company,time))
        
    #commit the chnages and close the connection
    conn.commit()
    conn.close()

