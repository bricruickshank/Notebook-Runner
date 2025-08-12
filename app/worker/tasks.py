import os, tempfile, subprocess, uuid
from celery import Celery
from ..utils.store import ArtifactStore
from ..utils.slack import post_slack
from ..utils.nbexec import execute_notebook_html_csv

REDIS_URL = os.getenv("REDIS_URL")
celery_app = Celery("notebook_runner", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task(bind=True)
def run_notebook_task(self, git_url: str, git_ref: str, notebook_path: str, params: dict, send_to_slack: bool = True):
    run_id = str(uuid.uuid4())
    workdir = tempfile.mkdtemp(prefix="nb-run-")
    repo_dir = os.path.join(workdir, "repo")
    subprocess.run(["git", "clone", "--depth", "1", "--branch", git_ref, git_url, repo_dir], check=True)
    html_bytes, csv_artifacts = execute_notebook_html_csv(
        nb_path=os.path.join(repo_dir, notebook_path),
        params=params
    )
    store = ArtifactStore()
    html_uri = store.put_bytes(f"runs/{run_id}/report.html", html_bytes)
    csv_uris = [store.put_bytes(f"runs/{run_id}/{name}.csv", data) for name, data in csv_artifacts.items()]
    if send_to_slack:
        lines = [f"✅ Report ready: <{html_uri}|Open HTML>"] + [f"• CSV: <{u}|{u.split('/')[-1]}>" for u in csv_uris]
        post_slack("\n".join(lines))
    return {"run_id": run_id, "html": html_uri, "csvs": csv_uris}
