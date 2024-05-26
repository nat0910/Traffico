from collections import defaultdict
from time import time
from datetime import datetime

import cv2
import numpy as np

from ultralytics.utils.checks import check_imshow
from ultralytics.utils.plotting import Annotator,colors

import threading
import cv2
import numpy as np


import os

class StopSignal:

    def __init__(self) -> None:
        
        self.im0 = None
        self.annotator = None
        self.view_img = False
        self.reg_pts = [(20, 400), (1260, 400)]
        self.region_thickness = 3

        self.clss = None
        self.names = None
        self.boxes = None
        self.trk_ids = None
        self.trk_pts = None
        self.line_thickness = 2
        self.trk_history = defaultdict(list)

        self.current_time = 0
        self.dist_data = {}
        self.trk_idslist = []
        self.spdl_dist_thresh = 10
        self.trk_previous_times = {}
        self.trk_previous_points = {}
        self.red_line_violators =[]
        self.exported_images = set()

        self.env_check = check_imshow(warn=True)

        self.traffic_signal_state = True  # False represents green, True represents red
        self.keep_running = True
        self.start_traffic_signal_toggle()


    def set_args(
        self,
        reg_pts,
        names,
        view_img=False,
        line_thickness=2,
        region_thickness=5,
        spdl_dist_thresh=10,
    ):
        if reg_pts is None:
            print("Region points not provided, using default values")
        else:
            self.reg_pts = reg_pts
        self.names = names
        self.view_img = view_img
        self.line_thickness = line_thickness
        self.region_thickness = region_thickness
        self.spdl_dist_thresh = spdl_dist_thresh

    def extract_tracks(self, tracks):
        """
        Extracts results from the provided data.

        Args:
            tracks (list): List of tracks obtained from the object tracking process.
        """
        self.boxes = tracks[0].boxes.xyxy.cpu()
        self.clss = tracks[0].boxes.cls.cpu().tolist()
        self.trk_ids = tracks[0].boxes.id.int().cpu().tolist()

    def store_track_info(self, track_id, box):
        """
        Store track data.

        Args:
            track_id (int): object track id.
            box (list): object bounding box data
        """
        track = self.trk_history[track_id]
        bbox_center = (float((box[0] + box[2]) / 2), float((box[1] + box[3]) / 2))
        track.append(bbox_center)

        if len(track) > 5:
            track.pop(0)

        self.trk_pts = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
        return track
    
    def display_frames(self):
        """Display frame."""
        # cv2.imshow("Ultralytics Speed Estimation", self.im0)
        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     return

    def check_line_crossing(self,trk_id,track,traffic_signal_state):

        if not self.reg_pts[0][0] < track[-1][0] < self.reg_pts[1][0]:
            return
      
        if (self.reg_pts[1][1] - self.spdl_dist_thresh < track[-1][1] < self.reg_pts[1][1] + self.spdl_dist_thresh or
                self.reg_pts[0][1] - self.spdl_dist_thresh < track[-1][1] < self.reg_pts[0][1] + self.spdl_dist_thresh):
                if traffic_signal_state == True:
                    if trk_id not in self.red_line_violators:
                        self.red_line_violators.append(trk_id)
                        print(f"Violation: Car {trk_id} crossed the line on red at position {track[-1]}. Added to violators list.")

    def plot_box_and_track(self, track_id, box, cls, track, traffic_signal_state = False,path=None):
        """
            Plot track and bounding box, highlighting red light violations.

            Args:
                track_id (int): object track id.
                box (list): object bounding box data
                cls (str): object class name
                track (list): tracking history for tracks path drawing
                path (str): path to save images of violations
         """

        violation_label = "Red Light Violation" if track_id in self.red_line_violators else self.names[int(cls)]
        bbox_color = (0, 0, 255) if track_id in self.red_line_violators else (255, 0, 255)  # Red for violators, magenta otherwise

        self.annotator.box_label(box, violation_label, bbox_color)
        cv2.circle(self.im0, (int(track[-1][0]), int(track[-1][1])), 5, bbox_color, -1)

        if track_id in self.red_line_violators:
            if track_id not in self.exported_images:
                current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                image_name = f"track_{track_id}_{current_datetime}.jpg"
                image_path = os.path.join(path, image_name)
                x1, y1, x2, y2 = map(int, box)
                cropped_region = self.im0[y1:y2, x1:x2]
                cv2.imwrite(image_path, cropped_region)
                self.exported_images.add(track_id)



    def check_signal(self, im0, tracks, path=None, region_color=(255, 0, 0)):

        self.im0 = im0
        if tracks[0].boxes.id is None:
            if self.view_img and self.env_check:
                self.display_frames()
            return im0
        self.extract_tracks(tracks)

        self.annotator = Annotator(self.im0, line_width=2)
        self.annotator.draw_region(reg_pts=self.reg_pts, color=region_color, thickness=self.region_thickness)
    
        for box, trk_id, cls in zip(self.boxes, self.trk_ids, self.clss):
            track = self.store_track_info(trk_id, box)

            if trk_id not in self.trk_previous_times:
                self.trk_previous_times[trk_id] = 0

            self.check_line_crossing(trk_id, track, self.traffic_signal_state)
            self.plot_box_and_track(trk_id, box, cls, track,traffic_signal_state=self.traffic_signal_state, path=path)
            
            # Removed speed calculation and simplified to focus on violations    

        if self.view_img and self.env_check:
            self.display_frames()

        return im0
    
    def toggle_traffic_signal(self):
        while self.keep_running:
            threading.Event().wait(60)
            self.traffic_signal_state = not self.traffic_signal_state
            print(f"Traffic signal state changed to: {'Red' if self.traffic_signal_state else 'Green'}")

    def start_traffic_signal_toggle(self):
        self.signal_thread = threading.Thread(target=self.toggle_traffic_signal)
        self.signal_thread.daemon = True
        self.signal_thread.start()
    
    def stop(self):
        self.keep_running = False
        self.signal_thread.join()
if __name__ == "__main__":
    stop_signal = StopSignal()
    stop_signal.start_traffic_signal_toggle()