import cv2
import os

def audit_conveyor_video(video_path: str) -> dict:
    """
    Extract basic information from the video tape to assess the scope of the problem.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")
        
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Silent failure avoided: OpenCV could not open the video.")
        
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = float(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate duration in seconds (beware of the case fps = 0.0)
    duration_sec = total_frames / fps if fps > 0 else 0
    
    cap.release()

    return {
        "resolution": (width, height),
        "fps": fps,
        "total_frames": total_frames,
        "duration_sec": duration_sec
    }


if __name__ == "__main__":
    # Test 1: expected error
    try:
        audit_conveyor_video("dummy_not_exists.mp4")
    except FileNotFoundError as e:
        print(f"Edge case OK: {e}")

    # Test 2: real case
    video_path = "data/videos/tape_test.mp4"

    if os.path.exists(video_path):
        res = audit_conveyor_video(video_path)
        assert isinstance(res, dict) and "fps" in res
        print(f"Successful audit: {res}")