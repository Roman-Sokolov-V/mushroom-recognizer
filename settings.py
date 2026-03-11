from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
KERAS_MODEL = "mushroom_model_0.81151.keras"
MODEL_PATH = os.path.join("prediction", "static", "models", KERAS_MODEL)
