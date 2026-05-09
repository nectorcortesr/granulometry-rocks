import cv2
import os

def cut_video(input_path, output_path, start_sec, end_sec):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input video not found: {input_path}")

    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        raise ValueError("Could not open input video")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        raise ValueError("FPS is zero, invalid video")

    start_frame = int(start_sec * fps)
    end_frame = int(end_sec * fps)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    for frame_idx in range(start_frame, end_frame):
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

    print(f"Video cut successfully: {output_path}")


if __name__ == "__main__":
    input_video = "data/videos/raw.mp4"
    output_video = "data/videos/tape_test.mp4"

    # Adjust these values after reviewing the video
    start_sec = 184   # example: 3:04
    end_sec = 216    # example: 3:36

    cut_video(input_video, output_video, start_sec, end_sec)