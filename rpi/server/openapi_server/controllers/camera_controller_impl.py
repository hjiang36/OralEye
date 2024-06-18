from flask import Response, send_file
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from libcamera import controls

import io
import numpy as np
import threading

pi_camera = Picamera2()

# Configuration for still capture with raw resolution
raw_resolution = (4608, 2592)
still_config = pi_camera.create_still_configuration(raw={"size": raw_resolution})

# Configuration for video streaming
video_config = pi_camera.create_video_configuration(main={"format": "RGB888", "size": (640, 480)})

# Configure as video as starting point
pi_camera.configure(video_config)

# Create encoder and output for video streaming
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
    with camera_lock:
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


def camera_autofocus_post_impl(state: str):
    if state == 'on':
        pi_camera.set_controls({'AfMode': controls.AfModeEnum.Continuous})
        return {'message': 'Auto-focus is set to on'}, 200
    elif state == 'off':
        pi_camera.set_controls({'AfMode': controls.AfModeEnum.Manual})
        return {'message': 'Auto-focus is set to off'}, 200
    
def camera_exposure_post_impl(exposure_time_us: int):
    pi_camera.set_controls({'ExposureTime': exposure_time_us})
    return {'message': 'Exposure time is set to {} us'.format(exposure_time_us)}, 200

def camera_manual_focus_post_impl(focus_distance_mm: int):
    # lens position is the diopters (reciprocal of focus distance)
    lens_position = 1000.0 / focus_distance_mm
    pi_camera.set_controls({'LensPosition': lens_position})
    return {'message': 'Focus distance is set to {} mm'.format(focus_distance_mm)}, 200

def capture_raw_bayer():
    with camera_lock:
        pi_camera.stop_encoder()  # Stop video encoder
        pi_camera.stop()
        pi_camera.configure(still_config)  # Switch to still configuration
        raw_stream = io.BytesIO()
        pi_camera.start()
        raw_buffer = pi_camera.capture_array('raw')
        np.save(raw_stream, raw_buffer)
        pi_camera.stop()
        pi_camera.configure(video_config)  # Switch back to video configuration
         # If camera was running, restart it
        if camera_running:
            pi_camera.start()
            pi_camera.start_encoder(encoder, output)  # Restart video encoder

        return raw_stream

def camera_capture_post_impl():
    try:
        raw_stream = capture_raw_bayer()
        print('Raw capture done, sending the file now')
        return send_file(raw_stream, mimetype='application/octet-stream', as_attachment=True, attachment_filename='capture.raw')
    except Exception as e:
        return {'error': str(e)}, 500