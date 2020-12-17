function getRandomArbitrary(min, max) {
  return Math.random() * (max - min) + min;
}
var delayInMilliseconds = 7000; //7 seconds
var time=1;
var l2=25;  //lat
var l1=68; //lon
var radius= 6378.1;
var angle=45;
(function myLoop(i) {
  setTimeout(function() {
    var lon1=l1*(Math.PI/180);   
    var lat1=l2*(Math.PI/180);
    //var angle=Math.random(0,90);
    if(i%4==0)
    angle=getRandomArbitrary(angle,360);
    var speed=getRandomArbitrary(35000,45000)
    var distance =speed/time;
    angrad= angle * (Math.PI/180);
    //var angrad=1.57; //angle in radian
    var lat=Math.asin(Math.sin(lat1)*Math.cos(distance/radius)+Math.cos(lat1)*Math.sin(distance/radius)*Math.cos(angrad));
    var lon=lon1+Math.atan2(Math.sin(angrad)*Math.sin(distance/radius)*Math.cos(lat1),
                      Math.cos(distance/radius)-Math.sin(lat1)*Math.sin(lat));
    time+=7;          //refreshing time
    var llon=lon * (180/Math.PI);
    var llat=lat * (180/Math.PI);
    l1=llon;             
    l2=llat;
    var ang= angrad * (180/Math.PI);  //angle in degree
    console.log("<b>longitude:</b>",llon);
    console.log("<br><br>");
    console.log("<b>latitude:</b>",llat);
    console.log("<br><br>");
    console.log("<b>angle:</b>",ang);
    console.log("<br><br>");
    console.log(i);
    if (--i) myLoop(i);   //  decrement i and call myLoop again if i > 0
  }, delayInMilliseconds)
})(18); 
