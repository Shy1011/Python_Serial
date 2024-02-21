# 2024年2月18日
使用线程来接收数据时出现了问题    
只要一开始接收数据就会导致程序卡死    
但是去掉线程中的while(1)就可以正常执行程序  
Pyqt5的UI只能在主线程中更新,如果在子线程中跟新UI就会导致程序退出 

# 使用线程接收串口数据

## UI需要在主线程中更新
Pyqt5的UI只能在主线程中更新,如果在子线程中跟新UI就会导致程序退出     
所以应该在子线程中设置一个变量,作为信号让主线程检测这个信号,信号改变就触发槽函数.类似下面    
~~~python
from PyQt5.QtCore import QObject, pyqtSignal

class SerialGUI(QWidget, Ui_Form):
    state = True

    # 定义一个信号，用于接收串口数据
    receive_data_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.receive_data_signal.connect(self.update_received_data)
        # 其他初始化代码...

    # 其他方法...

    def changeSerialState(self):
        self.state = not self.state
        if self.state:
            try:
                self.ser.closeSerial()
                print("Serial Close")
            except Exception as e:
                print(f"Error while closing serial port: {e}")
        else:
            try:
                self.ser.openSerial()
                time_thread = threading.Thread(target=self.recData)
                time_thread.start()
                print("Serial Open")
            except Exception as e:
                print(f"Error while opening serial port: {e}")
                win = portHasBeenOpened()
                win.exec()

    def recData(self):
        while True:
            data = self.ser.ReceiveData()
            # 发送串口数据信号到主线程
            self.receive_data_signal.emit(data)

    # 槽函数，用于在主线程中更新接收到的串口数据到 textBrowser
    def update_received_data(self, data):
        self.textBrowser.setText(data)
~~~


~~~python
# 伪代码
receive_data_signal = pyqtSignal(str)

self.receive_data_signal.connect(self.update_received_data)
self.receive_data_signal.emit(data)

 def update_received_data(self, data):
        self.textBrowser.setText(data)

        
"""
在PyQt5中，pyqtSignal是一个用于创建自定义信号的类。信号是在对象之间进行通信的一种机制，当某个事件发生时，会发送信号，其他对象可以连接到这个信号并在接收到信号时执行特定的操作。

在给出的代码片段中：

receive_data_signal = pyqtSignal(str)：这行代码定义了一个名为receive_data_signal的自定义信号，该信号传递一个字符串参数。

self.receive_data_signal.connect(self.update_received_data)：这行代码建立了一个连接，将receive_data_signal信号与update_received_data方法关联起来。这意味着当receive_data_signal信号发出时，会调用update_received_data方法，并将传递的数据作为参数传递给它。

self.receive_data_signal.emit(data)：这行代码发出了receive_data_signal信号，并传递了data作为参数。这将触发与之连接的update_received_data方法。

def update_received_data(self, data):：这是一个接收信号的方法，它会在信号被发出时被调用。在这个例子中，update_received_data方法接收一个字符串参数data。

self.textBrowser.setText(data)：这行代码在update_received_data方法中被调用，它将接收到的data字符串设置为textBrowser组件的文本内容，以更新UI界面显示。
"""

~~~

## 串口接收数据
最后使用线程 + 自定义信号完成了串口数据的接收  


# 自动重发
出现问题  
原因 : 还不知道是什么原因  

# 串口接收数据

有时候串口在接收数据的时候不是一次性接收完的,而是$0001 0002 #      
可能是这样收到的    
$000      
1 0002#        
如果你想显示完整的串口数据,可能就需要先判断,再处理.   再拼接   