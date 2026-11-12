#small script to load resumes
from jobrank.db import init_db, add_resume

init_db()
add_resume("diego", "data/resume.txt")