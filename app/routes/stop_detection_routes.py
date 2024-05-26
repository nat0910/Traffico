from flask import Blueprint,render_template,Response
import cv2
from app.controller.stop_signal_controller import gen_frames
camera = cv2.VideoCapture(r'videos\highway.mp4')

signal_jumping_blueprint = Blueprint('/signal-jumping',__name__)



@signal_jumping_blueprint.route('/',methods=['GET'])
def handle_loading_page():
    return render_template('stop-signal.html')
       
@signal_jumping_blueprint.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')