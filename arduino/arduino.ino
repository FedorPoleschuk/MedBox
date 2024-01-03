#include <i2cmaster.h>
#include <Wire.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"

// pOxiMetr
MAX30105 particleSensor;
#define MAX_BRIGHTNESS 255
uint32_t irBuffer[100];   //infrared LED sensor data
uint32_t redBuffer[100];  //red LED sensor data
int32_t bufferLength;     //data length
int32_t spo2;             //SPO2 value
int8_t validSPO2;         //indicator to show if the SPO2 calculation is valid
int32_t heartRate;        //heart rate value
int8_t validHeartRate;    //indicator to show if the heart rate calculation is valid
boolean firstTime = true;
byte pulseLED = 11;  //Must be on PWM pin
byte readLED = 13;   //Blinks with each data read

void setup() {
  Serial.begin(500000);  // Инициализация порта Serial с скоростью 9600 бод

  // temperatureMetr
  i2c_init();  // Initialise the i2c bus
  // PORTD = (1 << PORTD1) | (1 << PORTD0); // enable pullups

  // pOxiMetr
  pinMode(pulseLED, OUTPUT);
  pinMode(readLED, OUTPUT);
  particleSensor.begin(Wire, I2C_SPEED_FAST);
  byte ledBrightness = 60;                                                                        //Options: 0=Off to 255=50mA
  byte sampleAverage = 4;                                                                         //Options: 1, 2, 4, 8, 16, 32
  byte ledMode = 2;                                                                               //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  byte sampleRate = 100;                                                                          //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
  int pulseWidth = 411;                                                                           //Options: 69, 118, 215, 411
  int adcRange = 4096;                                                                            //Options: 2048, 4096, 8192, 16384
  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);  //Configure sensor with these settings

  pinMode(10, INPUT);  // Setup for leads off detection LO +
  pinMode(9, INPUT);   // Setup for leads off detection LO -
}

int TMP = 0;

void loop() {
  int str;
  static String inputBuffer = "";  // Буфер для сбора входных данных
  static bool newDataAvailable =
    false;  // Флаг для обозначения наличия новых данных

  // Проверка наличия новых данных
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      newDataAvailable =
        true;  // Установить флаг новых данных, если найден символ новой строки
    } else {
      str = c;
      str -= 48;  // Добавить символ к буферу
    }
  }

  if (newDataAvailable) {
    // Если есть новые данные, обработайте их
    processSerialData(str);
    // Очистите буфер и сбросьте флаг новых данных
    inputBuffer = "";
    newDataAvailable = false;
  }

  // Здесь вы можете выполнять свои функции без блокировки чтения из Serial
  int command = inputBuffer.toInt();
  switch (TMP) {
    case 1:
      firstTime = true;
      function1();
      break;
    case 2:
      firstTime = true;
      camOtoscope();
      break;
    case 3:
      pOxyMetr();
      break;
    case 4:
      firstTime = true;
      electroCardioGram();
      break;
    case 5:
      firstTime = true;
      function5();
      break;
    case 6:
      firstTime = true;
      temperatureMetr();
      break;
    case 7:
      firstTime = true;
      function7();
      break;
    default:
      firstTime = true;
      Serial.println(0);
      // Обработка некорректных команд, если необходимо
      break;
  }
  delay(300);
  // Добавьте другие функции по мере необходимости
}

void processSerialData(int data) {
  // Разбор и обработка входных данных из Serial
  int command = data;

  // Выполните действия в зависимости от команды
  switch (command) {
    case 1:
      firstTime = true;
      function1();
      break;
    case 2:
      firstTime = true;
      camOtoscope();
      break;
    case 3:

      pOxyMetr();
      break;
    case 4:
      firstTime = true;
      electroCardioGram();
      break;
    case 5:
      firstTime = true;
      function5();
      break;
    case 6:
      firstTime = true;
      temperatureMetr();
      break;
    case 7:
      firstTime = true;
      function7();
      break;
    default:
      firstTime = true;
      // Обработка некорректных команд, если необходимо
      break;
  }
}

void function1() {
  // Реализация функции 1
  Serial.println(1);
  TMP = 1;

  // Добавьте код функции 1 здесь
}

void camOtoscope() {
  // Реализация функции 2
  Serial.println(2);
  TMP = 2;

  // Добавьте код функции 2 здесь
}

void pOxyMetr() {
  // Реализация функции 3
  if (firstTime) {
    bufferLength = 100;  //buffer length of 100 stores 4 seconds of samples running at 25sps
    for (byte i = 0; i < bufferLength; i++) {
      while (particleSensor.available() == false)  //do we have new data?
        particleSensor.check();                    //Check the sensor for new data
      Serial.println(0);
      redBuffer[i] = particleSensor.getRed();
      irBuffer[i] = particleSensor.getIR();
      particleSensor.nextSample();  //We're finished with this sample so move to next sample
    }
    maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
    firstTime = false;
  }
  //dumping the first 25 sets of samples in the memory and shift the last 75 sets of samples to the top
  for (byte i = 25; i < 100; i++) {
    redBuffer[i - 25] = redBuffer[i];
    irBuffer[i - 25] = irBuffer[i];
  }

  //take 25 sets of samples before calculating the heart rate.
  for (byte i = 75; i < 100; i++) {
    while (particleSensor.available() == false)  //do we have new data?
      particleSensor.check();                    //Check the sensor for new data

    digitalWrite(readLED, !digitalRead(readLED));  //Blink onboard LED with every data read

    redBuffer[i] = particleSensor.getRed();
    irBuffer[i] = particleSensor.getIR();
    particleSensor.nextSample();  //We're finished with this sample so move to next sample

    //send samples and calculation result to terminal program through UART
    if (validSPO2 == 1) {
      Serial.println(spo2, DEC);
    } else {
      Serial.println(0);
    }
  }

  //After gathering 25 new samples recalculate HR and SP02
  maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
  TMP = 3;
}

void electroCardioGram() {
  // Реализация функции 4
  if ((digitalRead(10) == 1) || (digitalRead(9) == 1)) {
    Serial.println(0);
  } else {
    // send the value of analog input 0:
    Serial.println(analogRead(A0));
  }
  TMP = 4;

  // Добавьте код функции 4 здесь
}

void function5() {
  // Реализация функции 5
  Serial.println(5);
  TMP = 5;

  // Добавьте код функции 5 здесь
}

void temperatureMetr() {  // 5V, GND, 20 pin, 21 pin
  int device = 0x5A << 1;
  int data_low = 0;
  int data_high = 0;
  int pec = 0;
  unsigned char result = i2c_start(device + I2C_WRITE);
  i2c_write(0x07);

  // read
  i2c_rep_start(device + I2C_READ);
  data_low = i2c_readAck();   // Read 1 byte and then send ack
  data_high = i2c_readAck();  // Read 1 byte and then send ack
  pec = i2c_readNak();
  i2c_stop();

  // This converts high and low bytes together and processes temperature, MSB is
  // a error bit and is ignored for temps
  double tempFactor =
    0.02;                    // 0.02 degrees per LSB (measurement resolution of the MLX90614)
  double tempData = 0x0000;  // zero out the data
  tempData = (double)(((data_high & 0x007F) << 8) + data_low);
  tempData = (tempData * tempFactor) - 0.01;
  float celcius = tempData - 273.15;
  Serial.println(celcius);
  TMP = 6;
}

void function7() {
  // Реализация функции 7
  Serial.println(7);
  TMP = 7;

  // Добавьте код функции 7 здесь
}

// Если у вас есть другие функции, добавьте их здесь
