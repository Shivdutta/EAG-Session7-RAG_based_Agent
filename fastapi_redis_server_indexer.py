from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis import Redis
from rq import Queue
from redis_jobs import run_sync_process_documents_job, run_sync_process_html_job
from rq.job import Job

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your extension's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Redis
redis_conn = Redis()
q = Queue('mcp-tasks', connection=redis_conn)

class PageContent(BaseModel):
    url: str
    title: str
    text: str

@app.post("/add_to_index")
async def add_to_index(payload: PageContent):
    try:
        print("📥 Queuing HTML content...")

        arguments = {
            "url": payload.url,
            "title": payload.title,
            "text": payload.text
        }

        # Enqueue the job using the correct function reference
        job = q.enqueue(run_sync_process_html_job, arguments)

        return {
            "status": "queued",
            "message": "HTML content enqueued for processing",
            "job_id": job.get_id()
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Queueing failed: {str(e)}"
        }

@app.post("/run-process-documents")
async def run_process_documents():
    try:
        print("📥 Queuing process_documents task...")

        job = q.enqueue(run_sync_process_html_job,{})

        return {
            "status": "queued",
            "message": "Document processing enqueued",
            "job_id": job.get_id()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Queueing failed: {e}")


@app.post("/run-process-documents")
async def run_process_documents():
    try:
        print("📥 Queuing process_documents task...")

        job = q.enqueue(run_sync_process_documents_job)

        return {
            "status": "queued",
            "message": "Document processing enqueued",
            "job_id": job.get_id()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Queueing failed: {e}")

@app.get("/")
def root():
    return {"message": "MCP FastAPI with Redis Queue is running"}



@app.get("/job-status/{job_id}")
def get_job_status(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_conn)

        return {
            "status": job.get_status(),
            "result": job.result if job.is_finished else None,
            "enqueued_at": str(job.enqueued_at),
            "started_at": str(job.started_at) if job.started_at else None,
            "ended_at": str(job.ended_at) if job.ended_at else None,
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Job not found or error: {e}")
