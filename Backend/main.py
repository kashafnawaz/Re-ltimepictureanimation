from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
import os
import uuid
import shutil

from app import process_job

app = FastAPI(
    title="Real-Time Picture Animation API",
    description="Generates anime-style talking video from image and audio",
    version="1.0.0"
)

job_status = {}

@app.get("/")
def home():
    return {"message": "Welcome to Real-Time Picture Animation API"}

@app.post("/generate")
async def generate(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    audio: UploadFile = File(...)
):
    # Create unique job
    job_id = str(uuid.uuid4())[:8]
    job_folder = os.path.join("results", job_id, "input")
    os.makedirs(job_folder, exist_ok=True)

    # Save uploaded files
    image_path = os.path.join(job_folder, image.filename)
    audio_path = os.path.join(job_folder, audio.filename)

    with open(image_path, "wb") as f:
        shutil.copyfileobj(image.file, f)
    with open(audio_path, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    # Start pipeline in background
    job_status[job_id] = "started"
    background_tasks.add_task(process_job, job_id, job_status)

    return {"job_id": job_id, "status": "started"}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    status = job_status.get(job_id, "not_found")
    return {"job_id": job_id, "status": status}

@app.get("/result/{job_id}/sadtalker")
def get_sadtalker_result(job_id: str):
    video_path = os.path.join("results", job_id, "sadtalker.mp4")
    if os.path.exists(video_path):
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename="sadtalker.mp4"
        )
    return JSONResponse(
        {"error": "SadTalker video not ready yet"},
        status_code=404
    )

@app.get("/result/{job_id}/final")
def get_final_result(job_id: str):
    video_path = os.path.join("results", job_id, "output.mp4")
    if os.path.exists(video_path):
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename="output.mp4"
        )
    return JSONResponse(
        {"error": "Final video not ready yet"},
        status_code=404
    )