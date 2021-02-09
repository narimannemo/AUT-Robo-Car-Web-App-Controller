#include <ESP8266WiFi.h>
//#include <ESP8266WebServer.h>
#include <ArduinoJson.h>

 


const char *ssid = "Mohammad"; 
const char *password = "";
const char *ssid2 = "Mohammad's Iphone";
const char *pass2 = "123456aa";
String t = "";
String ip1 = "";
int i =0;
WiFiServer server(80);

  
//void mainpage()
//{
//   server.send(200,"text/html",t);
////   server.arg("plain");
////   DynamicJasonBuffer jBuffer;
////   JasonObject& jObject = jBuffer.parsObject(data);
////   String ch = jObject["/s"];
////   Serial.println(ch);
//   Serial.println("w");
//
//};




void setup() {
  pinMode(LED_BUILTIN,OUTPUT);
	Serial.begin(115200);
	//Serial.println();
	//Serial.print("connecting to ");
  //Serial.print(ssid);
  WiFi.begin(ssid2, pass2);
  WiFi.begin(ssid, password); 
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    //Serial.print(".");
  };
  //Serial.println();
  //Serial.println("wifi connected");
  IPAddress ip =WiFi.localIP();
  
  ip1=String(ip[0])+".";
  ip1+=String(ip[1])+".";
  ip1+=String(ip[2])+".";
  ip1+=String(ip[3]);
  //texSerial.println(ip1);
  String a = "";
    a +="<!DOCTYPE html>\n";
  a +="<html>\n";
  a +="<head>\n";
  a +="    <title>Robot Navigation</title>\n";
  a +="    <link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css\" integrity=\"sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB\" crossorigin=\"anonymous\">\n";
  a +="    <link rel=\"stylesheet\" href=\"http://drive.google.com/uc?export=download&id=11IUqgh4O3E2dkZ9-Twi3n3N7hd3O-IZ6\">\n";
  a +="    <link href=\"https://fonts.googleapis.com/css?family=IBM+Plex+Mono:300\" rel=\"stylesheet\">\n";
  a +="    <link href=\"https://fonts.googleapis.com/css?family=Caveat|Permanent+Marker\" rel=\"stylesheet\">\n";
  a +="</head>\n";
  a +="<body>\n";
  a +="<div class=\"row\">\n";
  a +="     <div class=\"col-lg-4\">\n";   
  a +="   <ul id=\"adidas\">\n";
  a +="        <li></li>\n";
  a +="        <li></li>\n";
  a +="       <li></li>\n";       
  a +="   </ul>\n";
  a +="    </div>\n";  
  a +="    <div class=\"col-lg-4\">\n";
  a +="        <h1 class=\"tm\">FORZA TEAMMELLI!</h1>\n";
  a +="    </div>\n";    
  a +="<div class=\"col-lg-4\">\n";
  a +="    </div>\n";
  a +="    </div>\n";
  a +="<div class=\"row\">\n";
  a +="  <div class=\"col-lg-3\">\n";  
  a +="    </div>\n";    
  a +="    <div class=\"col-lg-3\" align=\"center\">\n";
  a +="    <h3 class=\"speed\">LEFT MOTOR SPEED</h3>\n";
  a +="        <canvas width=\"380\" height=\"250\" id=\"foo\"></canvas>\n";
  a +="        <h3 id=\"lm\" class=\"speed text-center\">left</h3>\n";    
  a +="    </div>\n";
  a +="  <div class=\"col-lg-3 \" align=\"center\">\n";
  a +="    <h3  class=\"speed\">RIGHT MOTOR SPEED</h3>\n";
  a +="      <canvas width=\"380\" height=\"250\" id=\"boo\"></canvas>\n";
  a +="      <h3 id=\"rm\" class=\"speed text-center\">right</h3>\n";
  a +="    </div>\n";
  a +="</div>\n";    
  a +="<div class=\"row\">\n";
  a +="    <div class=\"col-lg-4\"></div>\n";
  a +="    <div class=\"col-lg-4\">\n";
  a +="        <form>\n";
  a +="        <ul id=\"keyboard\">\n";
  a +="            <li id=\"w\" class=\"letterW\">W</li>\n";
  a +="            <li id=\"a\" class=\"letter\">A</li>\n";
  a +="            <li id=\"s\" class=\"letter\">S</li>\n";
  a +="           <li id=\"d\" class=\"letter\">D</li>\n";
  a +="    </ul>\n";
  a +="    </form>\n"; 
  a +="    </div>\n";
  a +="    <div class=\"col-lg-4\"></div>\n";  
  a +="</div>\n";    
  a +="<script type=\"text/javascript\" src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js\"></script>\n";
  a +="<script type=\"text/javascript\" src=\"/keyboard.js\"></script>\n";
  a +="<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js\"></script>\n";
  a +="<script type=\"text/javascript\">\n";
  a +="window.onload = function() {\n";
  a +="  document.getElementById(\"w\").onclick = function() {\n";
  a +=" $.post(\"http://";
  a += ip1;
  a += ":80\",\"/w\\n\", function(response){\n";
  a += "var lines = response.split('t');\n";
  a += "$('#lm').html(lines[0]);\n";
  a += "$('#rm').html(lines[1]);\n";
  a +=" gauge.set(lines[0]);\n";
  a +=" gaugeR.set(lines[1]);\n";
  a +=" });\n";
  a +=" event.preventDefault();\n";
  a +="}\n";
  a +=" document.getElementById(\"a\").onclick = function() {\n";
  a +=" $.post(\"http://";
  a += ip1;
  a += ":80\",\"/a\\n\", function(response){\n";
  a += "var lines = response.split('t');\n";
  a += "$('#lm').html(lines[0]);\n";
  a += "$('#rm').html(lines[1]);\n";
  a +=" gauge.set(lines[0]);\n";
  a +=" gaugeR.set(lines[1]);\n";
  a +=" });\n";
  a +=" event.preventDefault();\n";
  a +="}\n";
  a +=" document.getElementById(\"s\").onclick = function() {\n";
  a +=" $.post(\"http://";
  a += ip1;
  a += ":80\",\"/s\\n\", function(response){\n";
  a += "var lines = response.split('t');\n";
  a += "$('#lm').html(lines[0]);\n";
  a += "$('#rm').html(lines[1]);\n";
  a +=" gauge.set(lines[0]);\n";
  a +=" gaugeR.set(lines[1]);\n";
  a +=" });\n";
  a +="event.preventDefault();\n";
  a +="}\n";
  a +=" document.getElementById(\"d\").onclick = function() {\n";
  a +=" $.post(\"http://";
  a += ip1;
  a += ":80\",\"/d\\n\", function(response){\n";
  a += "var lines = response.split('t');\n";
  a += "$('#lm').html(lines[0]);\n";
  a += "$('#rm').html(lines[1]);\n";
  a +=" gauge.set(lines[0]);\n";
  a +=" gaugeR.set(lines[1]);\n";
  a +=" });\n";
  a +=" event.preventDefault();\n";
  a +="}\n";
  a +="    };\n";
  a +="</script>\n";
  a +="<!--\n";
  a +="//function uniKeyCode(event) {\n";
  a +="//    var key = event.keyCode;\n";
  a +="//    if (key === 37|| key === 38 ||key === 39 ||key === 40){\n";
  a +="//    document.getElementById(\"w\").innerHTML =\"&uarr;\" ;\n";
  a +="//    document.getElementById(\"a\").innerHTML =\"&larr;\" ;\n";
  a +="//    document.getElementById(\"s\").innerHTML =\"&darr;\" ;\n";
  a +="//    document.getElementById(\"d\").innerHTML =\"&rarr;\" ;\n";
  a +="//    }\n";
  a +="//}\n";
  a +="-->\n";
  a +="<script src=\"http://bernii.github.io/gauge.js/dist/gauge.js\"></script>\n";  
  a +="<script type=\"text/javascript\" >\n";
  a +="var opts = {\n";
  a +="  angle: -0.2, // The span of the gauge arc\n";
  a +="  lineWidth: 0.2, // The line thickness\n";
  a +="  radiusScale: 1, // Relative radius\n";
  a +="  pointer: {\n";
  a +="    length: 0.6, // // Relative to gauge radius\n";
  a +="    strokeWidth: 0.05, // The thickness\n";
  a +="    color: '#000000' // Fill color\n";
  a +="  },\n";
  a +="  limitMax: false,     // If false, max value increases automatically if value > maxValue\n";
  a +="  limitMin: false,     // If true, the min value of the gauge will be fixed\n";
  a +=" generateGradient: true,\n";
  a +="  highDpiSupport: true,     // High resolution support\n";
  a +="staticZones: [ \n";
  a +="   {strokeStyle: \"#cc0000\", min: -200, max: -180},\n";
  a +="  {strokeStyle: \"#FFFFFF\", min: -180, max: 180},\n";
  a +="   {strokeStyle: \"#cb7d00\", min: 155, max: 162},\n";
  a +="   {strokeStyle: \"#cb7d00\", min: -162, max: -155},\n";
  a +="   {strokeStyle: \"#cb3700\", min: -178, max: -165},\n";
  a +="   {strokeStyle: \"#000000\", min: -101, max: -100},\n";  
  a +="   {strokeStyle: \"#000000\", min: 100, max: 101 },\n";
  a +="   {strokeStyle: \"#000000\", min: -151, max: -150},\n";    
  a +="   {strokeStyle: \"#000000\", min: 150, max: 151 },\n";
  a +="   {strokeStyle: \"#000000\", min: -51, max: -50},\n";   
  a +="   {strokeStyle: \"#000000\", min: 50, max: 51 },\n";     
  a +="   {strokeStyle: \"#cb3700\", min: 165, max: 178},\n";    
  a +="   {strokeStyle: \"#cc0000\", min: 180, max: 200}  // Red\n";
  a +="],\n";
  a +="staticLabels: {\n";
  a +="  font: \"20px 'IBM Plex Mono', monospace\",  // Specifies font\n";
  a +="  labels: [-200,-100,-50,50,100,200],  // Print labels at these values\n";
  a +=" color: \"#000000\",  // Optional: Label text color\n";
  a +="  fractionDigits: 0  // Optional: Numerical precision. 0=round off.\n";
  a +="}\n";
  a +="};\n";   
  a +="var lm=document.getElementById(\"lm\").innerHTML;\n";    
  a +="var target = document.getElementById('foo');\n";
  a +="var gauge = new Gauge(target).setOptions(opts);\n";
  a +="gauge.maxValue = 200;\n";
  a +="gauge.setMinValue(-200);\n";
  a +="gauge.animationSpeed = 32;\n";
  a +="gauge.set(0);\n";
  a +="var rm=document.getElementById(\"rm\").innerHTML;\n";   
  a +="var target = document.getElementById('boo');\n";
  a +="var gaugeR = new Gauge(target).setOptions(opts);\n";
  a +="gaugeR.maxValue = 200;\n";
  a +="gaugeR.setMinValue(-200);\n";
  a +="gaugeR.animationSpeed = 32;\n";
  a +="gaugeR.set(0);\n";
  a +="    </script>\n";   
  a +="</body>\n";
  a +="</html>\n";      
  a +="</script>\n";    
  a +="</body>\n";
  a +="</html>\n";

  t=a;
	server.begin();
  Serial.println(ip1);
}

void loop() {
//  server.handleClient();
  WiFiClient client = server.available();  
  if (!client) 
  {
      return;
  };

  while (!client.available()) 
  {
    delay(1);
  };
  String req = client.readStringUntil('\r');
  if(req.indexOf("GET / HTTP/1.1")!=-1)
  {
      client.print(t);
  };

  if (req.indexOf("POST") != -1) 
  {
    digitalWrite(LED_BUILTIN,!digitalRead(LED_BUILTIN));
    while (client.available())
    {
      req = client.readStringUntil('\n');
    };
  };

   if(req.indexOf("/w")!=-1)
  {
    String left = "0t";
    String right = "0t";
    Serial.println("w");
    left = Serial.readStringUntil('t');
    left += "t";
    right = Serial.readStringUntil('t');
    right += "t" ;
    client.println(left+right);
  }
  else if(req.indexOf("/a")!=-1)
  {
    String left = "0t";
    String right = "0t";
    Serial.println("a");
    left = Serial.readStringUntil('t');
    left += "t";
    right = Serial.readStringUntil('t');
    right += "t" ; 
    client.print(left+right);
  }
  else if(req.indexOf("/s")!=-1)
  {
    String left = "0t";
    String right = "0t";
    Serial.println("s");
    left = Serial.readStringUntil('t');
    left += "t";
    right = Serial.readStringUntil('t');
    right += "t";  
    client.print(left+right);
  }
  else if(req.indexOf("/d")!=-1)
  {
    String left = "0t";
    String right = "0t";
    Serial.println("d");
    left = Serial.readStringUntil('t');
    left += "t";
    right = Serial.readStringUntil('t');
    right += "t";  
    client.print(left+right);
  }
  else if(req.indexOf("/e")!=-1)
  {
    String left = "0t";
    String right = "0t";
    Serial.println("h");
    left = Serial.readStringUntil('t');
    left += "t";
    right = Serial.readStringUntil('t');
    right += "t" ; 
    client.print(left+right);
  };
  client.flush();



  //delay(1);
  //Serial.println("Client disconnected");
}
