#include <CapacitiveSensor.h>

CapacitiveSensor   cs_4_8 = CapacitiveSensor(4,8); // 1M resistor between pins 4 & 8, pin 8 is sensor pin, add a wire and or foil

void setup()                    
{
   cs_4_8.set_CS_AutocaL_Millis(0xFFFFFFFF);// turn off autocalibrate on channel 1 - just as an example
   Serial.begin(9600);
}

void loop()                    
{
 long sensor1 =  cs_4_8.capacitiveSensor(50);
 if (sensor1 > 100){
   Serial.println(sensor1);  // print sensor output 
 }
   delay(100);
}
