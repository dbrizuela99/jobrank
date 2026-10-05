import httpx
import html
# to check what time did the database pull and update
from datetime import datetime, timezone

#for clean up of description
from bs4 import BeautifulSoup
#import the db table
from jobrank.db import init_db, save_jobs, count_jobs, mark_inactive

#function to clean the raw text
def clean_html(raw):
    #clean the text from the corrupted tags
    cleaned = html.unescape(raw)

    # remove the tags completely
    cleaned = BeautifulSoup(cleaned, "html.parser").get_text(" ")
    
    #return the cleaned text joined with only one space 
    return " ".join(cleaned.split())



# companies variable that will be where it is pulling from 
COMPANIES = ["stripe", "airbnb", "discord", "figma", "databricks", "cloudflare", "robinhood", "dropbox", "pinterest", "reddit", "lyft", "gitlab"]

#jobs list matchign with company
all_jobs = []

#list that carries the successfull companies
suc_companies = []

#initialize the db
init_db()

#get current run time
time = datetime.now(timezone.utc).isoformat()

for company in COMPANIES:

    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"


    try: 
        # get the JSON from the URL wiht a 30 sec timer
        response = httpx.get(url, timeout=30)
        
        #throw an exception if it did not work
        response.raise_for_status()

        #if it did get through add it to the successfull cache
        suc_companies.append(company)

        #get the list of jobs (each job is a dict with values "title" -> a job title)
        jobs = response.json()["jobs"]

        for job in jobs:
            #add the company value into the dictionary of the job
            job["company"] = company

            #clean the raw description
            description = clean_html(job["content"])

            #add it to the job
            job["description"] = description

            #add the current time it was found
            job["last_seen_at"] = time

            #add that it was recently seen
            job["is_active"] = 1



        #count of jobs from that specific company
        print(f"{company} { len(jobs)}")

        #add it to the all jobs
        all_jobs.extend(jobs)

    #catch all errors
    except httpx.HTTPError as e:
        print(f"Skipping {company} error {e}")

#print the total count
print(f"All jobs: {len(all_jobs)}")

all_jobs.pop()

#store the jobs into the database
save_jobs(all_jobs)

#check for any inactive jobs and remove/hide them  from the db
mark_inactive(suc_companies, time)

print(f"Jobs stored in the database: {count_jobs()}")



    

