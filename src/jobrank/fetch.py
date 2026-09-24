import httpx
import html
from bs4 import BeautifulSoup

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

for company in COMPANIES:

    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"


    try: 
        # get the JSON from the URL
        response = httpx.get(url)
        
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

    except httpx.HTTPStatusError:
        print(f"Skipping {company}")

#print the total count
print(f"All jobs: {len(all_jobs)}")

print(all_jobs[0]["description"])



    

