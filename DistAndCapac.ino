#include "Adafruit_VL53L0X.h"
#include <CapacitiveSensor.h>

CapacitiveSensor   cs_4_8 = CapacitiveSensor(4,8);

Adafruit_VL53L0X lox = Adafruit_VL53L0X();

void setup() {
  Serial.begin(9600);
  cs_4_8.set_CS_AutocaL_Millis(0xFFFFFFFF);
  // wait until serial port opens for native USB devices
  while (! Serial) {
    delay(1);
  }
  
  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while(1);
  }
  // power 

}


void loop() {
  long sensor1 =  cs_4_8.capacitiveSensor(50);
  VL53L0X_RangingMeasurementData_t measure;

  lox.rangingTest(&measure, false); // pass in 'true' to get debug data printout!

  if (measure.RangeStatus != 4) {  // phase failures have incorrect data
    if (measure.RangeMilliMeter < 800) {
      Serial.println(measure.RangeMilliMeter);
    }
  } 
  if (sensor1 > 100){
    Serial.println(sensor1);
  }
  delay(100);
}
