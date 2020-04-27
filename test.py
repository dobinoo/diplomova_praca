import serial
ser = serial.Serial('/dev/ttyUSB0',115200);

message = "020FE"
ser.write(message.encode())
