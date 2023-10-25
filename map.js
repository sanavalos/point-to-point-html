var map = L.map('map', {
 center: [-38.030786, -59.72168],
 zoom: 6
});

var tiles = new L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
 attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
maxZoom: '15'}).addTo(map);

const locations = [{coordinates: [-34.603824, -58.450012], text: 'Shop 1'},
{coordinates: [-34.932104, -57.951508], text: 'Shop 2'},
{coordinates: [-37.999409, -57.573853], text: 'Shop 3'},
{coordinates: [-38.733732, -62.259521], text: 'Shop 4'},]

for (let i = 0; i < locations.length; i++) {
    L.marker(locations[i].coordinates,{ 
     title: "TITLE",
     opacity: 0.75
    }).addTo(map).bindPopup(locations[i].text);
}

