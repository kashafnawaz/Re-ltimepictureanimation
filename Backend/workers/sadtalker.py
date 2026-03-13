import subprocess
import os
import glob
import shutil

SADTALKER_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../models/SadTalker")
)
CHECKPOINT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../checkpoints")
)
PYTHON = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../venv/Scripts/python.exe")
)

def run_sadtalker(image_path, audio_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image_path = os.path.abspath(image_path)
    audio_path = os.path.abspath(audio_path)
    result_dir = os.path.abspath(os.path.dirname(output_path))

    cmd = [
        PYTHON, "inference.py",
        "--source_image",   image_path,
        "--driven_audio",   audio_path,
        "--result_dir",     result_dir,
        "--checkpoint_dir", CHECKPOINT_DIR,
        "--still",
        "--preprocess",     "resize",
        "--batch_size",     "1",
    ]

    print("[INFO] Running SadTalker:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=SADTALKER_DIR)

    if result.returncode != 0:
        raise Exception("SadTalker process failed")

    # Find generated video and copy to expected path
    generated = glob.glob(os.path.join(result_dir, "*.mp4"))
    if generated:
        shutil.copy(generated[0], output_path)

    return output_path