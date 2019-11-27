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

/* B value of the thermistor */
const int B = 4275;

/* R0 = 100k */
const int R0 = 100000;

/* Grove - Temperature Sensor connect to A0 */
const int pinTempSensor = A0;

/* Holds the tempurature in Celsius */
float temp;

/**********************************************************************
 * 
 * The setup function before we go into the loop.
 * 
 *********************************************************************/
void setup() {

    Serial.begin(9600);
}

/**********************************************************************
 * 
 * The loop function that will run forever or until the arduino is
 * powered down.
 * 
 *********************************************************************/
void loop() {

    temp = getTemp();

    delay(100);
}



/**********************************************************************
 * The functions gets the tempurature from a Grove Temp Sensor v1.2.
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
