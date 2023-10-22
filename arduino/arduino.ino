void setup() {
  Serial.begin(1000000); // Инициализация порта Serial с скоростью 9600 бод
}
int TMP=0;

void loop() {
  static String inputBuffer = ""; // Буфер для сбора входных данных
  static bool newDataAvailable = false; // Флаг для обозначения наличия новых данных

  // Проверка наличия новых данных
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      newDataAvailable = true; // Установить флаг новых данных, если найден символ новой строки
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
    default:
      Serial.println(0);
      // Обработка некорректных команд, если необходимо
      break;
  }
  delay(300);
  // Добавьте другие функции по мере необходимости
}

void processSerialData(const String& data) {
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
    default:

      // Обработка некорректных команд, если необходимо
      break;
  }
}



void function1() {
  // Реализация функции 1
  Serial.println(1);
  TMP=1;

  // Добавьте код функции 1 здесь
}

void function2() {
  // Реализация функции 2
  Serial.println(2);
  TMP=2;

  // Добавьте код функции 2 здесь
}

void function3() {
  // Реализация функции 3
  Serial.println(3);
  TMP=3;

  // Добавьте код функции 3 здесь
}

// Если у вас есть другие функции, добавьте их здесь
