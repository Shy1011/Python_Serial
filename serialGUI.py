from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys
from SerialPort import  Ui_Form
from Serial_01 import SerialPort
from hintDialog import portHasBeenOpened
import threading
from PyQt5.QtCore import pyqtSignal
from datetime import datetime
import time
import re
import xlwings as xw
class SerialGUI(QWidget,Ui_Form):

    state = False # 端口状态
    threadFlag = True # 线程开启状态
    dataNumber = 0 # 接收到的字符串数量
    dataSent = 0  # 发送了多少个字符串
    ascllState = False # ACII/HEX显示标志位
    timeShow = False # 是否显示时间标志位
    autoSend = False # 是否自动重发标志位
    fullData = ""  # 缓存的数据 显示的数据
    check = False #
    NameTest = "A1"


    # 定义一个信号，用于接收串口数据 可以触发槽函数的 详见 Readme.md
    # 触发函数用一个数字出发函数
    receive_data_signal = pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self.ser = SerialPort() # 创建端口实例
        self.ser.defaultSet()
        self.frameInit()

        for x in range(43) :
            label = getattr(self, f"label_{81+2*x}")  # 获取对应索引的label对象
            label.setText("-----")

        for x in range(100) :
            text = getattr(self, f"lineEdit_{x + 200}")
            label = getattr(self, f"label_{x + 200}")  # 获取对应索引的label对象
            label.setText("-----")
            text.setText("")
            # text.setReadOnly(True) # 使文本编辑框不可编辑
            text.setToolTip('Enter text')  # 设置工具提示

    def frameInit(self):
        self.setupUi(self)  # UI 初始化设置
        self.portSearch()  # 搜索 串口端口
        self.textBrowser.setText("")
        self.setWindowIcon(QIcon('R.png'))  # 设置窗口图标
        self.setWindowTitle('串口助手')
        self.comboBox.currentIndexChanged.connect(self.updateLabel_1)  # combo_2 槽函数
        self.comboBox_2.currentIndexChanged.connect(self.updateLabel_2)  # combo_2 槽函数
        self.comboBox_8.currentIndexChanged.connect(self.updateLabel_3)  # combo_2 槽函数
        self.checkBox_2.toggled.connect(self.AscllState)  # ASCII HEX切换
        self.checkBox_2.setChecked(True)
        self.checkBox_8.toggled.connect(self.autoSent)
        self.checkBox_8.setChecked(False)
        self.checkBox_6.setChecked(False)
        self.checkBox_6.toggled.connect(self.checkState)
        self.checkBox.clicked.connect(self.changeSerialState)
        self.checkBox_5.toggled.connect(self.timeShowState)
        self.sendData.clicked.connect(self.sendMessage)
        self.ClearData.clicked.connect(self.clearData)
        self.receive_data_signal.connect(self.update_received_data)
        self.pushButton_2.clicked.connect(self.push)
        self.radioButton.toggled.connect(self.radioFunc1)
        self.radioButton.setChecked(True)
        self.radioButton_2.toggled.connect(self.radioFunc2)
        self.pushButton.clicked.connect(self.clearLabel)
        self.pushButton_3.clicked.connect(self.btn3)


        # settooltips  hints
        self.pushButton_3.setToolTip("按下这个按键来设置名字")
        self.comboBox_8.setToolTip("选择表格中哪一列的数据")
        self.pushButton_2.setToolTip("清楚表格中所有侦测到的数据")
        self.ClearData.setToolTip("清除屏幕上显示的所有接收到的数据")

    def btn3(self):
        x = 0
        app = xw.App(visible=False)
        # 打开Excel文件
        wb = xw.Book('Names.xlsx')
        # 选择要读取的工作表
        sheet = wb.sheets['Sheet1']

        for c in range(100) :
            text = getattr(self, f"lineEdit_{c + 200}")
            text.setText("")

        for column in sheet.range(self.NameTest).expand('down').columns:  # 行 显示的是单个元素
            print(column.value)
        for i in (column.value) :
            text = getattr(self, f"lineEdit_{x + 200}")
            text.setText(i)
            x = x + 1
        wb.close()
        app.quit()


    def push(self):
        for x in range(100):
            text = getattr(self, f"lineEdit_{x + 200}")
            label = getattr(self, f"label_{x + 200}")  # 获取对应索引的label对象
            label.setText("-----")
            # text.setText("")
            self.label_299.setText("Ran Shuai")

    def checkState(self):
        if self.state:
            self.check = not self.check
        if (self.state == False) :
            win = portHasBeenOpened("监测前 请先打开串口")
            win.exec()
            self.check = False
            self.checkBox_6.setChecked(False)



    def radioFunc1(self):
        if self.radioButton.isChecked():
            print("1 is Checked")

    def radioFunc2(self):
        if self.radioButton_2.isChecked():
            print("2 is Checked")

    def autoSent(self):
        self.autoSend = not self.autoSend
        print(self.autoSend)
        thread1 = threading.Thread(target=self.autoSend1)
        thread1.start()


    def autoSend1(self):
        try :
            while(self.autoSend and self.state) :
                time.sleep(float(self.lineEdit.text()))
                print("Autosend Message")
                self.ser.sendData(self.textEdit.toPlainText())
                self.dataSent = self.dataSent + len(self.textEdit.toPlainText())
                self.label_9.setText(f'Rx : {str(self.dataSent)}')
        except :
            print("The port has already been opened")
            # win = portHasBeenOpened()
            # win.exec()

    def AscllState(self):
        self.ascllState = not self.ascllState
        print(self.ascllState)
        if self.ascllState == True :
            self.label_11.setText("ASCII")
        else :
            self.label_11.setText("HEX")

    def timeShowState(self):
        self.timeShow = not self.timeShow
        print(self.timeShow)

    def sendMessage(self):
        try :
            self.ser.sendData(self.textEdit.toPlainText())
            self.dataSent = self.dataSent + len(self.textEdit.toPlainText())
            self.label_9.setText(f'Tx : {str(self.dataSent)}')
        except :
            print("The port has already been opened")
            win = portHasBeenOpened("请先打开窗口")
            win.exec()

    def changeSerialState(self):   # 开关串口的端口
        self.state = not self.state
        if self.state == False :
            try :
                self.threadFlag = False
                self.ser.closeSerial()
                print("Serial Close")
                # self..setText("Close")

            except :
                print("Something is Wrong")

        elif(self.state == True):
            try :
                self.threadFlag = True
                self.ser.openSerial()
                time_thread = threading.Thread(target=self.recData)
                time_thread.start()
                print("Serial Open")
                # self.label_10.setText("Open")



            except :
                print("The port has already been opened")
                self.state = False
                self.checkBox.setChecked(False)
                win = portHasBeenOpened("此端口已被占用/或端口异常 \n    请选择另外的端口")
                win.exec()




    def updateLabel_1(self): # 端口选择
        self.ser.setPort(self.comboBox.currentText()) # 列表的文本选择
        print(f"Port is {self.comboBox.currentText()}")

    def updateLabel_3(self): # 端口选择
        self.NameTest = self.comboBox_8.currentText() # 列表的文本选择
        print(type(self.NameTest))

    def updateLabel_2(self): # 波特率的自定义设置
        if self.comboBox_2.currentText() == "Custom" :
            self.comboBox_2.setEditable(True)
        else :
            self.comboBox_2.setEditable(False)
        self.ser.setBaudrate(self.comboBox_2.currentText()) # 列表的文本选择
        print(f"Baudrate is {self.comboBox_2.currentText()}")


    def portSearch(self): # Port号的搜索

        self.ports = self.ser.searchPort()
        self.ports.sort()
        for port in self.ports :
            self.comboBox.addItem(f"{port}")

    def recData(self):
        while(self.threadFlag):
            data = self.ser.ReceiveData()
            # 发送串口数据信号到主线程
            self.dataNumber = self.dataNumber + len(data[0]) # 获取接收到多少个字符串
            if self.ascllState == True :
                self.receive_data_signal.emit(data[0])  # UI的更新不能再线程中所以我在这里设定一个槽函数,用来更新UI

            else :
                self.receive_data_signal.emit(data[1])


    def update_received_data(self,data): # receive_data_signal的槽函数
        if self.timeShow == False :
            if self.check == False :
                self.textBrowser.append(data)
            self.fullData = self.fullData + data
            if self.fullData[-1] == "\n" or self.fullData[-1] == "\r":
                self.textBrowser_2.append(self.fullData)
                if self.check == True :
                    self.textBrowser.append(self.fullData)


                string = re.sub(r'\D', '', self.fullData) # 删除除了数字之外的所有字符串
                self.fullData = ""
                print(len(string))
                signalNumber2 = int(len(string)/5) # 解析后的信号个数
                signalNumber = int(self.comboBox_7.currentText())
                print(signalNumber)
                groups = [string[i:i + 5] for i in range(0, len(string), 5)]  # 按照五个为一组分割字符串
                for i in range(signalNumber2) :
                    label = getattr(self, f"label_{i + 200}")  # 获取对应索引的label对象
                    label.setText(groups[i])



                if len(string) >= (signalNumber*5) :   # 因为每个信号是用5个字符表示的,只有当被解析的字符串大于5*信号数量的时候才开始更新信号
                    if (signalNumber >= 10) :
                        start_index = 81
                        for i in range(10):
                            label = getattr(self, f"label_{start_index + i * 2}")
                            label.setText(groups[i])


                    if (signalNumber >= 20) :
                        self.label_101.setText(groups[10])
                        self.label_103.setText(groups[11])
                        self.label_105.setText(groups[12])
                        self.label_107.setText(groups[13])
                        self.label_111.setText(groups[14]) # 这里有一个Label放错了所以不能使用循环
                        self.label_113.setText(groups[15])
                        self.label_115.setText(groups[16])
                        self.label_117.setText(groups[17])
                        self.label_119.setText(groups[18])
                        self.label_121.setText(groups[19])
                    #
                    if (signalNumber >= 30):
                        start_index = 123
                        groups_index = 20
                        for i in range(10):
                            getattr(self, f"label_{start_index + i * 2}").setText(groups[groups_index])
                            groups_index += 1

                    #
                    if (signalNumber >= 40):
                        start_index = 143
                        groups_index = 30
                        for i in range(10):
                            getattr(self, f"label_{start_index + i * 2}").setText(groups[groups_index])
                            groups_index += 1

                    if (signalNumber >= 41):
                        self.label_109.setText(groups[40])
                    if (signalNumber >= 42):
                        self.label_163.setText(groups[41])
                    if (signalNumber >= 43):
                        self.label_165.setText(groups[42])
        else :
            current_time = datetime.now()

            # 格式化时间，只包括小时、分钟和秒
            formatted_time = current_time.strftime("%H:%M:%S")
            self.textBrowser.append(f'{formatted_time} {data}')

        self.label_8.setText(f'Rx : {str(self.dataNumber)}')

    def clearLabel(self):
        for x in range(43) :
            label = getattr(self, f"label_{81+2*x}")  # 获取对应索引的label对象
            label.setText("-----")

    def clearData(self):
        self.textBrowser.setText("")
        self.dataNumber = 0
        self.dataSent = 0
        self.label_8.setText(f'Rx : {str(self.dataNumber)}')
        self.label_9.setText(f'Tx : {str(self.dataSent)}')

    def closeEvent(self, event):
        # 在关闭窗口时执行的操作
        print("Widget is being closed")
        self.threadFlag = False # 关闭进程
        self.autoSend = False  # 关闭进程
        event.accept()  # 接受关闭事件

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    win = SerialGUI()
    win.show()
    sys.exit(app.exec_())  # 运行应用程序，直到退出
