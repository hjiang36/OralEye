async function checkStream(ip) {
    const url = `http://${ip}:8000`;
    const streamAvailable = await window.api.checkStream(url);
    console.log('Stream available:', streamAvailable);
    if (streamAvailable) {
        document.getElementById('stream').src = url + '/video_feed';
        document.getElementById('stream').style.display = 'block';
    } else {
        document.getElementById('stream').style.display = 'none';
    }
}

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
        checkStream(ip);
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
});
