import serial
ser=serial.Serial('/dev/ttyUSB0',9600,timeout=1,parity=serial.PARITY_NONE,stopbits=1)

data = []

while True:
    x = ser.readline()
    if x:
        str1 = x.decode('utf-8')
        data.append(str1)
        if len(data) >= 5000:
            break

print(data)

with open(r'/home/ecg1013/Desktop/process/using_data.txt','w') as f:
    for d in data:
        f.write(d)