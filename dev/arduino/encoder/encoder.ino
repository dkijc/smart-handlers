/* Rotary encoder test code
 * Modified from http://www.circuitsathome.com/mcu/programming/reading-rotary-encoder-on-arduino by Oleg
 * Latest mod by Jessica Faruque 7/17/2013
 */
 
#include <CapacitiveSensor.h>

CapacitiveSensor   cs_4_8 = CapacitiveSensor(4,8); // 1M resistor between pins 4 & 8, pin 8 is sensor pin, add a wire and or foil 

#define ENC_A 3 //these need to be digital input pins
#define ENC_B 2
#define ENC_BUTT 5

int buttonVal,
    lastButtonState = 0;

void setup()
{
  cs_4_8.set_CS_AutocaL_Millis(0xFFFFFFFF);// turn off autocalibrate on channel 1 - just as an example
  /* Setup encoder pins as inputs */
  pinMode(ENC_A, INPUT_PULLUP);
  pinMode(ENC_B, INPUT_PULLUP);
  pinMode(ENC_BUTT, INPUT);
 
  Serial.begin (9600);
}
 
void loop()
{
  static unsigned int counter4x = 0;      //the SparkFun encoders jump by 4 states from detent to detent
  static unsigned int counter = 0;
  static unsigned int prevCounter = 0;
   
  read_butt();
    
  int tmpdata;
  tmpdata = read_encoder();
  if( tmpdata) {
    counter4x += tmpdata;
    counter = counter4x/4;
    if (prevCounter != counter){
      Serial.println(counter);
    }
    prevCounter = counter;
  }

  long sensor1 =  cs_4_8.capacitiveSensor(25);

  if (sensor1 > 0 && sensor1 > 100) {
    Serial.println("c");  // print sensor output 
    delay(100);
  }
}

void read_butt() {
  buttonVal = digitalRead(ENC_BUTT);
  if(buttonVal == LOW && lastButtonState != buttonVal) {
    Serial.println("b");
  }
  
  lastButtonState = buttonVal; 
}
 
/* returns change in encoder state (-1,0,1) */
int read_encoder()
{
  static int enc_states[] = {
    0,-1,1,0,1,0,0,-1,-1,0,0,1,0,1,-1,0  };
  static byte ABab = 0;
  ABab *= 4;                   //shift the old values over 2 bits
  ABab = ABab%16;      //keeps only bits 0-3
  ABab += 2*digitalRead(ENC_A)+digitalRead(ENC_B); //adds enc_a and enc_b values to bits 1 and 0
  return ( enc_states[ABab]);
 
 
}
