import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个QPushButton
        self.button = QPushButton('Click Me', self)
        # 设置按钮的位置和大小
        self.button.setGeometry(100, 100, 100, 50)

        # 创建阴影效果
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor('black'))

        # 为按钮设置按下和释放的事件处理
        self.button.pressed.connect(self.applyShadow)
        self.button.released.connect(self.clearShadow)

        # 设置窗口的位置和大小
        self.setGeometry(300, 300, 300, 200)
        # 设置窗口的标题
        self.setWindowTitle('Button Shadow Example')
        # 显示窗口
        self.show()

    def applyShadow(self):
        # 按钮按下时应用阴影效果
        self.button.setGraphicsEffect(self.shadow)

    def clearShadow(self):
        # 按钮释放时清除阴影效果
        self.button.setGraphicsEffect(None)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())