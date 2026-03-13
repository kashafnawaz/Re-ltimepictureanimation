import os
import traceback
import shutil
from workers.sadtalker import run_sadtalker
from workers.animegan import run_animegan

def process_job(job_id, job_status):
    try:
        print(f"[INFO] Starting job {job_id}")
        job_folder = os.path.join("results", job_id)
        input_folder = os.path.join(job_folder, "input")
        image_path = None
        audio_path = None

        for file in os.listdir(input_folder):
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                image_path = os.path.join(input_folder, file)
            elif file.lower().endswith((".wav", ".mp3")):
                audio_path = os.path.join(input_folder, file)

        if not image_path or not audio_path:
            raise Exception("Missing image or audio file")

        # Stage 1 — SadTalker
        job_status[job_id] = "running_sadtalker"
        print("[INFO] Running SadTalker...")
        sadtalker_output = os.path.join(job_folder, "sadtalker.mp4")
        run_sadtalker(
            image_path=image_path,
            audio_path=audio_path,
            output_path=sadtalker_output
        )
        if not os.path.exists(sadtalker_output):
            raise Exception("SadTalker failed")
        job_status[job_id] = "sadtalker_completed"
        print("[INFO] SadTalker completed")

        # Stage 2 — AnimeGANv2
        job_status[job_id] = "running_animegan"
        print("[INFO] Running AnimeGANv2...")
        animegan_output = os.path.join(job_folder, "output.mp4")
        run_animegan(
            input_video=sadtalker_output,
            output_path=animegan_output
        )
        if not os.path.exists(animegan_output):
            raise Exception("AnimeGAN failed")
        job_status[job_id] = "completed"
        print(f"[SUCCESS] Job {job_id} completed — anime video ready!")

    except Exception as e:
        job_status[job_id] = "failed"
        print(f"[ERROR] Job {job_id} failed")
        traceback.print_exc()

if __name__ == "__main__":
    job_status = {}
    process_job("testjob", job_status)
    print(job_status)