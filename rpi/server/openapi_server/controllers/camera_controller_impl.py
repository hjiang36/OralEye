from flask import Flask, request, jsonify
from picamera2 import Picamera2, exc  # Handle potential camera exceptions

app = Flask(__name__)

# Flag to track camera state (True: on, False: off)
camera_on = False
pi_camera = None  # Initialize camera object as None initially

def start_camera():
  global camera_on, pi_camera
  if not camera_on:
    pi_camera = Picamera2()
    pi_camera.configure(pi_camera.create_video_configuration(main={"format": "RGB888", "size": (640, 480)}))
    pi_camera.start()
    camera_on = True

def stop_camera():
  global camera_on, pi_camera
  if camera_on:
    if pi_camera:
      pi_camera.stop()
      pi_camera = None
    camera_on = False

@app.route('/start_camera', methods=['POST'])
def start_camera_api():
  try:
    start_camera()
    return jsonify({'message': 'Camera started successfully!'})
  except exc.CameraError as e:
    # Handle camera errors gracefully
    return jsonify({'error': f'Camera error: {e}'}), 500

@app.route('/stop_camera', methods=['POST'])
def stop_camera_api():
  stop_camera()
  return jsonify({'message': 'Camera stopped successfully!'})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)  # You can change the port as needed