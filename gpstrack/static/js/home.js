var map;
tracks = {};


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
}

function plotTrack(track) {
    var points = [];
    for (var i = 0; i < track['points'].length; i++) {
        points.unshift({
            lat: track['points'][i]['location']['lat'],
            lng: track['points'][i]['location']['lon']
        });
        var route = new google.maps.Polyline({
            path: points,
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 1.0,
            strokeWeight: 2
        });

        route.setMap(map);
    }
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