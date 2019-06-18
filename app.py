#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

# This is the main script to run djsmile application

from flask import Flask, request, render_template, Response
from camera import Camera
from generate_joke import get_joke
import pathlib

app = Flask(__name__)


def gen(camera):
    """Yield frames returned from camera.get_frame(),
    with face bounding box and smile predictions."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    """Return index.html page with new joke."""
    return render_template('index.html', joke=get_joke())


@app.route('/video_feed')
def video_feed():
    """Return camera live feed."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=['POST'])
def update():
    """Return new index.html page with a new joke generated when button
    is clicked, and automatically scrolling to live feed section."""
    if request.form['next'] == '↻':
        return render_template('index.html', scroll='livefeed',
                               joke=get_joke())


if __name__ == '__main__':

    path = pathlib.Path('../devel_mode_on.txt')

    # developer environment
    if path.exists():
        app.run(host='127.0.0.1', debug=True, port="5000")
    # production environment
    else:
        app.run(host='0.0.0.0', debug=False, port="80")
