
// Initialise and declare variables
#define signalPin 12 // The toggle button is attached to this pin - PORTC
#define estopPin 11  // The emergency stop signal - PORTC  
#define out1 6       //  - PORTD // TET
#define out2 5       // - PORTD // TET
#define out3 4       // - PORTD // CAM

int signalState = LOW; // Button state tracker, low if not pressed, high if pressed

// To be read from the userside arduino
unsigned long gate_time; // Length of gate trigger signal that you want (how long you want to acquire data for)

// Constant delays and buffers
int buffer_time = 500; // Length of add on to gate trigger to capture last frame --> add on 2 seconds
int cam_delay = 30.5; // experimentally determined delay 

unsigned long time_now = 0; // Current time
int start_gate = -1; // Boolean to record whether this is the first start or not

unsigned long gate;

// Serial Check
char numarr[7]; // Stores the char version of the unsigned long gate_time

void setup() {
  
  // Set the pin modes
  pinMode(out1, OUTPUT); // Output to hardware (1,2 and 3)
  pinMode(out2, OUTPUT);  
  pinMode(out3, OUTPUT);   
  pinMode(signalPin, INPUT);  // Input from user side
  pinMode(estopPin, INPUT);  // Input from user side

  // All off
  PORTD = B00000000;

  // Serial start 
  Serial.begin(9600);
}

void loop() {
  
  signalState = digitalRead(signalPin); // check button state
  
  if (signalState == HIGH) // if the signal is high 
  {
    time_now = millis();
    while( millis() < (time_now + gate) )
    {
      PORTD = PORTD | B00010000;; // Start only output 3 (pin 4) --> where the camera is connected to

      if(millis()>(time_now + cam_delay))
      {
       PORTD = PORTD | B01110000; // Set all to outputs to on, using or logic to not affect the other outputs to produce a uniform square wave 
      }

      if (digitalRead(estopPin) == 1)
       {
         break;  
       }
    }

    signalState = digitalRead(signalPin); // check button state
    Serial.begin(9600);
  }
  
  if (signalState == LOW) // Keep the outputs off and listen for the Serial port
  {
       PORTD = B00000000; // All off 
       while(Serial.available()) // While there is something being sent 
       {
       int sigstate = digitalRead(signalPin); // check button state
       if(sigstate == HIGH)
       {
        Serial.end();
        break; // break the loop if the signal state is high
       }
       Serial.readBytes(numarr,6); // Read the serial data and store it
       Serial.write('1'); // Send this twice to terminate the other Arduino
       Serial.write('1'); // Send this twice to terminate the other Arduino
       gate_time = atoi(numarr);
       gate = gate_time + buffer_time + cam_delay; // total gate length, not editable
       Serial.end();
       } 
  }

}
