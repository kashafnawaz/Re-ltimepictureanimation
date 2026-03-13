from workers.video_utils import extract_frames, reconstruct_video

print("Starting test...")

extract_frames("sample.mp4", "test_frames")

reconstruct_video("test_frames", "test_output.mp4")

print("Engine test completed!")