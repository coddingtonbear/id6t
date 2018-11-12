
const map = new google.maps.Map(
    document.getElementById("map"),
    {
        zoom: 10,
        disableDefaultUI: true,
        mapTypeId: 'hybrid',
        center: {lat: 45.5122, lng: -122.6587}
    }
)
var marker = null;

function updateStatistics(data) {
    if(data.position) {
        if(marker) {
            marker.setMap(null);
        }
        const position = new google.maps.LatLng(data.position[0], data.position[1])
        marker = new google.maps.Marker({
            position: position,
            map: map,
        })
        map.setCenter(position);
    }
    if(data['power.battery_voltage']) {
        document.getElementById('battery-voltage').innerHTML = data['power.battery_voltage'] + ' V';
    }
    if(data['power.current_amps']) {
        document.getElementById('current-consumption').innerHTML = data['power.current_amps'] + ' A';
    }
    if(data['led.enabled']) {
        document.getElementById('led-lighting').innerHTML = "ON"
    } else {
        document.getElementById('led-lighting').innerHTML = "OFF"
    }
    if(data['velocity']) {
        document.getElementById('velocity').innerHTML = data['velocity'] + ' mph'
    }
}

const events = new EventSource("/events/")
events.onmessage = (evt) => {
    updateStatistics(JSON.parse(evt.data))
}

const state = JSON.parse(JSON.parse(document.getElementById('maxwell-state').innerHTML))
updateStatistics(state)
