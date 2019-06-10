#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Response
from camera import Camera
from generate_joke import get_joke
import pathlib

app = Flask(__name__)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html', joke=get_joke())


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=['POST'])
def update():
    if request.form['next'] == '↻':
        return render_template('index.html', scroll='livefeed', joke=get_joke())


if __name__ == '__main__':
    path = pathlib.Path('../devel_mode_on.txt')
    if path.exists():
        app.run(host='127.0.0.1', debug=True, port="5000")
    else:
        app.run(host='0.0.0.0', debug=True, port="80")
