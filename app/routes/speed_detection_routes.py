from flask import Blueprint,render_template,Response
from app.controller.speed_detection_controller import gen_frames

speed_detection_blueprint = Blueprint('/speed-detection',__name__)

@speed_detection_blueprint.route('/',methods=['GET'])
def handle_loading_page():
    return render_template('speed-detection.html')
       
@speed_detection_blueprint.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')