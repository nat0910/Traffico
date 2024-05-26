import cv2
from ultralytics import YOLO
import threading
import queue
import time
import pandas as pd
import os

camera = cv2.VideoCapture('videos/Camera01.MOV')  # Ensure correct video source path

model = YOLO('yolo_models/yolov8n.pt')
helmet_model = YOLO('yolo_models\helmet\helmet-detection-weights.pt')

frame_queue = queue.Queue(maxsize=10)

without_helmet_classid = 1

from app.utils.without_helmet import HelmetDetection


speed_obj = HelmetDetection()

speed_obj.set_args(
    reg_pts=[(0, int(500 * 0.7)), (1020, int(500 * 0.7))],
    names=['person','motorcycle'],
    view_img=False,  # No need for local display
)


# def process_frame():
#     while True:
#         success, frame = camera.read()

#         if not success:
#             break

#         frame = cv2.resize(frame, (1020, 500))

#         # Run YOLOv8 tracking on the frame
#         results = helmet_model.track(frame, persist=True, show=False)

#         # Render the detections on the frame
#         if len(results) > 0:
#             annotated_frame = results[0].plot()  # results.render() returns a list of images

#             # Encode the frame in JPEG format
#             ret, buffer = cv2.imencode('.jpg', annotated_frame)

#             if ret:
#                 frame_queue.put(buffer.tobytes())
#             else:
#                 frame_queue.put(None)
#                 break
#         else:
#             # If no detections, put the original frame to the queue
#             ret, buffer = cv2.imencode('.jpg', frame)
#             if ret:
#                 frame_queue.put(buffer.tobytes())
#             else:
#                 frame_queue.put(None)
#                 break


# def process_frames():
#     while True:
#         success, frame = camera.read()
#         if not success:
#             frame_queue.put(None)  # Signal the generator to stop
#             break

#         frame = cv2.resize(frame, (1020, 500))

#         # Run helmet detection on the frame
#         results = helmet_model.track(frame, persist=True, show=False)
#         exported_images = set()

#         if results:
#             for det in results[0].boxes.data.detach().cpu().numpy():  # detections per frame
#                 if int(det[-1]) == without_helmet_classid:  # Check for 'without helmet' class ID
#                     x1, y1, x2, y2 , track_id = map(int, det[:5])  # Get original bounding box coordinates
#                     cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Calculate center of the bounding box
#                     new_width = (x2 - x1) * 4
#                     new_height = (y2 - y1) * 6
#                     new_x1 = max(0, cx - new_width // 2)
#                     new_y1 = max(0, cy - new_height // 2)
#                     new_x2 = min(1020, cx + new_width // 2)
#                     new_y2 = min(500, cy + new_height // 2)
#                     cv2.rectangle(frame, (new_x1, new_y1), (new_x2, new_y2), (0, 0, 255), 2)  # Draw new bounding box
#                     if track_id not in exported_images:
#                         image_name = f"track_{track_id}_speed_{'without helmet'}kmph.jpg"
#                         image_path = os.path.join('instance/data/violation-detected/helmet-violation', image_name)
#                         cropped_region = frame[new_y1:new_y2, new_x1:new_x2]
#                         cv2.imwrite(image_path, cropped_region)
#                         # cv2.imwrite(image_path, self.im0)
#                         exported_images.add(track_id)
#         # Encode and queue the frame
#         ret, buffer = cv2.imencode('.jpg', frame)
#         if ret:
#             frame_queue.put(buffer.tobytes())
#         else:
#             frame_queue.put(None)
#             break




def process_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = cv2.resize(frame, (1020, 500))
        tracks = model.track(frame, persist=True, show=False)
        frame = speed_obj.estimate_speed(frame, tracks, path='instance/data/violation-detected/helmet-violation', speed_threshold=10)

        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            frame_queue.put(buffer.tobytes())
        else:
            frame_queue.put(None)
            break


def gen_frames():
    threading.Thread(target=process_frames, daemon=True).start()

    while True:
        frame_bytes = frame_queue.get()
        if frame_bytes is None:
            break

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
