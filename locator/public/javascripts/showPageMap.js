mapboxgl.accessToken = 'pk.eyJ1IjoiY29kZWhhY2tlcm9uZSIsImEiOiJja2g0ZG5mMWMwdjd3MndwY3h1MjJ0NDdkIn0.5kZ-Uc9FYE7nlN1vHtP6Qg';
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/satellite-streets-v11', // stylesheet location
    center: [longitude, latitude], // starting position [lng, lat]
    zoom: 10 // starting zoom
});
map.addControl(new mapboxgl.NavigationControl());
new mapboxgl.Marker()
    .setLngLat([longitude, latitude])
    .setPopup(
        new mapboxgl.Popup({ offset: 25 })
        .setHTML(
            `Your location`
        )
    )
    .addTo(map)