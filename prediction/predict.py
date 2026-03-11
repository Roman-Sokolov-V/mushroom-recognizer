import tensorflow as tf
from settings import MODEL_PATH

IMAGE_SIZE = (224, 224)

prediction_model = tf.keras.models.load_model(MODEL_PATH, compile=False)


def preprocess(image):
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = tf.expand_dims(img_array, axis=0)
    return img_array


def load_and_preprocess(image_path: str):
    image = tf.keras.preprocessing.image.load_img(
        image_path,
        target_size=IMAGE_SIZE
    )
    return preprocess(image)


def classify(image_path: str, model: tf.keras.Model = prediction_model):
    preprocessed_image = load_and_preprocess(image_path)
    return model.predict(preprocessed_image)
