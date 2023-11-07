
import sys, os
from werkzeug.utils import secure_filename
from flask import Flask,send_file, abort, render_template, request,url_for,flash,redirect
from src.logger import logging
from src.exception import FaceDetectionException
from src.components.face_detect_image import FaceDetectionImage
from src.components.face_detect_webcam import FaceDetectionWebcam
from flask import send_from_directory

app=Flask(__name__)

if not os.path.exists('uploads'):
    os.makedirs('uploads')

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(APP_ROOT,'uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/",methods=['GET','POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        sharing = FaceDetectionException(e,sys)
        logging.info(sharing.error_message)

# ABC.jpg
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file present')
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            print('No file selected')
            return redirect(request.url)
        

        if file and allowed_file(file.filename):
            print(file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return render_template("image.html")

@app.route('/uploads/<name>')
def download_file(name):
    img_path = os.path.join(UPLOAD_FOLDER, name)
    face_detect_obj = FaceDetectionImage(image_path=img_path)
    face_detect_obj.display_image()
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/webcam', methods=['GET', 'POST'])
def webcam():
    try:
        face_detect_web_obj = FaceDetectionWebcam()
        face_detect_web_obj.load_camera()
        return redirect(url_for('index'))
        
    except Exception as e:
        raise FaceDetectionException(e,sys)
    
if __name__=="__main__":
    app.run(debug=True)