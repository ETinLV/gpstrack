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
        console.log(track);
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

function createInfoBox(point) {
    return new google.maps.InfoWindow({
        content: createContentString(point)
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
    return `<div class="leaflet-popup-content-wrapper"><div class="leaflet-popup-content" style="width: 193px;"><div id="divPopup" class="container-fluid" style="margin:-10px; padding-right:2px; padding-left:2px; min-width:140px;">' +
	'<div style="padding-bottom:5px;">'

		<div>
			<div data-bind="text: displayName" style="font-size:14px;overflow:hidden;text-overflow:ellipsis; white-space:nowrap">` + track.user.profile.display_name + `</div>
		</div>
		<div style="color:#999999;">
			<span style="float:left;font-size:11px;" data-bind="text:  messageDate">Apr 30, 2017</span>
			<span style="float:right;font-size:11px;" data-bind="text: messageTime">3:58:48 PM</span>
		</div>


		<div style="clear: both;"></div>
		<br>

		<div data-bind="visible: function () { return message() != null &amp;&amp; message() != '' }">
			<span style="font-size: 12px; overflow: hidden; text-overflow: ellipsis;word-wrap:break-word;" data-bind="text: message"></span>
			<br>
		</div>
		<div data-bind="visible: Debug()==true" style="display: none;">
			Id: <span data-bind="text: sourcePoint().Id">0</span><br>
			Trail: <span data-bind="text: sourcePoint().T">3391051</span>
		</div>
	</div>
	<div class="row-fluid" data-bind="visible: displayMore" style="padding-bottom: 10px;">
		<table>
			<tbody>
				<tr style="white-space:nowrap">
					<td>
						<span style="color:gray;font-size:11px;">Speed: <span style="white-space:nowrap;font-size:11px;color:black" data-bind="text: speed">0.62 mph</span>
					</span></td>
					<td style="padding-left:12px;">
						<span style="color:gray;font-size:11px;">Course: <span style="white-space:nowrap;font-size:11px;color:black" data-bind="html: heading">N</span>
					</span></td>
				</tr>
				<tr style="white-space:nowrap">
					<td>
						<span style="color:gray;font-size:11px;">Elevation: <span style="white-space:nowrap;font-size:11px;color:black" data-bind="text: altitude">1,072.83 ft.</span>
					</span></td>
					<td style="padding-left:12px;">
						<span style="color: gray; font-size: 11px; display: none;" data-bind="visible: batt()!=''">Batt: <span style="white-space:nowrap;font-size:11px;color:black" data-bind="text: batt"></span>
					</span></td>
				</tr>
				<tr style="white-space:nowrap" data-bind="visible: oneCoord()==false">
					<td>
						<span style="color:gray;font-size:11px;">Lat: <span style="white-space:nowrap;font-size:11px;color:black" data-bind="text: lat">36.038754</span>
					</span></td>
					<td style="padding-left:12px;">
						<span style="color:gray;font-size:11px;">Lon: <span style="white-space:nowrap;font-size:11px;color:black" data-bind="text: lon">-114.782291</span>
					</span></td>
				</tr>
				<tr style="white-space:nowrap">
					<td colspan="2" data-bind="visible: oneCoord()==true, text: coords()[0]" style="color: gray; font-size: 11px; display: none;">36.038754</td>
				</tr>
			</tbody>
		</table>
	</div>
	<div class="row-fluid" style="text-align:center;">
		<span style="position:relative">
			<input type="image" title="Activate tracking on this user's inReach." data-bind="click: showTrackingDlg, attr: { src: trackingButtonImage }, enable: userListBtnEnabled, visible: EnableTracking(), css: { paddedBubble: displayMore() == false }" src="/content/images/Popup/Track-Big.png" class="" style="display: none;">
			<span class="popupButtonText" data-bind="visible: displayMore() &amp;&amp; EnableTracking()" style="display: none;">Track</span>
		</span>
		<span style="position:relative">
			<input type="image" title="Send a message to this user." data-bind="click: showMessageDlg, attr: { src: messageButtonImage }, enable: userListBtnEnabled, visible:EnableMessage(), css: { paddedBubble: displayMore() == false }" src="/content/images/Popup/Message-Big.png" class="">
			<span class="popupButtonText" data-bind="visible: displayMore() &amp;&amp; EnableMessage()">Message</span>
		</span>
		<span style="position:relative">
			<input type="image" title="Request the location of this user." data-bind="click: showLocateDlg, attr: { src: locateButtonImage }, enable: userListBtnEnabled, visible:EnableLocate(), css: { paddedBubble: displayMore() == false }" src="/content/images/Popup/Locate-Big.png" class="" style="display: none;">
			<span class="popupButtonText" data-bind="visible: displayMore() &amp;&amp; EnableLocate()" style="display: none;">Locate</span>
		</span>
	</div>
	<div style="text-align: center; cursor: pointer; color: inherit;" data-bind="html: (displayMore() ? '▼ LESS ▼' : '▲ MORE ▲'), click: function () { displayMore() ? displayMore(false) : displayMore(true) }, style: { color: (displayMore() ? 'inherit' : '#0080FF') }">▼ LESS ▼</div>
</div></div></div>`

}

