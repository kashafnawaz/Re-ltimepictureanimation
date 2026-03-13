import os
import cv2


# -------------------------------------------------
# 1️⃣ Extract Frames From Video
# -------------------------------------------------
def extract_frames(video_path, output_folder, resize_width=512):

    if not os.path.exists(video_path):
        raise Exception("Video file not found for frame extraction")

    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception("Failed to open video file")

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize for CPU safety (keep aspect ratio)
        height, width = frame.shape[:2]
        scale = resize_width / float(width)
        new_height = int(height * scale)

        resized_frame = cv2.resize(frame, (resize_width, new_height))

        frame_filename = os.path.join(
            output_folder,
            f"frame_{frame_count:05d}.jpg"
        )

        cv2.imwrite(frame_filename, resized_frame)

        frame_count += 1

    cap.release()

    if frame_count == 0:
        raise Exception("No frames were extracted from video")

    print(f"[INFO] Extracted {frame_count} frames successfully")


# -------------------------------------------------
# 2️⃣ Reconstruct Video From Frames
# -------------------------------------------------
def reconstruct_video(frames_folder, output_path, fps=25):

    if not os.path.exists(frames_folder):
        raise Exception("Frames folder does not exist")

    frames = sorted([
        f for f in os.listdir(frames_folder)
        if f.lower().endswith(".jpg")
    ])

    if len(frames) == 0:
        raise Exception("No frames found for reconstruction")

    # Read first frame to get size
    first_frame_path = os.path.join(frames_folder, frames[0])
    first_frame = cv2.imread(first_frame_path)

    if first_frame is None:
        raise Exception("Failed to read first frame")

    height, width = first_frame.shape[:2]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame_name in frames:
        frame_path = os.path.join(frames_folder, frame_name)
        frame = cv2.imread(frame_path)

        if frame is None:
            continue

        out.write(frame)

    out.release()

    if not os.path.exists(output_path):
        raise Exception("Video reconstruction failed")

    print("[INFO] Final video reconstructed successfully")