import subprocess
import os
import glob
import shutil

ANIMEGAN_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../models/AnimeGANv2")
)
CHECKPOINT_DIR = os.path.join(ANIMEGAN_DIR, "checkpoint", "generator_Shinkai_weight")
PYTHON = r"C:\ProgramData\anaconda3\envs\animegan_env\python.exe"

def run_animegan(input_video, output_path):
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    input_video = os.path.abspath(input_video)
    output_dir  = os.path.abspath(output_dir)

    cmd = [
        PYTHON, "video2anime.py",
        "--video",          input_video,
        "--checkpoint_dir", CHECKPOINT_DIR,
        "--output",         output_dir,
    ]

    print("[INFO] Running AnimeGANv2:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ANIMEGAN_DIR)

    if result.returncode != 0:
        raise Exception("AnimeGANv2 process failed")

    # Find generated video
    generated = glob.glob(os.path.join(output_dir, "*_AnimeGANv2.mp4"))
    if not generated:
        raise Exception("AnimeGANv2 output video not found")

    anime_video = generated[0]

    # Merge audio from original SadTalker video
    print("[INFO] Merging audio into anime video...")
    temp_output = output_path.replace(".mp4", "_temp.mp4")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", anime_video,
        "-i", input_video,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        temp_output
    ]
    subprocess.run(ffmpeg_cmd)
    os.replace(temp_output, output_path)
    print(f"[INFO] Final video with audio saved to {output_path}")

    return output_path