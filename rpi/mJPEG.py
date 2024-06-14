
#!/usr/bin/python3
from flask import Flask, Response
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

import time
import io


app = Flask(__name__)
pi_camera = Picamera2()
pi_camera.configure(pi_camera.create_video_configuration(main={"format": "RGB888", "size": (640, 480)}))
encoder = JpegEncoder()
pi_camera.start()

@app.route('/')
def index():
    return '<html><body><img src="/video_feed"></body></html>'

def generate():
    encoder = JpegEncoder(q=80)
    stream = io.BytesIO()
    output = FileOutput(stream)
    pi_camera.start_encoder(encoder, output)

    while True:
        pi_camera.capture_file(stream, format='jpeg')
        frame = stream.getvalue()
        stream.truncate(0)
        stream.seek(0)
        yield(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
