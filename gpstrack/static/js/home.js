var map;
tracks = {};
var iconBase = static_url + 'images/markers/';
icons = {};

function init() {
    getTracks().done(function (res, status) {
        tracks = res;
        firstTrack = tracks[0]['points'];
        initMap(
            firstTrack[firstTrack.length - 1]['location']['lat'],
            firstTrack[firstTrack.length - 1]['location']['lon'])
    }).done(function () {
        for (var i = 1; i < tracks.length; i++) {
            plotTrack(tracks[i])
        }
    })
}


function initMap(lat, lon) {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: lat, lng: lon},
        zoom: 16,
        mapTypeId: 'terrain'

    });

    icons = {
        black_marker: {
            url: iconBase + 'marker_black.png',
            scaledSize: new google.maps.Size(6, 6),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(3, 3)
        },
        red_marker: {
            url: iconBase + 'marker_red.png',
            scaledSize: new google.maps.Size(6, 6),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(3, 3)
        },
        green_marker: {
            url: iconBase + 'marker_green.png',
            scaledSize: new google.maps.Size(6, 6),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(3, 3)
        },
        yellow_marker: {
            url: iconBase + 'marker_yellow.png',
            scaledSize: new google.maps.Size(6, 6),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(3, 3)
        },
        blue_marker: {
            url: iconBase + 'marker_blue.png',
            scaledSize: new google.maps.Size(6, 6),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(3, 3)
        }
    };



}

function plotTrack(track) {
    var points = [];

    track['points'].forEach(function (point) {
            points.unshift(
                new google.maps.LatLng(point['location']['lat'], point['location']['lon'])
                // lat: point['location']['lat'],
                // lng: point['location']['lon']
            )
        }
    );
    var route = new google.maps.Polyline({
        path: points,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });

    points.forEach(function (point) {
        // var latLong = new google.maps.LatLng(,)
        var marker = new google.maps.Marker({
            position: point,
            icon: icons['red_marker'],
            map: map
        });
        marker.setMap(map);
    });
    route.setMap(map);
}


function getTracks() {
    return $.getJSON({
        url: tracksListURL
    })
}

function getPointsForTrack(trackPK) {
    return $.getJSON({
        url: tracksListURL + trackPK + '/points'
        // success: function(res, status) {
        // }
    })
}