# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response, request, jsonify
import os
from eyecatching.readRes import *
from eyecatching.settings import *
import time
from eyecatching.camera import VideoCamera
from werkzeug.utils import secure_filename

app = Flask(__name__)

video_stream = VideoCamera()

def gen(camera):
    frame = camera.get_frame()
    yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
     return Response(gen(video_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "Only for: png / PNG / jpg / JPG/ bmp / jpeg"})

        global user_input
        user_input = request.form.get("name")

        global pointPerPlot
        pointPerPlot = request.form.get("plot_points")

        basepath = os.path.dirname(__file__)

        upload_path = os.path.join(basepath, 'static', secure_filename(f.filename))
        f.save(upload_path)

        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static', user_input), img)

        return render_template('upload_ok.html', userinput=user_input, val1=time.time())

    return render_template('upload.html')


@app.route('/plot/', methods=['POST', 'GET'])
def resPlotAll():
    plot_url = plot(user_input, pointPerPlot)
    return render_template('plot_track.html', plot_url = plot_url);
