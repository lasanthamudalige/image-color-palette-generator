from flask import Flask, render_template, redirect, request
import datetime
import os
from PIL import Image
from collections import Counter


app = Flask(__name__)

IMG_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER


# Current date
current_year = datetime.date.today().year


@app.route("/")
def home():
    sample_image = os.path.join(
        app.config['UPLOAD_FOLDER'], 'thunderstorm.jpg')

    frequent_colors = get_colors(sample_image, 10)

    delete_uploaded_images()

    return render_template("index.html", image=sample_image, colors=frequent_colors, year=current_year)


@app.route("/upload", methods=["GET", "POST"])
def get_image():
    if request.method == "POST":
        if "image" not in request.files:
            return redirect("/")

        file = request.files["image"]
        image = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(image)

        try:
            frequent_colors = get_colors(image, 10)

            return render_template("index.html", image=image, colors=frequent_colors, year=current_year)

        except:
            return redirect("/")


def get_colors(image_file, num_of_colors):
    image = Image.open(image_file)
    colors = Counter(image.getdata())

    sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
    sorted_colors = dict(sorted_colors)

    frequent_colors = list(sorted_colors.keys())[0:num_of_colors - 1]

    hex_colors = []

    for color in frequent_colors:
        r = color[0]
        g = color[1]
        b = color[2]

        hex_colors.append(rgb2hex(r, g, b))

    return hex_colors


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def delete_uploaded_images():
    files_path = os.listdir(IMG_FOLDER)

    for file in files_path:
        if file != "thunderstorm.jpg":
            os.remove(f"{IMG_FOLDER}/{file}")


if __name__ == "__main__":
    app.run()
