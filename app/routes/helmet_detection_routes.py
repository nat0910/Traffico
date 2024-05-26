# from flask import Blueprint,render_template,Response,current_app

# import cv2


# camera = cv2.VideoCapture(r'videos/Camera01.MOV')

# helmet_blueprint = Blueprint('/helmet',__name__)

# @helmet_blueprint.route('/',methods=['GET'])
# def handle_loading_page():
#     return render_template('helmet-detection.html')

# def gen_frames():  

#     red_color = (0, 0, 255)
#     blue_color = (255, 0, 0)
#     text_color = (0, 0, 0) 
    
#     while True:
#         success, frame = camera.read()  # read the camera frame
#         if not success:
#             break
#         else:
#             frame = cv2.resize(frame, (1020, 500))

#             model = current_app.helmet_detection

#             result = model

#             cv2.line(frame, (172, 198), (774, 198), red_color, 2)
#             cv2.putText(frame, 'Red Line', (172, 198), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

#             cv2.line(frame, (8, 268), (927, 268), blue_color, 2)
#             cv2.putText(frame, 'Blue Line', (8, 268), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
#             ret, buffer = cv2.imencode('.jpg', frame)
        
            
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
            
# @helmet_blueprint.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

from flask import Blueprint,render_template,Response
from app.controller.helmet_detection_controller import gen_frames


helmet_blueprint = Blueprint('/helmet-detection',__name__)

@helmet_blueprint.route('/',methods=['GET'])
def handle_loading_page():
    return render_template('helmet-detection.html')

@helmet_blueprint.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
