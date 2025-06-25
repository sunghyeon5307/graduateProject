import serial
import time

ser = serial.Serial('/dev/cu.usbserial-1140', 115200)
time.sleep(2)

ser.write(b"1\n")
ser.flush()
print("전송완료")