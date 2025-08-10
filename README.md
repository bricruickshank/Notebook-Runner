# Notebook Runner (MVP)
Zero-touch scheduled notebook execution with HTML + CSV artifacts and Slack notifications.

## Deploy on Render (no local needed)
1) Create a new GitHub repo and push this folder.
2) In Render: New → Blueprint → select your repo. Render reads `render.yaml` and creates:
   - Web Service (API) from `Dockerfile.api`
   - Worker (Celery) from `Dockerfile.worker`
3) Set environment variables in both services:
   - API_KEY, REDIS_URL (Upstash), optional: S3_* , SLACK_WEBHOOK_URL, DATABASE_URL (Neon)
4) Hit the API `/health` then POST `/runs` with your headers/body.

## CSV export convention
Use:
```python
from IPython.display import display
display({'text/csv': df.to_csv(index=False)}, metadata={'name': 'my_export'}, raw=True)
```
Reports will include an HTML file and any CSVs you emit like this.
