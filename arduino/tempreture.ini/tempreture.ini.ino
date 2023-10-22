#include <i2cmaster.h>

// #include <avr/io.h>

void setup(){
  Serial.begin(9600);
  Serial.println("Setup...");
  // try {
  i2c_init(); // Initialise the i2c bus
  // } catch (const std::exception &e) // caught by reference to base
  // {
  //   std::cout << " a standard exception was caught in temperatureFunction(), with message '"
  //             << e.what() << "'\n";
  //   errors[6] = 1;
  // } 
  Serial.println("I2C initialized");
  PORTD = (1 << PORTD1) | (1 << PORTD0);//enable pullups
}

void loop(){
  int device = 0x5A<<1;
  int data_low = 0;
  int data_high = 0;
  int pec = 0;

  Serial.println("Variable initialized");

  unsigned char result = i2c_start(device+I2C_WRITE);
  Serial.println(result);
  i2c_write(0x07);
  Serial.println("Writing shit");

  // read
  i2c_rep_start(device+I2C_READ);
  data_low = i2c_readAck(); //Read 1 byte and then send ack
  data_high = i2c_readAck(); //Read 1 byte and then send ack
  pec = i2c_readNak();
  i2c_stop();

  //This converts high and low bytes together and processes temperature, MSB is a error bit and is ignored for temps
  double tempFactor = 0.02; // 0.02 degrees per LSB (measurement resolution of the MLX90614)
  double tempData = 0x0000; // zero out the data
  int frac; // data past the decimal point

  // This masks off the error bit of the high byte, then moves it left 8 bits and adds the low byte.
  tempData = (double)(((data_high & 0x007F) << 8) + data_low);
  tempData = (tempData * tempFactor)-0.01;

  float celcius = tempData - 273.15;
  float fahrenheit = (celcius*1.8) + 32;

  Serial.print("Celcius: ");
  Serial.println(celcius);

  Serial.print("Fahrenheit: ");
  Serial.println(fahrenheit);

  delay(1000); // wait a second before printing again
}