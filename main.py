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
    # Get the sample image from the images folder to display
    sample_image = os.path.join(
        app.config['UPLOAD_FOLDER'], 'thunderstorm.jpg')

    # Get common colors from that image
    common_colors = get_colors(sample_image, 10)

    # The works only when user upload some images
    # This removes all the files except the sample image
    delete_uploaded_images()

    return render_template("index.html", image=sample_image, colors=common_colors, year=current_year)


@app.route("/upload", methods=["GET", "POST"])
def get_image():
    if request.method == "POST":
        # If image is empty
        if "image" not in request.files:
            return redirect("/")
        # Else get the image and save it in the upload folder
        file = request.files["image"]
        image = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(image)

        # Check if file is not an image
        try:
            # If file is an image get 10 common colors and load index file with that image
            frequent_colors = get_colors(image, 10)

            return render_template("index.html", image=image, colors=frequent_colors, year=current_year)

        except:
            return redirect("/")


def get_colors(image_file, num_of_colors):
    # Open the image
    image = Image.open(image_file)
    # Get all the colors as a dictionary
    colors = Counter(image.getdata())

    # Order color the with the most used order
    sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
    # Add it to a dictionary
    sorted_colors = dict(sorted_colors)

    # Get number of most used colors
    frequent_colors = list(sorted_colors.keys())[0:num_of_colors - 1]

    # Convert rbg colors to hex and return
    hex_colors = []

    for color in frequent_colors:
        r = color[0]
        g = color[1]
        b = color[2]

        hex_colors.append(rgb2hex(r, g, b))

    return hex_colors

# Convert rbg colors to hex
def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def delete_uploaded_images():
    # list all the file in the image folder
    files_path = os.listdir(IMG_FOLDER)

    # If there are files other than sample in the image folder
    for file in files_path:
        if file != "thunderstorm.jpg":
            os.remove(f"{IMG_FOLDER}/{file}")


if __name__ == "__main__":
    app.run()
