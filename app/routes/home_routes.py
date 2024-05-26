from flask import Blueprint,render_template,Response
import cv2


home_blueprint = Blueprint('/',__name__)



@home_blueprint.route('/',methods=['GET'])
def handle_loading_page():
    return render_template('index.html')

