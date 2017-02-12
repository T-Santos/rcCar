/*
  rcCarReceiver
    This program receives 4 char hex c strings and converts them to decimal commands to 
    then be sent to digital pins. The digital pins are then set to HIGH and connect to the 
    external hardware sending a signal
 */
 
int input = 13;  // Pin 13 has an LED connected on most Arduino boards. Used for visual output
int fwd = 12;    // Pin set for forward signal
int rev = 11;    // Pin set for reverse signal
int left = 10;   // Pin set for turn left signal
int right = 9;   // Pin set for turn right signal

char inString[4];      // c string input to capture 0x00 - 0x0A range
long int command = 0;  // converted input to long

// the setup routine runs once when you press reset:
void setup() {                
  
  // opens serial port, sets data rate to 9600 bps
  Serial.begin(9600);
  
  // initialize the digital pin as an output.
  pinMode(input, OUTPUT);  
  pinMode(fwd, OUTPUT);  
  pinMode(rev, OUTPUT);
  pinMode(left, OUTPUT);  
  pinMode(right, OUTPUT);
}

// set all pins to no output
void myStop(){
  digitalWrite(input,LOW);
  digitalWrite(fwd,LOW);
  digitalWrite(rev,LOW);
  digitalWrite(left,LOW);
  digitalWrite(right,LOW);
}

// set forward and "input received" pin to output
void forward(){
  digitalWrite(input,HIGH);
  digitalWrite(fwd,HIGH);
}

// set reverse and "input received" pin to output
void reverse(){
  digitalWrite(input,HIGH);
  digitalWrite(rev,HIGH);
}

// set left "input received" pin to output
void Left(){
  digitalWrite(input,HIGH);
  digitalWrite(left,HIGH);
}

// set right and "input received" pin to output
void Right(){
  digitalWrite(input,HIGH);
  digitalWrite(right,HIGH);
}

// Purpose: Take the input command and cause the respective pins
//          to emit a signal
// Args: Long Command - integer input to trigger certain actions
void callCommand(long command){
  
  // stop all pior signals
  myStop();
 
 // Receive new signal
  switch(command){
    case 0:
      myStop();
      break;
    case 1: 
      Right();
      break;
    case 2:
      Left();
      break;
    case 4:
      reverse();
      break;
    case 5:
      reverse();
      Right();
      break;
    case 6:
      reverse();
      Left();
      break;
    case 8:
      forward();
      break;
    case 9:
      forward();
      Right();
      break;
    case 10:
      forward();
      Left();
      break;
    default:
      myStop();
  }
}
  
// the loop routine runs over and over again forever:
void loop(){

        // receive data:
        if (Serial.available() > 0) {
                
                // read in 4 byte chunks
                // Args in hex format in range 0x00 - 0x0A 
                Serial.readBytes(inString,4);
                
                // convert hex string to base 16 integer
                command = strtol(inString,NULL,16);
                Serial.print("I received: ");
                Serial.println(command);
                Serial.println(command,DEC);
                Serial.println(command,HEX);
                Serial.println("------");
                callCommand(command);
        }
}
