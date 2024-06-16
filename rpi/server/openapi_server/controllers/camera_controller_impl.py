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
pi_camera.start()
camera_lock = threading.Lock()

def generate():
    stream = io.BytesIO()
    output = FileOutput(stream)
    pi_camera.start_encoder(encoder, output)

    while True:
        with camera_lock:
            pi_camera.capture_file(stream, format='jpeg')
            frame = stream.getvalue()
            stream.truncate(0)
            stream.seek(0)
            yield(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def camera_preview_video_feed_get_impl():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def camera_preview_start_impl():
    # Start the mjpeg server to start streaming
    result = subprocess.run(
        ['sudo', 'systemctl', 'start', 'mJPEG.service'],
        capture_output=True, text=True)
    if result.returncode == 0:
        return {'message': f'Service started successfully'}, 200
    else:
        return {'message': f'Failed to start service', 'error': result.stderr}, 500


def camera_preview_stop_impl():
    # Stop the mjpeg server to stop streaming
    result = subprocess.run(
        ['sudo', 'systemctl', 'stop', 'mJPEG.service'],
        capture_output=True, text=True)
    if result.returncode == 0:
        return {'message': f'Service stopped successfully'}, 200
    else:
        return {'message': f'Failed to stop service', 'error': result.stderr}, 500