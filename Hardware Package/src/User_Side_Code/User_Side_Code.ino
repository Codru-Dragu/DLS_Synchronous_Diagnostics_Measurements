
// Initialise and declare variables
const int bttnPin = 12;    // The toggle button is attached to this pin - PORTC
const int startLed = 5;  // Led to indicate that the process has started - PORTD
const int stopLed = 4;    // Led to indicate that the process has not started / has stopped - PORTD
const int output = 6;     // Send the ouput trigger signal - PORTD
const int e_output = 3; // Send Emergency stop signal - PORTC

int bttnState = LOW; // Button state tracker, low if not pressed, high if pressed
int startState = -1; // Start indicator LED state tracker, negative if off, positive if on
int stopState = 1;   // Stop indicator LED state tracker, negative if off, positive if on
int triggStart = -1; // Trigger start tracker

long lastDebouncerTime = 0; // last time the output pin was toggled
long debounceDelay = 600;   // the debounce time; increase if the output flickers

int activ_period = 1000; // Length of blink


// ************************************************************

// TO BE EDITED BY USER // --> EG. collect 10 seconds of data every 20 seconds
unsigned long interval_time = 20000; // Length of time between data collection intervals // EG. 20 seconds // KEEP AT LEAST 20S (30S)
// This will be transmitted to the other arduino (to communicate via serial port)
unsigned long gate_interval = 10000; // Length of time for which the trigger on signal is held (length of time for which you want to acquire data) // EG. 10 seconds
// MODES
int mode = 1; // Choice of Mode: 0 -> One off trigger, 1 -> Conitnuous trigger

// ************************************************************


// Undeitable from other Arduino (constant - if you change it here you must also change it in the other code.)
unsigned long buffer_time = 500; // Buffer to make sure the last captures are not clipped (1.5 seconds)
unsigned long total_delay = 30.5; // This delay was determined experimentally

// Wait between blinks - uneditable 
unsigned long wait_period = (interval_time + buffer_time + total_delay + gate_interval)-activ_period;  // Pause between blinks minus the interval time (need to minus the active period as the signal is on from the active period and this only adds time (as in, the active period time is already accounted for, do not add it twice)))
unsigned long time_now = 0; // The current time

int a = 1; // Infinted while loop variable - do not edit.

// Serial Check
int did_ser = 0; // Int to check if the gate value has already been sent by serial connection
char numarr[7]; // Use 7 instead of 6 as 6 produces weird characters at the end for some reason, stores the char version of the gate signal

// Function to prepare the numarr array
void preprint(unsigned long tosplit)
{
  // Assuming the longest gate time you could possibly want was 2 minutes (120000 milisecs)
  // That is 6 digits, so send each digit as part of an array and complete the 6 available slots:
  // First, set all the numarr spaces to 0:
  numarr[0] = '0';
  numarr[1] = '0';
  numarr[2] = '0';
  numarr[3] = '0';
  numarr[4] = '0';
  numarr[5] = '0';

  // Set the count
  int count = 6;

  while (count >= 0)
  {
    if (tosplit != 0)
    {
      int digi = tosplit % 10; // Get the last digit
      char c = '0'+digi; // convert it to char - need the '0'
      numarr[count-1] = c; // add it to the end of the array
      tosplit = tosplit/10; // Divide tosplit by 10 
    }
    count = count - 1; // Decrease count until the whole array is filled with the number and leading zeroes
  }
// The numarray has been made  
}



void setup() {
  
  // Set the pin modes
  pinMode(startLed, OUTPUT); // Start LED
  pinMode(stopLed, OUTPUT);  // Stop LED
  pinMode(bttnPin, INPUT);   // Button Pin 
  pinMode(output, OUTPUT);   // Signal sender
  pinMode(e_output, OUTPUT); // Emergecy Signal Stop
 
  digitalWrite(stopLed, HIGH); // Trigger is off initially, so set the Stop LED on
  digitalWrite(e_output, HIGH); // Trigger is off initially, so set the Stop LED on

  preprint(gate_interval); // Convert the long gate_interval into a sendable char array
  Serial.begin(9600);
}

void loop() {

  // Before everything happens, check if the set up has been done or not:
  if(did_ser == 0) // the serial set up has not been done, go here:
  {
     while(!Serial.available()) // While no handshake signal is being recieved from the midbox arduino
   { // Send the gate value accross serial
      Serial.write(numarr,6);
      delay(500);
   }
   // When the handshake signal has been recieved, it breaks the loop and ends the serial connection
  Serial.end();

  // Toggle serial set up done marker
  did_ser = 1;
  }

  // After the Serial set up is done, resume normal looping 
  
  else
  {
  
  bttnState = digitalRead(bttnPin); // check button state
  //Serial.println( String( "Button input (signalState) = " ) + bttnState);
  
  // Filter out noise by setting a time buffer
  if (( millis()-lastDebouncerTime )> debounceDelay)
  {    
    // If button pressed, toggle the led indicators
    if ((bttnState == HIGH)&&(startState < 0))
    {    
      PORTD = B01100000; // Start LED High, Output High, Stop LED Low, EMergency signal low
      startState = - startState;    // Record change in LED state
      lastDebouncerTime = millis(); // Set the debouncer time
      triggStart = 1;
    }    
    
    else if ((bttnState == HIGH)&&(startState > 0))
    {    

      PORTD = B00011000; // Start LED Low, Output Low, Stop LED High, Emergency Signal High
      startState = - startState;    // Record change in LED state
      lastDebouncerTime = millis(); // Set the debouncer time
      triggStart = -1;
    }

    // If the trigger start signal is sent then start acquisition by sending the output signal
    if ((triggStart == 1))
    {
      // Get the current time
      time_now = millis();
      
      while(millis() < time_now + activ_period) // While the time is less than the active period of the LED
      {
        PORTD = B01100000; // Start LED High, Output High, Stop LED Low, EMergency signal low
        if(digitalRead(bttnPin) == 1) // Break if the button press detected (reset mode)
        {
          break;
        }       
      }
      

      // For the one-off mode specifically, once the 1 second active period is up, turn off the output signal but keep the led's on
      // The one off mode will be stopped by default (red light on) then when pressed filicker red and green and remain in the red green state wihtout sending another trigger
      // Then when pressed again, will go back to the default stopped red state. Therefore, between triggers, the button should be pressed twice- onece to reset (red mode) and then to trigger gain (red green mode)
      if(mode == 0)
      {
        while(a == 1) // infinite while loop to stop sending conitnuous signals
      {
        PORTD = B00110000; // Start LED Low, Output low, Stop LED high, Emergency Signal high
        if(digitalRead(bttnPin) == 1) // Break if button press detected (reset mode)
        {
          break;
        }  
      }
  
      }
      // For the continuous mode:
      else 
      {
        time_now = millis();
        while(millis() < time_now + wait_period) // Check if the current time is less than the waiting period or not
        {
        PORTD = B00000000; // Start LED Low, Output Low, Stop LED Low, Emergency Signal low
        if(digitalRead(bttnPin) == 1) // Break if button press detetcted (reset mode)
        {
          break;
        }  
      }
        
        
        
      }
      

      
    }
   }
 }
}
