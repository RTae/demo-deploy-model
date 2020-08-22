from flask import Flask, flash, request ,jsonify, render_template
from werkzeug.utils import secure_filename
from model.ML_APP import *
import json
import cv2
import os

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/')
def main():
    return 'Hello This is home page'

@application.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], 'image.png'))
            img = cv2.imread('./uploads/image.png')
            label, confident = predictImage(img)
            return jsonify({'label': label ,
                    'confident': json.dumps(str(confident))
                    })

    return render_template('upload.html')
 
if __name__ == '__main__':
    application.debug = False
    application.run()