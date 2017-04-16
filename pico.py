import os
import random
import hashlib
import flask
import peewee
from PIL import Image

app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # 30 megabytes
app.config["BLOB_FOLDER"] = "IMAGES" # Name of the LOCAL folder 
									 # in which images are saved.


@app.route("/", methods = ["GET", "POST"])
def index():
	if flask.request.method == "GET":
		return flask.render_template("index.html")

	elif flask.request.method == "POST":

		# Save the uploaded file to a temporary location.
		file = flask.request.files["image"]

		extension = file.filename.split(".")[-1]
		tempname = "temp_{}.{}".format(str(random.randint(0,9999)),extension)

		file.save(os.path.join(app.config["BLOB_FOLDER"], tempname))

		# Load up the saved temporary file and get its hash
		file = open(os.path.join(app.config["BLOB_FOLDER"], tempname),"rb")
		data = file.read()
		file.close()

		m = hashlib.md5()
		m.update(data)
		name = m.hexdigest()

		# Convert the file to .jpg format and save it under the new
		# name obtained by hashing.
		im = Image.open(os.path.join(app.config["BLOB_FOLDER"], tempname))
		im.save(os.path.join(app.config["BLOB_FOLDER"], name + ".jpg"), "JPEG")

		# Delete the temporary file.
		os.remove(os.path.join(app.config["BLOB_FOLDER"], tempname))

		return flask.redirect(flask.url_for("image",image_id = name+".jpg"))

		

	
@app.route("/<string:image_id>")
def image(image_id):
	return flask.send_file(os.path.join(app.config["BLOB_FOLDER"], image_id))






if __name__ == "__main__":
	app.run(
		host = "0.0.0.0",
		port = 80,
		debug = True
		)

