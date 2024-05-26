from flask import Flask
from app.extension import db,setup_extensions
from app.routes import *
from app.models.violation_model import TrafficViolation
from datetime import datetime


def create_app():
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile('config.py')
    print("HELMET DETECTION MODEL:", app.config['HELMET_MODEL_PATH'])
    print("SPEED DETECTION MODEL:", app.config['SPEED_MODEL_PATH']) 
    print("SEATBELT DETECTION MODEL:", app.config['SEATBELT_MODEL_PATH']) 
    print("LICENSE DETECTION MODEL:", app.config['LICENSE_PLATE_MODEL_PATH']) 


    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI']) 
    print(f"Config loaded:, SECRET_KEY: {app.config.get('SECRET_KEY')}")

    setup_extensions(app)


    with app.app_context():
        db.create_all()
        print("Tables created successfully")
        dummy_data = [
            {
                'number_plate': 'ABC123',
                'timestamp': datetime.utcnow(),
                'camera_id': 'CAM1',
                'violation_type': 'Speeding'
            },
            {
                'number_plate': 'XYZ456',
                'timestamp': datetime.utcnow(),
                'camera_id': 'CAM2',
                'violation_type': 'Red Light Violation'
            }
        ]

        # Add dummy data to the database
        for data in dummy_data:
            new_violation = TrafficViolation(
                number_plate=data['number_plate'],
                timestamp=data['timestamp'],
                camera_id=data['camera_id'],
                violation_type=data['violation_type']
            )
            db.session.add(new_violation)

        # Commit the changes to the database
        db.session.commit()

    app.register_blueprint(home_routes.home_blueprint,url_prefix='/')
    app.register_blueprint(helmet_detection_routes.helmet_blueprint,url_prefix='/helmet-detection')
    app.register_blueprint(speed_detection_routes.speed_detection_blueprint,url_prefix='/speed-detection')
    app.register_blueprint(seatbelt_detection_routes.seatbelt_blueprint,url_prefix='/seatbelt-detection')
    app.register_blueprint(stop_detection_routes.signal_jumping_blueprint,url_prefix='/signal-jumping')


    return app