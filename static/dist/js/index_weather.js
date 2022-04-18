$.getJSON('http://api.openweathermap.org/data/2.5/forecast?id=1835848&APPID=f8b8761c25df03a84389bdbb6a97a6c5&units=metric'
,function(data){
// var $minTemp = data.list[0].main.temp_min;
// var $maxTemp = data.list[0].main.temp_max;
var $temp = data.list[0].main.temp;
var $temp1 = data.list[0].main.temp;
var $temp2 = data.list[0].main.temp;
var $temp3 = data.list[0].main.temp;
var $humidity = data.list[0].main.humidity;
var $type = data.list[0].weather[0].description;
var $sky = data.list[0].weather[0].main;
var $probability = data.list[0].clouds.all;
var $probability1 = data.list[0].clouds.all;
var $windspeed = data.list[0].wind.speed;

if($type == "Clouds")
$type = "구름";
else if($type == "Rain")
$type = "비";
else
$type = "맑음";

// $('.clowtemp').append($minTemp + "°C");
// $('.chightemp').append($maxTemp + "°C");
$('.temp').append($temp + "°C");
$('.chumidity').append($humidity + "%");
$('.csky').append($sky);
$('.ctype').append($type);
$('.cprobability').append($probability + "%");	
$('.windspeed').append($windspeed + "m/s");

if($temp1 < 10)
$temp1 = "추운날씨 따뜻하게 해주세요";
else if($temp1 > 20)
$temp1 = "더운날씨! 관리가 필요해요!";
else
$temp1 = "좋은 온도입니다!";

if($temp2 < 10)
$temp2 = "추운날씨 따뜻하게 해주세요";
else if($temp2 > 15)
$temp2 = "더운날씨! 관리가 필요해요!";
else
$temp2 = "좋은 온도입니다!";

if($temp3 < 18)
$temp3 = "추운날씨 따뜻하게 해주세요";
else if($temp3 > 24)
$temp3 = "더운날씨! 관리가 필요해요!";
else
$temp3 = "좋은 온도입니다!";

if($probability1 >= 80)
$probability1 = "비오는 날! 수분관리가 필요해요!";
else if($probability1 > 40)
$probability1 = "흐린날! 일조량 관리에 유의해주세요!";
else
$probability1 = "맑은 날! 햇볕을 많이 쬐게 해주세요!";

$('.temp1').append($temp1);
$('.temp2').append($temp2);
$('.temp3').append($temp3);
$('.probability1').append($probability1);


});