import httpx

# companies variable that will be where it is pulling from 
COMPANIES = ["stripe", "airbnb", "discord", "figma", "databricks", "cloudflare", "robinhood", "dropbox", "pinterest", "reddit", "lyft", "gitlab"]

#jobs list matchign with company
all_jobs = []

for company in COMPANIES:

    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"


    try: 
        # get the JSON from the URL
        response = httpx.get(url)
        
        #throw an exception if it did not work
        response.raise_for_status()

        #get the list of jobs (each a dict entry per job)
        jobs = response.json()["jobs"]

        for job in jobs:
            #add the company value into it
            job["company"] = company

        print(f"{company} { len(jobs)}")

        #add it to the all jobs
        all_jobs.extend(jobs)

    except httpx.HTTPStatusError:
        print(f"Skipping {company}")

#print the total count
print(f"All jobs: {len(all_jobs)}")

    

