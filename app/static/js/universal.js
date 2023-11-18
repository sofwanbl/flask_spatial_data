var map = L.map('map').setView([51.505,-0.19],13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
{ maxZoom:19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);