#include "AA_MCP2515.h"
#include <SPI.h>  
#include "FastLED.h"

#define LED_SIGNAL_PIN1 5 //entrance
#define LED_SIGNAL_PIN2 6 //nagy átjáro
#define LED_SIGNAL_PIN3 7 //plafon

#define MOTION_SENSOR_PIN 8
#define RADAR_SENSOR_PIN A1
#define LED_ADDRESS1 0x121
#define LED_ADDRESS2 0x122
#define LED_ADDRESS3 0x123
#define MOTION_SENSOR 0x124
#define LIGHT_SENSOR_ADDRESS 0x125
#define LIGHT_SENSOR_PIN A0
const unsigned char PS_pin = 3, second_relay_pin = 4, LED_count1 = 140;
const unsigned int LED_count2 = 280;  //280
const unsigned int LED_count3 = 200;
unsigned long start_off_millis1 = millis(), start_on_millis1 = millis(),light_sensor_next_time=millis();
unsigned long start_off_millis2 = millis(), start_on_millis2 = millis();
unsigned long start_on_millis3 = millis(),start_off_millis3= millis(), now = millis();
unsigned long volatile can_watchdog = millis();
unsigned char volatile last_sent_can_data_led1[]={0,0,0,0,0,0,0,0},last_sent_can_data_led2[]={0,0,0,0,0,0,0,0},last_sent_can_data_led3[]={0,0,0,0,0,0,0,0};
unsigned char volatile last_sent_can_data_motion_sensor[]={0,0,0,0,0,0,0,0},last_sent_can_data_light_sensor[]={0,0,0,0,0,0,0,0};

const CANBitrate::Config CAN_BITRATE = CANBitrate::Config_16MHz_250kbps;
const uint8_t CAN_PIN_CS = 10;
const int8_t CAN_PIN_INT = 2;

CANConfig config(CAN_BITRATE, CAN_PIN_CS, CAN_PIN_INT);
CANController CAN(config);



void onWakeup(CANController& controller) {
  controller.setMode(CANController::Mode::Normal);
}

#define LED_TYPE WS2812B
#define COLOR_ORDER RGB


CRGB leds1[LED_count1];
CRGB leds2[LED_count2];
CRGB leds3[LED_count3];
// system timer, incremented by one every time through the main loop

unsigned char r1 = 0,g1 = 0,b1 = 0, r2 = 0,g2 = 0,b2 = 0,r3 = 0,g3 = 0,b3 = 0;
unsigned char r1_act = 0, g1_act = 0,b1_act = 0,r2_act = 0,g2_act = 0,b2_act=0,r3_act = 0,g3_act = 0, b3_act = 0;
unsigned char trans1=20,trans2=20,trans3=20;
unsigned char pattern1=0,pattern2=0,pattern3=0;
unsigned char volatile order1=0,order2=0,order3=0;
unsigned char m1 = 0;  //motion sensor
boolean volatile can_bus_error_exists = false;
boolean led1_on=false,led2_on=false,led3_on=false ;
boolean volatile null_message1 = true, null_message2 = true, null_message3 = true, null_message4 = true, null_message5 = true;
boolean volatile new_order1 = false, new_order2 = false, new_order3 = false;

unsigned long last_motion = millis();
unsigned long startMillis;
#include "xmas.h"

  


void onReceive(CANController&, CANFrame frame) {
 //frame.print("RX");

  // received a packet
 




  
    unsigned long canId = frame.getId();
    //Serial.println(canId);
    can_watchdog = now;
    can_bus_error_exists = false;



    if (canId == LED_ADDRESS1) {
      //frame.print("be");
      
      null_message1 = true;
      //last_sent_can_data_led1[i]=frame.getData();
      const uint8_t *tdata = frame.getData();
  const uint8_t dlc = frame.getDlc();
  for (uint8_t i = 0; i<dlc; i++) {
    //out.print("0x"); out.print(*(data++), HEX); out.print(" ");
    last_sent_can_data_led1[i]=*(tdata++);
   if (last_sent_can_data_led1[i]>0)
      null_message1 = false;
  }
            
            
      
      if (!null_message1) {

        new_order1 = true;
      }
}
     else if (canId == LED_ADDRESS2) {   
      //frame.print("be");
     
      null_message2 = true;
      //last_sent_can_data_led1[i]=frame.getData();
      const uint8_t *tdata = frame.getData();
  const uint8_t dlc = frame.getDlc();
  for (uint8_t i = 0; i<dlc; i++) {
    //out.print("0x"); out.print(*(data++), HEX); out.print(" ");
    last_sent_can_data_led2[i]=*(tdata++);
   if (last_sent_can_data_led2[i]>0)
      null_message2 = false;
  }
    
      
      if (!null_message2) {

        new_order2 = true;
      }
}
      else if (canId == LED_ADDRESS3) {   
        //frame.print("be");
     
      null_message3 = true;
      //last_sent_can_data_led1[i]=frame.getData();
      const uint8_t *tdata = frame.getData();
  const uint8_t dlc = frame.getDlc();
  for (uint8_t i = 0; i<dlc; i++) {
    //out.print("0x"); out.print(*(data++), HEX); out.print(" ");
    last_sent_can_data_led3[i]=*(tdata++);
   if (last_sent_can_data_led3[i]>0)
      null_message3 = false;
  }
    
      
      if (!null_message3) {

        new_order3 = true;
      }
    
    }    else if (canId == LIGHT_SENSOR_ADDRESS) {
      
      null_message4 = true;
      
    }

     // }
      }






void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);
  pinMode(PS_pin, OUTPUT);
  pinMode(second_relay_pin, OUTPUT);
  pinMode(MOTION_SENSOR_PIN, INPUT);
  pinMode(LIGHT_SENSOR_PIN, INPUT);
  pinMode(RADAR_SENSOR_PIN, INPUT);
  digitalWrite(PS_pin, LOW);
  //FastLED.setMaxRefreshRate(0);
  // initialize the random number generator with a seed obtained by
  // summing the voltages on the disconnected analog inputs
  FastLED.addLeds<LED_TYPE, LED_SIGNAL_PIN1, COLOR_ORDER>(leds1, LED_count1);
  FastLED.addLeds<LED_TYPE, LED_SIGNAL_PIN2, COLOR_ORDER>(leds2, LED_count2);
  FastLED.addLeds<LED_TYPE, LED_SIGNAL_PIN3, COLOR_ORDER>(leds3, LED_count3);

  Serial.println("MCP2515 Receiver Callback test!");
 
 while(CAN.begin(CANController::Mode::Normal) != CANController::OK) {
    Serial.println("CAN begin FAIL - delaying for 1 second");
    delay(1000);
  }
  Serial.println("CAN begin OK");
  
  CAN.setInterruptCallbacks(&onReceive, &onWakeup);

  
 const int addresses [] = {0x121,0x122,0x123};
 //adatkeres
for (int address : addresses) {
  uint8_t can_data[] = { 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
  
       CANFrame frame(address, can_data, sizeof(can_data));
      CAN.write(frame);
      delay(100);
      }
}

int cansend(unsigned long canId,uint8_t  can_data[8]){
      
      CANFrame frame(canId, can_data, 16);
      CAN.write(frame);
      //frame.print("CAN TX");
      
     
      return 1;
  }



void loop() {
  
  now = millis();
  //Serial.println(digitalRead(MOTION_SENSOR));
  if (null_message1)
    null_message1 = !cansend(LED_ADDRESS1, last_sent_can_data_led1);

  if (null_message2)
    null_message2 = !cansend(LED_ADDRESS2, last_sent_can_data_led2);

  if (null_message3)
    null_message3 = !cansend(LED_ADDRESS3, last_sent_can_data_led3);
  if (null_message4) {
    //map(analogRead(LIGHT_SENSOR_PIN), 0, 1023, 0, 255)
    last_sent_can_data_light_sensor[0]=1;
    last_sent_can_data_light_sensor[1] = char(map(analogRead(LIGHT_SENSOR_PIN), 0, 1023, 0, 100));
    null_message4 = !cansend(LIGHT_SENSOR_ADDRESS, last_sent_can_data_light_sensor);
  }

  if (new_order1) {
    order1 = last_sent_can_data_led1[0];  //2:be, 4: ki, 6:
    r1 = last_sent_can_data_led1[1];
    g1 = last_sent_can_data_led1[2];
    b1 = last_sent_can_data_led1[3];
    trans1 = last_sent_can_data_led1[4];
    pattern1 = last_sent_can_data_led1[5];
    last_sent_can_data_led1[0] = last_sent_can_data_led1[0] + 1;

   
    new_order1 = !cansend(LED_ADDRESS1, last_sent_can_data_led1);
  }

  if (new_order2) {
    order2 = last_sent_can_data_led2[0];  //2:be, 4: ki, 6:
    r2 = last_sent_can_data_led2[1];
    g2 = last_sent_can_data_led2[2];
    b2 = last_sent_can_data_led2[3];
    trans2 = last_sent_can_data_led2[4];
     pattern2 = last_sent_can_data_led2[5];
    last_sent_can_data_led2[0] = last_sent_can_data_led2[0] + 1;

    new_order2 = !cansend(LED_ADDRESS2, last_sent_can_data_led2);
  }
  if (new_order3) {
    order3 = last_sent_can_data_led3[0];  //2:be, 4: ki, 6:
    r3 = last_sent_can_data_led3[1];
    g3 = last_sent_can_data_led3[2];
    b3 = last_sent_can_data_led3[3];
    trans3 = last_sent_can_data_led3[4];
    pattern3 = last_sent_can_data_led3[5];
    last_sent_can_data_led3[0] = last_sent_can_data_led3[0] + 1;

   
    new_order3 = !cansend(LED_ADDRESS3, last_sent_can_data_led3);
  }


  if (digitalRead(MOTION_SENSOR_PIN) == 1 || digitalRead(RADAR_SENSOR_PIN) == 1) {
   

    if (last_motion + 5000 < now) {
      //Serial.println("motion");
      //unsigned char stmp[8] = {1,0,0,0,0,0,0x00,0x00};
      //CAN.sendMsgBuf(MOTION_SENSOR, 0, 8, stmp);
      last_motion = now;
      last_sent_can_data_motion_sensor[0]=1;
      last_sent_can_data_motion_sensor[1]=1;
      for (int i=1;i<7;i++)
        last_sent_can_data_motion_sensor[i]=0;
    
      cansend(MOTION_SENSOR, last_sent_can_data_motion_sensor);          
    }
  }

//Serial.println(analogRead(LIGHT_SENSOR_PIN));
/*
  if (now > light_sensor_next_time && map(round(analogRead(LIGHT_SENSOR_PIN) / 100) * 100, 0, 1023, 0, 255) != last_sent_can_data_light_sensor[1]) {
    last_sent_can_data_light_sensor[0]=1;
    last_sent_can_data_light_sensor[1] = map(round(analogRead(LIGHT_SENSOR_PIN) / 100) * 100, 0, 1023, 0, 255);
    cansend(LIGHT_SENSOR_ADDRESS, last_sent_can_data_light_sensor);
    light_sensor_next_time = now + 10000;
  }
*/
  if (led1_on || led2_on || led3_on){
    //Serial.println("PS ON");
    digitalWrite(PS_pin, HIGH);
  }
  else{ 
    //Serial.println("PS OFF");
    digitalWrite(PS_pin, LOW);
  }
  if (pattern1==0 && order1 == 2 && (r1 != r1_act || g1 != g1_act || b1 != b1_act) && start_on_millis1 + trans1 < now) {
    led1_on=true;
    if (r1 - r1_act > 2)
      r1_act += 2;
    else
      r1_act = r1;

    if (g1 - g1_act > 2)
      g1_act += 2;
    else
      g1_act = g1;

    if (b1 - b1_act > 2)
      b1_act += 2;
    else
      b1_act = b1;

    fill_solid(leds1, LED_count1, CRGB(r1_act, g1_act, b1_act));
       
    start_on_millis1 = now;
  }

  if (pattern2==0 && order2 == 2 && (r2 != r2_act || g2 != g2_act || b2 != b2_act) && start_on_millis2 + trans2 < now) {
   led2_on=true;
    if (r2 - r2_act > 2)
      r2_act += 2;
    else
      r2_act = r2;

    if (g2 - g2_act > 2)
      g2_act += 2;
    else
      g2_act = g2;

    if (b2 - b2_act > 2)
      b2_act += 2;
    else
      b2_act = b2;

    fill_solid(leds2, LED_count2, CRGB(r2_act, g2_act, b2_act));
    
    start_on_millis2 = now;
  }


if (pattern3==0 && order3 == 2 && (r3 != r3_act || g3 != g3_act || b3 != b3_act) && start_on_millis3 + trans3 < now) {
    led3_on=true;
    if (r3 - r3_act > 2)
      r3_act += 2;
    else
      r3_act = r3;

    if (g3 - g3_act > 2)
      g3_act += 2;
    else
      g3_act = g3;

    if (b3 - b3_act > 2)
      b3_act += 2;
    else
      b3_act = b3;

    fill_solid(leds3, LED_count3, CRGB(r3_act, g3_act, b3_act));
    
    start_on_millis3 = now;
  }


  if (order1 == 4 && start_off_millis1 + trans1*10 < now) {
    //Serial.print("OFF");
    if (r1_act > 6)
      r1_act -= 6;
    if (g1_act > 6)
      g1_act -= 6;
    if (b1_act > 5)
      b1_act -= 5;
    fill_solid(leds1, LED_count1, CRGB(r1_act, g1_act, b1_act));

    start_off_millis1 = now;
    if (r1_act<=6 && g1_act<=6 && b1_act<=5) {
      r1_act = 0, g1_act = 0, b1_act = 0;
      led1_on=false;
      fill_solid(leds1, LED_count1, CRGB(0, 0, 0));
    }
  }

  if (order2 == 4 && start_off_millis2 + trans2*10 < now) {
    //Serial.print("OFF");
    if (r2_act > 6)
      r2_act -= 6;
    if (g2_act > 6)
      g2_act -= 6;
    if (b2_act > 5)
      b2_act -= 5;
    fill_solid(leds2, LED_count2, CRGB(r2_act, g2_act, b2_act));

    start_off_millis2 = now;
    if (r2_act<=6 && g2_act<=6 && b2_act<=5) {
      r2_act = 0, g2_act = 0, b2_act = 0;
      led2_on=false;
      fill_solid(leds2, LED_count2, CRGB(0, 0, 0));
    }
  }

  if (order3 == 4 && start_off_millis3 + trans3*10 < now) {
    //Serial.print("OFF");
    if (r3_act > 6)
      r3_act -= 6;
    if (g3_act > 6)
      g3_act -= 6;
    if (b3_act > 5)
      b3_act -= 5;
    fill_solid(leds3, LED_count3, CRGB(r3_act, g3_act, b3_act));

    start_off_millis3 = now;
    if (r3_act<=6 && g3_act<=6 && b3_act<=5) {
      r3_act = 0, g3_act = 0, b3_act = 0;
      led3_on=false;
      fill_solid(leds3, LED_count3, CRGB(0, 0, 0));
    }
  }
  
  if (pattern1 > 0) {
    if (pattern1 == 1)
      rainbowCycle(leds1, LED_count1, 1);
    else if (pattern1 == 2)
      movingTwoColors(leds1, LED_count1, 10, 0, 10, 0, 110, 255, 255, 255, 255);
    else if (pattern1 == 3)
      solidColor(leds1, LED_count1, 1000, 96);
    else if (pattern1 == 4)
      solidColor(leds1, LED_count1, 1000, 128);
    else if (pattern1 == 5)
      solidColor(leds1, LED_count1, 1000, 192);
    else if (pattern1 == 6)
      solidColorWithSparkle(leds1, LED_count1, 5, 0, 255, 10);
  }
  if (pattern2 > 0) {
    if (pattern2 == 1)
      rainbowCycle(leds2, LED_count2, 1);
    else if (pattern2 == 2)
      movingTwoColors(leds2, LED_count2, 10, 0, 10, 0, 110, 255, 255, 255, 255);
    else if (pattern2 == 3)
      solidColor(leds2, LED_count2, 1000, 96);
    else if (pattern2 == 4)
      solidColor(leds2, LED_count2, 1000, 128);
    else if (pattern2 == 5)
      solidColor(leds2, LED_count2, 1000, 0);

    else if (leds2, LED_count2, pattern2 == 6)
      solidColorWithSparkle(leds2, LED_count2, 5, 0, 255, 10);

  }   
if (pattern3 > 0) {
    if (pattern3 == 1)
      rainbowCycle(leds3, LED_count3, 1);
    else if (pattern3 == 2)
      movingTwoColors(leds3, LED_count3, 10, 0, 10, 0, 110, 255, 255, 255, 255);
    else if (pattern3 == 3)
      solidColor(leds3, LED_count3, 1000, 96);
    else if (pattern3 == 4)
      solidColor(leds3, LED_count3, 1000, 128);
    else if (pattern3 == 5)
      solidColor(leds3, LED_count3, 1000, 0);

    else if (leds3, LED_count3, pattern3 == 6)
      solidColorWithSparkle(leds3, LED_count3, 5, 0, 255, 10);

  }   

  

  else if (can_bus_error_exists == false && now - can_watchdog > 60000) {  // there is no active CAN bus
    Serial.println("CAN BUS error");
    fill_solid(leds1, LED_count1, CRGB(100, 100, 100));
    //delay(1000);

    can_bus_error_exists = true;
  }else
  can_bus_error_exists = false;

  
  FastLED.delay(0);
  FastLED.show();
}
