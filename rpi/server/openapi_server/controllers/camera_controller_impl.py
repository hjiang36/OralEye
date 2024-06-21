from flask import Response, send_file
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from libcamera import controls
from PIL import Image

import io
import json
import numpy as np
import threading
import uuid

from openapi_server.controllers.lights_controller_impl import set_light_status

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
    # Turn on the red laser in preview mode
    set_light_status(red_laser='on')

    # Start the mjpeg server to start streaming
    global camera_running
    if camera_running:
        return {'message': 'Camera preview is already running'}, 200
    with camera_lock:
        pi_camera.start()
        pi_camera.start_encoder(encoder, output)
        camera_running = True


def camera_preview_stop_impl():
    # Turn off all the lights
    set_light_status(white_led='off', blue_led='off', red_laser='off')

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

def save_raw(raw_buffer: np.ndarray, output_file: str, metadata: dict):
    # Save raw image
    # TODO: save the raw image to standard EXR format with metadata
    bytes_buffer = raw_buffer.tobytes()
    with open(output_file + '.raw', 'wb') as f:
        f.write(bytes_buffer)
    
    # Save metadata
    with open(output_file + '.json', 'w') as f:
        f.write(json.dumps(metadata))
    return raw_buffer

def generate_thumbnail(raw_buffer: np.ndarray, thumbnail_size):
    b = raw_buffer[::2, ::5]
    g = raw_buffer[1::2, ::5]
    r = raw_buffer[::2, 1::5]

    # Create an image
    img = np.zeros((r.shape[0], r.shape[1], 3), dtype=np.uint8)
    img[:, :, 2] = b
    img[:, :, 1] = g
    img[:, :, 0] = r

    # Convert to PIL image and resize to target size
    pil_img = Image.fromarray(img)
    pil_img.resize(thumbnail_size)
    return pil_img

def capture_raw_squence():
    with camera_lock:
        # Stop camera so that we can swtich to still configuration
        pi_camera.stop_encoder()
        pi_camera.stop()
        pi_camera.configure(still_config)

        # Start camera
        pi_camera.start()
        job_id = str(uuid.uuid4())

        # Set lighting to room light
        set_light_status(white_led='off', blue_led='off', red_laser='off')
        raw_buffer = pi_camera.capture_array('raw')
        metadata = pi_camera.capture_metadata()
        ambient_img = save_raw(raw_buffer, '/tmp/raw_capture_' + job_id + '_ambient', metadata)

        # Set lighting to white LED
        set_light_status(white_led='on', blue_led='off')
        raw_buffer = pi_camera.capture_array('raw')
        metadata = pi_camera.capture_metadata()
        white_img = save_raw(raw_buffer, '/tmp/raw_capture_' + job_id + '_white', metadata)

        # Set lighting to blue LED
        set_light_status(white_led='off', blue_led='on')
        raw_buffer = pi_camera.capture_array('raw')
        set_light_status(blue_led='off')  # Turn off blue LED as soon as possible
        metadata = pi_camera.capture_metadata()
        blue_img = save_raw(raw_buffer, '/tmp/raw_capture_' + job_id + '_blue', metadata)

        # Generate thumbnail
        thumbnail_width = 256
        thumbnail_height = int(thumbnail_width * raw_resolution[1] / raw_resolution[0])
        size = (thumbnail_width, thumbnail_height)
        thumbnail_ambient = generate_thumbnail(ambient_img, size)
        thumbnail_white = generate_thumbnail(white_img, size)
        thumbnail_blue = generate_thumbnail(blue_img, size)

        # Stitch the thumbnails together and save to file
        thumbnail = Image.new('RGB', (thumbnail_width, thumbnail_height * 3))
        thumbnail.paste(thumbnail_ambient, (0, 0))
        thumbnail.paste(thumbnail_white, (0, thumbnail_height))
        thumbnail.paste(thumbnail_blue, (0, thumbnail_height * 2))
        thumbnail.save('/tmp/raw_capture_' + job_id + '_thumbnail.jpg')

        # Switch back to video configuration
        pi_camera.stop()
        pi_camera.configure(video_config)

         # If camera was running, restart it
        if camera_running:
            pi_camera.start()
            pi_camera.start_encoder(encoder, output)
            set_light_status(red_laser='on')

        # Return the job id
        return job_id

def camera_capture_post_impl():
    try:
        # Capture the raw sequence
        job_id = capture_raw_squence()

        # Return the generated thumbnail image
        return send_file(
            '/tmp/raw_capture_' + job_id + '_thumbnail.jpg',
            mimetype='application/octet-stream',
            as_attachment=True,
            attachment_filename=job_id + '.jpg')
    except Exception as e:
        print(str(e))
        return {'error': str(e)}, 500