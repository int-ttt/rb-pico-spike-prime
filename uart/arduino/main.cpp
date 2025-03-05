#include <arduino.h>
#include <SoftwareSerial.h>

SoftwareSerial uart(0, 1);

void setup() {
    uart.begin(115200);
}

int i = 1;
void loop() {
    byte b[] = {i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i}
    uart.write(b, 16);
    uart.flush();
    i++;
}