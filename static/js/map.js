let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 13,
  });
  map.setCenter(new google.maps.LatLng(18.58190845985503, 73.84872037451504));
  
}