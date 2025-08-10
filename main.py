import os
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from .worker.tasks import run_notebook_task
from .utils.db import init_db

API_KEY = os.getenv("API_KEY")
app = FastAPI(title="Notebook Runner MVP")

@app.on_event("startup")
def _startup():
    init_db()

def require_api_key(x_api_key: Optional[str] = Header(default=None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True

class RunRequest(BaseModel):
    git_url: str = Field(..., description="Git repo URL that contains the notebook.")
    git_ref: str = Field("main", description="Branch or tag.")
    notebook_path: str = Field(..., description="Path to .ipynb in the repo.")
    params: Dict[str, Any] = Field(default_factory=dict)
    send_to_slack: bool = True

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/runs", dependencies=[Depends(require_api_key)])
def trigger_run(req: RunRequest):
    task = run_notebook_task.delay(
        git_url=req.git_url,
        git_ref=req.git_ref,
        notebook_path=req.notebook_path,
        params=req.params,
        send_to_slack=req.send_to_slack,
    )
    return {"status": "queued", "task_id": task.id}
