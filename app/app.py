from flask import (
    Flask,
    request,
    redirect,
    flash,
    url_for,
    render_template,
    send_from_directory
)
from PIL import Image
import pickle
import os

from app.utils import edibility_tuple
from settings import SECRET_KEY
from prediction.predict import classify


app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)
app.secret_key = SECRET_KEY


with open("mushrooms_names.pickle", "rb") as file:
    mushrooms_names = pickle.load(file)


@app.route('/')
def index():
    return render_template(
        'index.html',
    )


@app.route('/recognize', methods=['POST'])
def recognize():
    file = request.files["image"]
    filename = file.filename
    image_path = "app/uploads/" + filename
    file.save(image_path)
    try:
        with Image.open(file) as img:
            img.verify()
    except Exception:
        os.remove(image_path)
        flash("Uploaded file is not a valid image")
        return redirect(url_for("index"))

    prediction = classify(image_path=image_path)
    prediction = list(prediction[0])
    prediction_data = sorted(
        filter(
            lambda x: x[1] > 0.01,
            zip(mushrooms_names, prediction, edibility_tuple)
        ),
        key=lambda x: x[1],
        reverse=True
    )
    data_list_of_dicts = [
        {"name": name, "prediction": pred, "edibilyty": edibilyty}
        for name, pred, edibilyty
        in prediction_data
    ]
    for dict_data in data_list_of_dicts:
        dict_data["images"] = get_images_names(dict_data["name"])
    print(data_list_of_dicts)

    not_edible = sum(
        mushroom["prediction"]
        for mushroom
        in data_list_of_dicts
        if mushroom["edibilyty"] != "edible"
    )
    for mushroom in data_list_of_dicts:
        mushroom["images"] = (get_images_names(mushroom["name"]))

    return render_template(
        'recognize.html',
        predictions=data_list_of_dicts,
        not_edible=not_edible,
        uploaded_image_name=filename,
    )


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    upload_folder = os.path.join(app.root_path, "uploads")
    return send_from_directory(upload_folder, filename)


def get_images_names(mashroom_name):
    path = os.path.join(
        app.root_path, "static", "images", "merged_dataset", mashroom_name
    )
    return [
        f for f in os.listdir(path) if f.lower().endswith((".jpg", ".png"))
    ]


if __name__ == '__main__':
    app.run(debug=True)
