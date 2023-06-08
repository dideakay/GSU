#include <ESP8266WiFi.h>


const char* ssid = "WIFI_NAME";     // Replace with your phone's hotspot SSID
const char* password = "PASSPORT"; // Replace with your phone's hotspot password

void setup() {
  Serial.begin(115200);
  delay(10);

  // Connect to Wi-Fi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Your code here
}
