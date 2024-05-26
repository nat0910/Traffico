from flask_cors import CORS
from ultralytics import YOLO
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
cors = CORS()

def setup_extensions(app):
    db.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    try:
        app.helmet_detection = YOLO(app.config['HELMET_MODEL_PATH'])
        app.speed_detection = YOLO(app.config['SPEED_MODEL_PATH'])
        app.seatbelt_detection = YOLO(app.config['SEATBELT_MODEL_PATH'])
        app.license_detection = YOLO(app.config['LICENSE_PLATE_MODEL_PATH'])
        # app.signal_detection = YOLO(app.config['SIGNAL_MODEL_PATH'])
    except Exception as e:
        print(f"Error initializing YOLO models: {e}")



# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from joblib import load
# from .utils.utils import load_annoy_model
# from flask_jwt_extended import JWTManager
# from flask_migrate import Migrate

# db = SQLAlchemy()
# cors = CORS()
# jwt = JWTManager()
# migrate = Migrate()

# def setup_extensions(app):
#     db.init_app(app)  # Initialize Flask-SQLAlchemy Database
#     migrate.init_app(app, db)  # Initialize Flask-Migrate
#     jwt.init_app(app)  # Initialize Jwt Tokens
#     # CORS(app)
#     cors.init_app(app, resources={r"/*":{"origins": "*"}})
    

#     # Preload the Scaler model 
#     app.trained_scaler_model = load('trained_model/cluster/nutritional_scaler.pkl')
    
#     # Preload the K-means model 
#     app.trained_kmeans_model = load('trained_model/cluster/nutritional_cluster_kmeans.pkl')

#     # Preload the trained TD-IDF Vectorizer
#     app.trained_key_ingred_tdidf = load('trained_model/utils/combine_key_ingred/key_ingred_combinded_tdidf_vectorizer.joblib')
#     app.trained_recipe_name_tdidf = load('trained_model/utils/recipe_name/recipe_name_tdidf_vectorizer.joblib')

#     # Preload the trained SVD
#     app.trained_key_ingred_svd = load('trained_model/utils/combine_key_ingred/key_ingred_combinded_svd_model.joblib')
#     app.trained_recipe_name_svd = load('trained_model/utils/recipe_name/recipe_name_svd_model2.joblib')

#     # Preload the trained ANN Model
#     app.trained_ann_key_ingred_model = load_annoy_model('trained_model/ml_models/combine_key_ingred/reduced_key_ingred_combinded_annoy_index.ann')
#     app.trained_recipe_name_model = load_annoy_model('trained_model/ml_models/recipe_name/recipe_name_annoy_index.ann')