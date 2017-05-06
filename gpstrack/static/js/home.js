var map;
tracks = {};
var iconBase = static_url + 'images/markers/';
icons = {};
colors = {};

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
    mapObject = new google.maps.Map(document.getElementById('map'), {
        center: {lat: lat, lng: lon},
        zoom: 16,
        mapTypeId: 'terrain'

    });
    icons = createIcons();
    colors = createColors();

}


function plotTrack(track) {
    var track = track;
    var points = [];
    track['points'].forEach(function (point) {
        var google_point = new google.maps.LatLng(point['location']['lat'], point['location']['lon']);
        points.unshift(
            google_point
        )
        var marker = placeMarker(google_point);
        var infoBox = createInfoBox(point, track);
        google.maps.event.addListener(marker, 'click', function () {
                infoBox.open(mapObject, marker);
                marker.setMap(mapObject);

            }
        );
        marker.setMap(mapObject);
    });
    var route = new google.maps.Polyline({
        path: points,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    route.setMap(mapObject);
}

function placeMarker(point) {
    return new google.maps.Marker({
        position: point,
        icon: icons['red_marker'],
        map: map
    });
}

function createInfoBox(point, track) {
    return new google.maps.InfoWindow({
        content: createContentString(point, track)
    });
}


function getTracks() {
    return $.getJSON({
        url: tracksListURL
    })
}

function createIcons() {
    return {
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
    }
}

function createColors() {
    return {
        black: '#000000',
        red: 'F90000',
        green: '0CB300',
        yellow: 'EFFC00',
        blue: '0004FE'
    }
}

function getPointsForTrack(trackPK) {
    return $.getJSON({
        url: tracksListURL + trackPK + '/points'
        // success: function(res, status) {
        // }
    })
}

function createContentString(point, track) {
    console.log(point);
    console.log(track);
    return `<div class="leaflet-popup-content-wrapper"><div class="leaflet-popup-content" style="width: 193px;"><div id="divPopup" class="container-fluid" style="margin:-10px; padding-right:2px; padding-left:2px; min-width:140px;">
	<div style="padding-bottom:5px; padding-left:10px;">
		<div>
			<div style="font-size:14px;overflow:hidden;text-overflow:ellipsis; white-space:nowrap">` + track.user.profile.display_name + `</div>
		</div>
		<div style="color:#999999;">
			<span style="float:left;font-size:11px;" data-bind="text:  messageDate">` + new Date(point.time.local_Time).toDateString() + `</span>
			<span style="float:right;font-size:11px;" data-bind="text: messageTime">` + new Date(point.time.local_Time).toTimeString() + `</span>
		</div>
		<div style="clear: both;"></div>
		<br>
		<div>
			<span style="font-size: 12px; overflow: hidden; text-overflow: ellipsis;word-wrap:break-word;">` + 'a message, if a message' + `</span>
			<br>
		</div>
		<div style="display: none;">
			Track Id: <span>` + track.id + `</span><br>
			Track: <span>` + track.name + `</span>
		</div>
	</div>
	<div class="row-fluid" style="padding-bottom: 10px;">
		<table>
			<tbody>
				<tr style="white-space:nowrap">
					<td>
						<span style="color:gray;font-size:11px;">Speed: <span style="white-space:nowrap;font-size:11px;color:black">` + point.velocity + ` mph</span>
					</span></td>
					<td style="padding-left:12px;">
						<span style="color:gray;font-size:11px;">Course: <span style="white-space:nowrap;font-size:11px;color:black">` + point.course + `</span>
					</span></td>
				</tr>
				<tr style="white-space:nowrap">
					<td>
						<span style="color:gray;font-size:11px;">Elevation: <span style="white-space:nowrap;font-size:11px;color:black">` + point.location.elevation + ` ft.</span>
					</span></td>
					<td style="padding-left:12px;">
						<span style="color: gray; font-size: 11px; display: none;" data-bind="visible: batt()!=''">Batt: <span style="white-space:nowrap;font-size:11px;color:black">batt??</span>
					</span></td>
				</tr>
				<tr style="white-space:nowrap">
					<td>
						<span style="color:gray;font-size:11px;">Lat: <span style="white-space:nowrap;font-size:11px;color:black">` + point.location.lat + `</span>
					</span></td>
					<td style="padding-left:12px;">
						<span style="color:gray;font-size:11px;">Lon: <span style="white-space:nowrap;font-size:11px;color:black">` + point.location.lon + `</span>
					</span></td>
				</tr>
			</tbody>
		</table>
	</div>
</div></div></div>`

}

