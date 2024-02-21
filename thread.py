import threading
import time
import serial # 安装pyserial 而不是 serial
from serial.tools import list_ports  # 找串口设备需要的包
from Serial_01 import SerialPort
from SerialPort import  Ui_Form
# 定义一个线程子类
class CountThread(threading.Thread):
    def __init__(self, func,text):
        super().__init__()
        threading.Thread.__init__(self)
        # self.ser = serial.Serial()
        self.func = func
        self.flag = True

    def run(self):
        while(self.flag) :
            self.text = self.func()
            # time.sleep(1)
            # print("1")
    def get_result(self):
        return self.text

    def terminate(self):
        self.flag = False




# # 创建线程实例
# thread1 = CountThread("Thread 1", 5)
# thread2 = CountThread("Thread 2", 3)
#
# # 启动线程
# thread1.start()
# thread2.start()
#
# # 等待线程完成
# thread1.join()
# thread2.join()

print("主线程结束")
