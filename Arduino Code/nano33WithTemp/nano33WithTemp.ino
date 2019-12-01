/**********************************************************************
 * This program runs the Nano 33 IoT with a Grove - Temp Sensor v1.2.
 * The point of this program is to gather temp and send it to a
 * server to be read by a client (both of which will be built with
 * python).
 * 
 * Authors: Denver DeBoer
 *          Nicholas English
 *          Kevin Smith
 * File: nano33WithTemp.ino
 * Assignment: Project 3
 * Due Date: December 4, 2019
 *********************************************************************/


#include <math.h>
#include <stdio.h>
#include <SPI.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>

/********** Temp Sensor Values **********/

/* B value of the thermistor */
const int B = 4275;

/* R0 = 100k */
const int R0 = 100000;

/* Grove - Temperature Sensor connect to A0 */
const int pinTempSensor = A0;

/* Holds the tempurature in Celsius */
float temp;


/********** WiFi Values **********/

int status = WL_IDLE_STATUS;

char ssid[] = /* REDACTED */;   // REMEMBER TO REMOVE PERSONAL INFO BEFORE PUSH
char pass[] = /* REDACTED */;   // !!!

unsigned int localPort = 2390;

/* A string to send to the server. */
char MessageBuffer[] = "";

WiFiUDP Udp;


/**********************************************************************
 * 
 * The setup function before we go into the loop.
 * 
 *********************************************************************/
void setup() {

    /* Used to initialize the serial and wait for a port to open. */
    Serial.begin(9600);


    /* Check for the WiFi module. */
    if (WiFi.status() == WL_NO_MODULE) {
      
      Serial.println("Communication with WiFi module failed!");

      /* Then do NOT continue. */
      while (true);
    }


    /* Check the firmware version. */
    String fv = WiFi.firmwareVersion();
    
    if (fv < WIFI_FIRMWARE_LATEST_VERSION)
      Serial.println("Please upgrade the firmware");


    /* We attempt to connect to the WiFi network. */
    while (status != WL_CONNECTED) {
      Serial.print("Attempting to connect to SSID: ");
      Serial.println(ssid);
      
      // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
      status = WiFi.begin(ssid, pass);
  
      /* We wait 10 seconds for a connection. */
      Serial.println("Connecting to wifi...");
      delay(10000);
    }



    Serial.println("Connected to wifi!\n");
    printWifiStatus();
  
    Serial.println("\nStarting transmission to server...");
    Udp.begin(localPort);
    
}

/**********************************************************************
 * 
 * The loop function that will run forever or until the arduino is
 * powered down.
 * 
 *********************************************************************/
void loop() {

    /* Get the current temp from the sensor with 2 decimal places. */
    temp = getTemp();
    sprintf(MessageBuffer, "%.2f", temp);

    
    /* Send a message to the computer with the server. */
    IPAddress destinationIP( /* REDACTED */ );  // Address of target machine  (Private IP)
    unsigned int destinationPort = 10000;      // Port to send to
    
    Udp.beginPacket(destinationIP, destinationPort);

    Udp.write(MessageBuffer);
    Udp.endPacket();


    /* Delay between loops. */
    delay(1000);
}



/**********************************************************************
 * The function gets the tempurature from a Grove Temp Sensor v1.2.
 * The function was provided by Seeed, the creator of the sensor.
 * 
 * http://wiki.seeedstudio.com/Grove-Temperature_Sensor_V1.2/
 *********************************************************************/
float getTemp() {

    int a = analogRead(pinTempSensor);

    float R = 1023.0/a-1.0;
    R = R0*R;

    float temp = 1.0/(log(R/R0)/B+1/298.15)-273.15; // convert to temperature via datasheet

    Serial.print("Temperature = ");
    Serial.print(temp);
    Serial.println(" *C");

    return temp;
  
}



/**********************************************************************
 * The function prints the WiFi status that the Nano connected to.
 * The function was provided by Arduino.
 * 
 * https://www.arduino.cc/en/Tutorial/WiFiNINAWiFiUdpSendReceiveString
 *********************************************************************/
void printWifiStatus() {
    // print the SSID of the network you're attached to:
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());
  
    // print your board's IP address:
    IPAddress ip = WiFi.localIP();
    Serial.print("IP Address: ");
    Serial.println(ip);
  
    // print the received signal strength:
    long rssi = WiFi.RSSI();
    Serial.print("signal strength (RSSI):");
    Serial.print(rssi);
    Serial.println(" dBm");
}
