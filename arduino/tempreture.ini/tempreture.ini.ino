#include <i2cmaster.h>

void setup() {
  Serial.begin(1000000); // Инициализация порта Serial с скоростью 9600 бод
  // static String inputErrorBuffer = ""; // Буфер для сбора данных по ошибкам
  // static bool newErrorAvailable =
  // false; // Флаг для обозначения наличия новых данных по ошибкам
  // while (Serial.available()) {
  //   char error = Serial.read();
  //   if (error == '\n') {
  //     newErrorAvailable =
  //         true; // Установить флаг новых данных, если найден символ новой
  //         строки
  //   } else {
  //     inputErrorBuffer += error; // Добавить символ к буферу
  //   }
  // }

  // if (newErrorAvailable) {
  //   // Если есть новые данные, обработайте их
  //   int command = inputErrorBuffer.toInt();
  //   if (command == 8) {
  //     Serial.println(1);
  //     unsigned char errors[7] = [ '0', '0', '0', '0', '0', '0', '0' ];

  //     // errors[0] = 0;
  //     // errors[1] = 0;
  //     // errors[2] = 0;
  //     // errors[3] = 0;
  //     // errors[4] = 0;
  //     // errors[5] = 0;

  //     // temperature (tempretureFunction())
  //     i2c_init(); // Initialise the i2c bus
  //     errors[6] = i2c_start(device + I2C_WRITE);

  //     // errors[7] = 0;

  //     Serial.println(errors[0] + errors[1] + errors[2] + errors[3] +
  //     errors[4] +
  //                    errors[5] + errors[6]);
  //   }
  // } else {
  //   Serial.println(0);
  // }
  i2c_init();                            // Initialise the i2c bus
  PORTD = (1 << PORTD1) | (1 << PORTD0); // enable pullups
}

int TMP = 0;

void loop() {
  static String inputBuffer = ""; // Буфер для сбора входных данных
  static bool newDataAvailable =
      false; // Флаг для обозначения наличия новых данных

  // Проверка наличия новых данных
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      newDataAvailable =
          true; // Установить флаг новых данных, если найден символ новой строки
    } else {
      inputBuffer += c; // Добавить символ к буферу
    }
  }

  if (newDataAvailable) {
    // Если есть новые данные, обработайте их
    processSerialData(inputBuffer);
    // Очистите буфер и сбросьте флаг новых данных
    inputBuffer = "";
    newDataAvailable = false;
  }

  // Здесь вы можете выполнять свои функции без блокировки чтения из Serial
  int command = inputBuffer.toInt();
  switch (TMP) {
  case 1:
    function1();
    break;
  case 2:
    function2();
    break;
  case 3:
    function3();
    break;
  case 4:
    function4();
    break;
  case 5:
    function5();
    break;
  case 6:
    tempretureFunction();
    break;
  case 7:
    function7();
    break;
  default:
    Serial.println(0);
    // Обработка некорректных команд, если необходимо
    break;
  }
  delay(300);
  // Добавьте другие функции по мере необходимости
}

void processSerialData(const String &data) {
  // Разбор и обработка входных данных из Serial
  int command = data.toInt();

  // Выполните действия в зависимости от команды
  switch (command) {
  case 1:
    function1();
    break;
  case 2:
    function2();
    break;
  case 3:
    function3();
    break;
  case 4:
    function4();
    break;
  case 5:
    function5();
    break;
  case 6:
    tempretureFunction();
    break;
  case 7:
    function7();
    break;
  default:

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

void function2() {
  // Реализация функции 2
  Serial.println(2);
  TMP = 2;

  // Добавьте код функции 2 здесь
}

void function3() {
  // Реализация функции 3
  Serial.println(3);
  TMP = 3;

  // Добавьте код функции 3 здесь
}

void function4() {
  // Реализация функции 4
  Serial.println(4);
  TMP = 4;

  // Добавьте код функции 4 здесь
}

void function5() {
  // Реализация функции 5
  Serial.println(5);
  TMP = 5;

  // Добавьте код функции 5 здесь
}

void tempretureFunction() {
  int device = 0x5A << 1;
  int data_low = 0;
  int data_high = 0;
  int pec = 0;
  unsigned char result = i2c_start(device + I2C_WRITE);
  i2c_write(0x07);

  // read
  i2c_rep_start(device + I2C_READ);
  data_low = i2c_readAck();  // Read 1 byte and then send ack
  data_high = i2c_readAck(); // Read 1 byte and then send ack
  pec = i2c_readNak();
  i2c_stop();

  // This converts high and low bytes together and processes temperature, MSB is
  // a error bit and is ignored for temps
  double tempFactor =
      0.02; // 0.02 degrees per LSB (measurement resolution of the MLX90614)
  double tempData = 0x0000; // zero out the data
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
