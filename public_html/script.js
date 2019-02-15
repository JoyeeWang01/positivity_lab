// References:
//   https://developers.google.com/maps/documentation/javascript/examples/layer-heatmap
//   https://developers.google.com/maps/documentation/javascript/reference/visualization
//   https://elfsight.com/blog/2018/06/how-to-get-google-maps-api-key-guide/
//   https://stackoverflow.com/questions/35288250/google-maps-javascript-api-referernotallowedmaperror
//   https://stackoverflow.com/questions/13785466/default-center-on-united-states
//   https://stackoverflow.com/questions/36909380/why-use-defer-with-google-maps-javascript

// Points.
var posArray = new Array(), negArray=new Array();

// Gradients.
var posGradient, negGradient;

// Maps.
var posHeatmap, negHeatmap;

// Initialize everything.
function init() {       
        initPoints();
        initGradients();
        initMap();
        initHeatMaps();
}


function initPoints() {
        // Note: data is stored in data.js.        
		
        for (var i = 0; i < data.length; i++) {
                score = data[i]["score"]
                lat = data[i]["t"]
                lng = data[i]["g"]

                point = {};
				point["location"] = new google.maps.LatLng(lat, lng);
				point["weight"] = score;
				if (score >= 0.5)
					posArray.push(point);
				else
					negArray.push(point);                           
        }
		
}

function initGradients() {
        posGradient = [
                'rgba(0, 255, 0, 0.00)',
                'rgba(0, 255, 0, 0.05)',
                'rgba(0, 255, 0, 0.10)',
                'rgba(0, 255, 0, 0.15)',
                'rgba(0, 255, 0, 0.20)',
                'rgba(0, 255, 0, 0.25)',
                'rgba(0, 255, 0, 0.30)',
                'rgba(0, 255, 0, 0.35)',
                'rgba(0, 255, 0, 0.40)',
                'rgba(0, 255, 0, 0.45)',
                'rgba(0, 255, 0, 0.50)',
                'rgba(0, 255, 0, 0.55)',
                'rgba(0, 255, 0, 0.60)',
                'rgba(0, 255, 0, 0.65)',
                'rgba(0, 255, 0, 0.70)',
                'rgba(0, 255, 0, 0.75)',
                'rgba(0, 255, 0, 0.80)',
                'rgba(0, 255, 0, 0.85)',
                'rgba(0, 255, 0, 0.90)',
                'rgba(0, 255, 0, 0.95)',
                'rgba(0, 255, 0, 1.00)',
        ]

        negGradient = [
                'rgba(255, 0, 0, 0.00)',
                'rgba(255, 0, 0, 0.05)',
                'rgba(255, 0, 0, 0.10)',
                'rgba(255, 0, 0, 0.15)',
                'rgba(255, 0, 0, 0.20)',
                'rgba(255, 0, 0, 0.25)',
                'rgba(255, 0, 0, 0.30)',
                'rgba(255, 0, 0, 0.35)',
                'rgba(255, 0, 0, 0.40)',
                'rgba(255, 0, 0, 0.45)',
                'rgba(255, 0, 0, 0.50)',
                'rgba(255, 0, 0, 0.55)',
                'rgba(255, 0, 0, 0.60)',
                'rgba(255, 0, 0, 0.65)',
                'rgba(255, 0, 0, 0.70)',
                'rgba(255, 0, 0, 0.75)',
                'rgba(255, 0, 0, 0.80)',
                'rgba(255, 0, 0, 0.85)',
                'rgba(255, 0, 0, 0.90)',
                'rgba(255, 0, 0, 0.95)',
                'rgba(255, 0, 0, 1.00)',
        ]
}

function initMap() {
var styles1 = [
    {
        "featureType": "road",
        "elementType": "labels",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "poi",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "administrative",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "weight": 1
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry.stroke",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "weight": 0.8
            }
        ]
    },
    {
        "featureType": "landscape",
        "stylers": [
            {
                "color": "#ffffff"
            }
        ]
    },
    {
        "featureType": "water",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "transit",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "elementType": "labels",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "elementType": "labels.text",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "color": "#ffffff"
            }
        ]
    },
    {
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#000000"
            }
        ]
    },
    {
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    }
];   
		

	map = new google.maps.Map(document.getElementById('map'), {
			zoom: 9,
			center: {lat: 39.284534, lng: -76.616362}, 
			styles:styles1				
	});
	;

}

function initHeatMaps() {
	posHeatmap = new google.maps.visualization.HeatmapLayer({
                data: posArray,
                map: map,
                opacity: 0.75,
                gradient: posGradient,
                radius: 90
        });

        negHeatmap = new google.maps.visualization.HeatmapLayer({
                data: negArray,
                map: map,
                opacity: 0.75,
                gradient: negGradient,
                radius: 90
        });
		posHeatmap.setMap(map);
		negHeatmap.setMap( map );        
}


function process_data(data){
	//console.log(pointsData);
	var step = 0.05;
	var start_lat = 25;
	var start_lng = -122;
	
	var rectangles = {};
	
	for (var i=0; i< pointsData.length; i++){
		var lng = pointsData[i]["g"];
		var lat =pointsData[i]["t"];
		
		var lng_units = Math.floor((lng - start_lng)/step);
		var new_lng = start_lng + lng_units * step;
		
		
		var lat_units = Math.floor((lat - start_lat)/step);
		var new_lat = start_lat + lat_units * step;
		
		//console.log("old-lat ="+lat+" new_lat ="+new_lat);
		//console.log("old-lng ="+lng+" new_lng ="+new_lng);
		var coord_key = new_lat+","+new_lng;
		
		var counts = new Array(2);
		counts[0] = 0;
		counts[1] = 0;
		if (rectangles[coord_key]!=null){
			counts[0] = rectangles[coord_key][0];
			counts[1] = rectangles[coord_key][1];		
		}
		if(pointsData[i]["p"]==1)
			counts[0]++;
		counts[1]++;
		rectangles[coord_key] = counts;
	}
	
	//console.log(rectangles);
	
	
	var new_data = [];
	for (var key in rectangles) {
		// check if the property/key is defined in the object itself, not in parent
		if (rectangles.hasOwnProperty(key)) {
			var val_arr = rectangles[key];
			//get lat long from string key
			var a = key.split(',');
			var lat = parseFloat(a[0]);
			var lng = parseFloat(a[1]);
			var score = parseFloat(val_arr[0])/parseFloat(val_arr[1]);
			var new_point = {};
			
			new_point["p"] = 2*Number((score).toFixed(2));
			new_point["t"] = lat;
			new_point["g"] = lng;
			new_data.push(new_point);
		}
	}
	//console.log(new_data);
	return new_data;		
	
}
