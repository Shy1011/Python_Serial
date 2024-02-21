import serial # 安装pyserial 而不是 serial
from serial.tools import list_ports  # 找串口设备需要的包
"""
如果先安装了srerial 则需要删除serial这个库,执行一下代码.再去安装pyserial这是为了告诉编译器serial已经被删除了
否则编译器会找到错误的路径去
"""

class SerialPort():

    def defaultSet(self):
        self.ser = serial.Serial()  # 一定要先初始化才能进行后面的操作 否则就会出错
        self.ser.port = "COM1"  # 不区分大小写
        self.ser.baudrate = 9600
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.timeout = 0.01

    def openSerial(self):
        self.ser.open()  # 打开端口

    def closeSerial(self):
        self.ser.close()

    def sendData(self,words):
        # 串口发送
        stop = bytes([170, 0, 0, 0, 0, 0, 187])  # 定义结束指令(aa 00 00 00 00 00 bb)
        self.ser.write(words.encode('utf-8')) # 发送数据
        # self.ser.write(words.encode('utf-8'))  # 发送数据


    def ReceiveData(self):
        # 串口接收
        while True:
            data = self.ser.read_all()

            if data:
                # print(data) #
                rec_str = data.decode('utf-8')
                rec_hex = ' '.join([hex(x) for x in data])
                print(rec_str)
                print(type(rec_str))
                return rec_str,rec_hex

    def searchPort(self):

        # 获取端口列表，列表中为 ListPortInfo 对象
        port_list = list(list_ports.comports())

        num = len(port_list)

        if num <= 0:
            print("找不到任何串口设备")
        else:
            ports = []
            for i in range(num):
                # 将 ListPortInfo 对象转化为 list
                port = list(port_list[i])
                # print(port)
                print(port[0]) # COM0 端口名字只是其中的一项
                ports.append(port[0])
            return ports


    def  setBaudrate(self,baudrate):
        self.ser.baudrate = baudrate

    def setTimeout(self,timeout):
        self.ser.timeout = timeout

    def setPort(self,port):
        self.ser.port = port  # 不区分大小写



# ser.close() # 关闭端口

# serial1 = SerialPort()
#
# serial1.searchPort()