# from flask import Flask,jsonify,render_template,Response
# import cv2


# app = Flask(__name__)
# camera = cv2.VideoCapture(r'videos\highway.mp4')

# @app.route('/',methods=["GET"])
# def handle_home_page():
#     return render_template("index.html")

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

#             cv2.line(frame, (172, 198), (774, 198), red_color, 2)
#             cv2.putText(frame, 'Red Line', (172, 198), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

#             cv2.line(frame, (8, 268), (927, 268), blue_color, 2)
#             cv2.putText(frame, 'Blue Line', (8, 268), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
#             ret, buffer = cv2.imencode('.jpg', frame)
        
            
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
            
# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



# if __name__ == '__main__':
#     app.run(host='0.0.0.0',debug=True)
#     pass

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
