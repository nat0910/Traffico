from flask import Blueprint,render_template,Response
import cv2

from app.controller.seatbelt_detection_controller import gen_frames



seatbelt_blueprint = Blueprint('/seatbelt-detection',__name__)



@seatbelt_blueprint.route('/',methods=['GET'])
def handle_loading_page():
    return render_template('seatbelt-detection.html')

            
@seatbelt_blueprint.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')