import subprocess
from flask import Response
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

import io
import threading

pi_camera = Picamera2()
pi_camera.configure(pi_camera.create_video_configuration(main={"format": "RGB888", "size": (640, 480)}))
encoder = JpegEncoder(q=80)
stream = io.BytesIO()
output = FileOutput(stream)

camera_lock = threading.Lock()
camera_running = False


def generate():
    while True:
        if not camera_running:
            break
        with camera_lock:
            pi_camera.capture_file(stream, format='jpeg')
            frame = stream.getvalue()
            stream.truncate(0)
            stream.seek(0)
            yield(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def camera_preview_video_feed_get_impl():
    # Check if the camera is running
    if not camera_running:
        # TOOD: we may convert this to return an error image instead of 404
        return {'message': 'Camera preview is not running'}, 404
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def camera_preview_start_impl():
    # Start the mjpeg server to start streaming
    global camera_running
    if camera_running:
        return {'message': 'Camera preview is already running'}, 200
    with camera_lock:
        pi_camera.start()
        pi_camera.start_encoder(encoder, output)
        camera_running = True


def camera_preview_stop_impl():
    # Stop the mjpeg server to stop streaming
    global camera_running
    if not camera_running:
        return {'message': 'Camera preview is not running'}, 200
    with camera_lock:
        pi_camera.stop_encoder()
        pi_camera.stop()
        camera_running = False
    