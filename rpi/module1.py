from flask import Flask, Response
from picamera import PiCamera
import time

app = Flask(__name__)
camera = PiCamera()

@app.route('/')
def index():
    return '<html><body><img src="/video_feed"></body></html>'

def generate():
    camera.start_preview()
    time.sleep(2)  # Give the camera some time to warm up
    try:
        while True:
            camera.capture('image.jpg', format='jpeg')
            with open('image.jpg', 'rb') as f:
                frame = f.read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)  # Adjust this delay as needed
    finally:
        camera.stop_preview()

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)