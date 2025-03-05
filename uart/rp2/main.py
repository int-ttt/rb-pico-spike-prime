from machine import Pin, UART
import ustruct

led = Pin(25, Pin.OUT)
v33 = Pin(3, Pin.OUT)
ll = Pin(4)
v33.on()
led.on()
u1 = UART(0, 115200)
# u2 = UART(1, 115200)

while ll.value() == 0:
    pass
u1.write(b"\xaa")
# u2.write(b"\xaa")

while True:
    if u1.any() > 0:
        print('u1', u1.any(), ustruct.unpack("<B", u1.read(1)))
    # if u2.any() > 0:
    #     print('u2', u2.any(), ustruct.unpack("<B", u2.read(1)))