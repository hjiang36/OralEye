function setLightStatus(ip) {
    const lightStatus = {
        white_led: document.getElementById('white-led-toggle').checked ? 'on' : 'off',
        blue_led: document.getElementById('blue-led-toggle').checked ? 'on' : 'off',
        red_laser: document.getElementById('laser-toggle').checked ? 'on' : 'off',
    };
    console.log('Setting light status:', lightStatus);
    console.log('Set light IP:', ip);
    window.api.setLightStatus(ip, lightStatus);
}

document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const ip = urlParams.get('ip');

    if (ip) {
        document.getElementById('source-ip').innerHTML = ip;
    } else {
        document.getElementById('source-ip').innerHTML = 'No IP provided';
    }

    try {
        const lightStatus = await window.api.getLightStatus(ip);
        document.getElementById('white-led-toggle').checked = lightStatus.white_led === 'on';
        document.getElementById('blue-led-toggle').checked = lightStatus.blue_led === 'on';
        document.getElementById('laser-toggle').checked = lightStatus.red_laser === 'on';
    } catch (error) {
        console.error('Error fetching light status:', error);
    }

    // Toggling lights
    document.getElementById('white-led-toggle').addEventListener('click', () => {
        setLightStatus(ip);
    });

    document.getElementById('blue-led-toggle').addEventListener('click', () => {
        setLightStatus(ip);
    });

    document.getElementById('laser-toggle').addEventListener('click', () => {
        setLightStatus(ip);
    });

    // Start / stop streaming
    document.getElementById('streaming-toggle').addEventListener('click', () => {
        const streamStatus = document.getElementById('streaming-toggle').checked;
        window.api.setStreamingStatus(ip, streamStatus);
        
        // Wait and check the stream status again
        if (streamStatus) {
            const url = `http://${ip}:8080/camera/preview/video_feed`;
            document.getElementById('source-ip').innerHTML = ip + ", starting stream...";
            setTimeout(() => {
                document.getElementById('source-ip').innerHTML = ip;
                document.getElementById('stream').src = url + '?ts=' + new Date().getTime();
                document.getElementById('stream').style.display = 'block';
            }, 200);
        } else {
            // Hide the preview immediately
            document.getElementById('stream').src = '';
            document.getElementById('stream').style.display = 'none';
        }
    });

    // Capture image
    document.getElementById('capture-button').addEventListener('click', async () => {
        const outputPath = await window.api.captureRawImage(ip);
        console.log('Captured image:', outputPath);
        if (!outputPath) {
            document.getElementById('capture-info').innerHTML = "Failed to capture image";
        } else {
            document.getElementById('capture-info').innerHTML = "Saved to: " + outputPath;
        }
    });
});
