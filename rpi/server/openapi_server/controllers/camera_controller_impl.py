import subprocess

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