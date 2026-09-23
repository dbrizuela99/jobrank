import httpx

# board variable that will be where it is pulling from 
BOARD = "stripe"
URL = f"https://boards-api.greenhouse.io/v1/boards/{BOARD}/jobs"


# get the JSON from the URL
response = httpx.get(URL)

#if error will let us know here
response.raise_for_status()

#get the list from jobs
jobs = response.json()["jobs"] 


print(f"{len(jobs)} jobs at {BOARD}")
for job in jobs[:10]:
    print(f"- {job['title']} ({job['location']['name']})")


