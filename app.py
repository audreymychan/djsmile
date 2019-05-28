from flask import Flask, render_template, Response
from camera import Camera
from generate_joke import get_joke

app = Flask(__name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

joke = get_joke()

@app.route('/')
def index():
    return render_template('index.html', joke = joke)

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host = '127.0.0.1', debug = True, port = "5000")
