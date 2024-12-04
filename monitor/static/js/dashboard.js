async function updateStatus() {
    try {
        const response = await fetch('/status');
        const data = await response.json();

        document.getElementById('mqtt_status').innerText = data.mqtt_status;
        document.getElementById('gas').innerText = data.gas;
        document.getElementById('direction').innerText = data.direction;
        document.getElementById('steer').innerText = data.steer;
        document.getElementById('distance').innerText = data.distance.toFixed(2) + " cm";
    } catch (error) {
        console.error("Failed to fetch status:", error);
    }
}

setInterval(updateStatus, 1000); // Update setiap 1 detik
window.onload = updateStatus;
