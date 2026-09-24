import httpx
import html

#for clean up of description
from bs4 import BeautifulSoup
#import the db table
from jobrank.db import init_db, save_jobs, count_jobs

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

#initialize the db
init_db()

for company in COMPANIES:

    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"


    try: 
        # get the JSON from the URL wiht a 30 sec timer
        response = httpx.get(url, timeout=30)
        
        #throw an exception if it did not work
        response.raise_for_status()

        #get the list of jobs (each job is a dict with values "title" -> a job title)
        jobs = response.json()["jobs"]

        for job in jobs:
            #add the company value into the dictionary of the job
            job["company"] = company

            #clean the raw description
            description = clean_html(job["content"])

            #add it to the job
            job["description"] = description


        #count of jobs from that specific company
        print(f"{company} { len(jobs)}")

        #add it to the all jobs
        all_jobs.extend(jobs)

    #catch all errors
    except httpx.HTTPStatusError as e:
        print(f"Skipping {company}")

#print the total count
print(f"All jobs: {len(all_jobs)}")

#store the jobs into the database
save_jobs(all_jobs)

print(f"Jobs stored in the database: {count_jobs()}")



    

