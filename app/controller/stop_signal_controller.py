import cv2
from ultralytics import YOLO

from app.utils.stop_detection import StopSignal

import threading
import queue
import time

# Initialize the camera, model, and SpeedEstimator
camera = cv2.VideoCapture('videos/speed-detect.mp4')  # Ensure correct video source path

model = YOLO('yolo_models/speed-detection/speed-detection-weights.pt')

speed_obj = StopSignal()

speed_obj.set_args(
    reg_pts=[(0, int(500 * 0.75)), (1020, int(500 * 0.75))],
    names=model.model.names,
    view_img=False,  # No need for local display
)

frame_queue = queue.Queue(maxsize=10)

def process_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = cv2.resize(frame, (1020, 500))
        tracks = model.track(frame, persist=True, show=False)
        frame = speed_obj.check_signal(frame, tracks, path='instance/data/violation-detected/signal-detection')

        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            frame_queue.put(buffer.tobytes())
        else:
            frame_queue.put(None)
            break

    speed_obj.stop()

def gen_frames():

    threading.Thread(target=process_frames, daemon=True).start()

    while True:
        frame_bytes = frame_queue.get()
        if frame_bytes is None:
            break

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
