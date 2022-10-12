'''
实时心电信号处理
'''

import pywt
import numpy as np
import matplotlib.pyplot as plt
import heartpy
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

with open(r'/home/ecg1013/Desktop/process/using_data.txt','w') as f:
    for d in data:
        f.write(d)

tdata = np.loadtxt("using_data.txt")
coeffs = pywt.wavedec(data=tdata, wavelet='db5', level=9)
cA9, cD9, cD8, cD7, cD6, cD5, cD4, cD3, cD2, cD1 = coeffs
threshold = (np.median(np.abs(cD1))/0.6745)*(np.sqrt(2*np.log(len(cD1))))
cD1.fill(0)
cD2.fill(0)
cD3.fill(0)
for i in range(1, len(coeffs)-3):
    coeffs[i]=pywt.threshold(coeffs[i], threshold)
rdata = pywt.waverec(coeffs=coeffs, wavelet='db5')
plt.figure(figsize=(20,6))
plt.subplot(3,1,1)
plt.plot(tdata)
plt.title("raw data")
plt.subplot(3,1,2)
plt.plot(rdata)
plt.title("new data")
print("="*30)
print("analysing heart rate ...")
try:
    wd,measures = heartpy.process(rdata,500)
    print(measures)
    peakAna = heartpy.plotter(wd,measures,show=False)
    peakAna.show()
    plt.show()
except:
    print("heart rate analysis result...")
    print("very noisy signal please check source signal...")
    plt.show()
