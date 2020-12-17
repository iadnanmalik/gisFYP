
function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
  }
var map = L.map("map").setView([30.3753, 69.3451], 5);

var greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 43],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [-50, 50 ]
  });
defenceIcon= new L.icon({
    iconUrl: 'badge.png',
        iconSize: [25, 34]
    });
planeIcon= new L.icon({
        iconUrl: 'plane.png',
            iconSize: [25, 27]
        });
var osm = L.tileLayer(
"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
{
    attribution:
    "&copy; <a href='https://openstreetmap.org/copyright'> Openstreet map</a> contributors",
}
);

var Dark_layer = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
	maxZoom: 20,
	attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
});
var Watercolor = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}', {
	attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	subdomains: 'abcd',
	minZoom: 1,
	maxZoom: 16,
	ext: 'jpg'
});

var WorldStreetMap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
	attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
});

osm.addTo(map)
var baseLayers ={
    "Default":osm,
    "Dark layer":Dark_layer,
    "water color": Watercolor,
    "street map": WorldStreetMap
};

var marker=L.marker([33.6844,73.0479],{
    draggable : true,
    title: "This is Islamabad",
    opacity:1.0,
    icon: defenceIcon

}).addTo(map).bindPopup("<h1> Islmabad </h1> <p> This is the information about the marker </p>");
var markerSargodha=L.marker([32.0455,72.6716],{
        draggable : true,
        title: "Sargodha Air base",
        opacity:1.0,
        icon: defenceIcon
             
    }).addTo(map).bindPopup("<h1> Sargodha Air base </h1> <p> This is the information about the marker </p>");
    var geoJson=L.geoJSON(pakData,{
            onEachFeature: function(feature, layer){
                var district= feature.properties.NAME_2;
                var province= feature.properties.NAME_1;
                var city= feature.properties.NAME_3;
                var name= city + ", "+district+", "+ province;
                layer.bindPopup(`District: ${city}, Division: ${district}, Province: ${province}`);
            }
            ,
        
        style:{
            color: "green", 
            fillOpacity: 0,
            weight: 2.0,
        }
    } 
        ).addTo(map);


//var myMovingMarker = L.Marker.movingMarker([[33.6844,73.0479],[30.6844,75.0479]],
  //  [20000],{icon:planeIcon,
    //    rotationAngle:125
    
    //}).addTo(map);
//...
//myMovingMarker.start();

function getNextLatLong(l2,l1,angrad,distance,){
    var lon1=l1*(Math.PI/180);   
    var lat1=l2*(Math.PI/180);
   
    var lat=Math.asin(Math.sin(lat1)*Math.cos(distance/radius)+Math.cos(lat1)*Math.sin(distance/radius)*Math.cos(angrad));
    var lon=lon1+Math.atan2(Math.sin(angrad)*Math.sin(distance/radius)*Math.cos(lat1),
                      Math.cos(distance/radius)-Math.sin(lat1)*Math.sin(lat));
              //refreshing time
    var llon=lon * (180/Math.PI);
    var llat=lat * (180/Math.PI);
    return {
        llat:llat,
        llon:llon
    };
    
};
var delayInMilliseconds = 7000; //7 seconds
  var time=1;
  var consttime=7
  var l2=31.3260;  //lat
  var l1=75.7652; //lon
  var secondl2=32.6675;
  var secondl1=69.8597
  var radius= 6378.1;
  var angle=260;
  var secondangle=45;
  var markerInLoop= {};
  var secondmarkerInLoop={};

  (function myLoop(i) {
    setTimeout(function() {
      //var angle=Math.random(0,90);
      if(i%3==0){
      angle1=getRandomArbitrary(angle,360);
        angle2=getRandomArbitrary(0,angle);
        angle=angle1+angle2;
        angle=angle/2
        secondangle1=getRandomArbitrary(secondangle,360);
        secondangle2=getRandomArbitrary(0,secondangle);
        secondangle=secondangle1+secondangle2;
        secondangle=secondangle/2
        
    }
      var speed=getRandomArbitrary(350,450)

      var distance =speed/consttime;
      angrad= angle * (Math.PI/180);
      secondangrad= secondangle * (Math.PI/180);
         
      //var angrad=1.57; //angle in radian
        var newCords= getNextLatLong(l2,l1,angrad,distance);
        var secondnewCords=getNextLatLong(secondl2,secondl1,secondangrad,distance);
        time+=7;
      map.removeLayer(markerInLoop);
      markerInLoop=L.Marker.movingMarker([[l2,l1],[newCords.llat,newCords.llon]],
        [7000],{icon:planeIcon,
            rotationAngle:angle
        
        }).addTo(map);
    map.removeLayer(secondmarkerInLoop);
    secondmarkerInLoop=L.Marker.movingMarker([[secondl2,secondl1],[secondnewCords.llat,secondnewCords.llon]],
        [7000],{icon:planeIcon,
            rotationAngle:secondangle 
        }).addTo(map);
    
    //...
    markerInLoop.start();
    secondmarkerInLoop.start();
    l1=newCords.llon;             
    l2=newCords.llat;
    secondl1=secondnewCords.llon;
    secondl2=secondnewCords.llat;
        
    console.log("<b>longitude:</b>",l2);
      console.log("<br><br>");
      console.log("<b>latitude:</b>",l1);
      console.log("<br><br>");
      console.log("<b>angle:</b>",angle);
      console.log("<br><br>");
      console.log(i);
      if(i==1){
        map.removeLayer(markerInLoop);
        map.removeLayer(secondmarkerInLoop);
      }
      if (--i) myLoop(i);   //  decrement i and call myLoop again if i > 0
    }, delayInMilliseconds)
  })(11); 
  
var overLayers= {
    Islamabad:marker,
    "Sargodha Base": markerSargodha,
    "Pakistan's Districts": geoJson,
}
L.control.layers(baseLayers,overLayers).addTo(map);

//map.removeLayer(myMovingMarker1);

  