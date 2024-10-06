
void setPixel(CRGB leds_s[],int pixel=0, int hue=0, int sat = 255, int val = 255){
leds_s[pixel]=CHSV(hue,sat,val);
}

void setPixelRGB(CRGB leds_s[],int pixel=0, int red = 0, int green = 255, int blue = 255){
    leds_s[pixel].setRGB(red,green,blue);
}



void movingTwoColors(CRGB leds_s[],int num_leds,int cycle=10,int speed=500, int numberOfLeds = 5, byte hue1 = 0, byte hue2 = 96, byte sat1 = 255, byte sat2 = 255, byte val1 = 255, byte val2 = 255){

  int currentCycle=0;
  static uint16_t pos=0;
  while(currentCycle<cycle){
    //for(int pos=0;pos<numberOfLeds*2;pos++){
      for(int i2=0;i2<num_leds;i2+=numberOfLeds*2){
        for(int i3=0;i3<numberOfLeds;i3++){
          int newPixel=i2+i3+pos;
          if(newPixel>=num_leds){
            newPixel-=num_leds;
          }
          setPixel(leds_s,newPixel,hue1,sat1,val1);
          int newPixel2=i2+i3+pos+numberOfLeds;
          if(newPixel2>=num_leds){
            newPixel2-=num_leds;
          }
          setPixel(leds_s,newPixel2,hue2,sat2,val2);
        }
      }
      pos++;
      FastLED.show();
      delay(speed);
      currentCycle++;
    //}
    if (pos==numberOfLeds*2)
    	pos=0;
  }
  
}

void solidColor(CRGB leds_s[],int num_leds,int ms = 1000, byte hue = 0,byte sat=255,byte val=255){
  
  startMillis = millis();
  while(true){
    for(int i=0;i<num_leds;i++){
      setPixel(leds_s,i,hue,sat,val);
    }
    FastLED.show();
    now = millis();
    if(now - startMillis >= ms){
      break;
    }
  }
  
}

void solidColorWithSparkle(CRGB leds_s[],int num_leds,int seconds = 5, uint8_t hue = 0, int val = 255, int speed = 10){
  
  startMillis = millis();

  for(int i=0;i<num_leds;i++){
    setPixel(leds_s,i,hue,255,val);
  }
  
  FastLED.show();
  while(true){

    int pixel = random(num_leds);
    setPixel(leds_s,pixel,0,0,255);
    FastLED.show();
    delay(speed);
    //leds[pixel] = CHSV(hue,255,val);
    setPixel(leds_s,pixel,hue,255,val);
    FastLED.show();

    now = millis();
    if(now - startMillis >= seconds*1000){
      break;
    }
  }
  
}

byte * Wheel(byte WheelPos) {
  static byte c[3];
 
  if(WheelPos < 85) {
   c[0]=WheelPos * 3;
   c[1]=255 - WheelPos * 3;
   c[2]=0;
  } else if(WheelPos < 170) {
   WheelPos -= 85;
   c[0]=255 - WheelPos * 3;
   c[1]=0;
   c[2]=WheelPos * 3;
  } else {
   WheelPos -= 170;
   c[0]=0;
   c[1]=WheelPos * 3;
   c[2]=255 - WheelPos * 3;
  }

  return c;
}

void rainbowCycle(CRGB leds_s[],int num_leds,int SpeedDelay) {
  byte *c;
  static uint16_t i=0, j=0;

  // 5 cycles of all colors on wheel
    for(i=0; i< num_leds; i++) {
      c=Wheel(((i * 256 / num_leds) + j) & 255);
      setPixelRGB(leds_s,i, *c, *(c+1), *(c+2));
    }
    FastLED.show();
    delay(SpeedDelay);
  if (i==num_leds){
  j++;
  i=0;
  }
  if (j==255)
	j=0;
	
	
}
