import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QColor

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.shadowApplied = False  # 用于跟踪阴影是否已应用
        self.initUI()

    def initUI(self):
        # 创建一个QPushButton
        self.button = QPushButton(self)
        # 设置按钮的位置和大小
        self.button.setGeometry(100, 100, 100, 50)

        # 设置按钮的图标
        self.button.setIcon(QIcon('arrow.png'))
        # 可以调整图标的大小
        self.button.setIconSize(QSize(40, 40))

        # 为按钮连接点击事件
        self.button.clicked.connect(self.toggleShadow)

        # 创建阴影效果，但不立即应用
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setXOffset(5)
        self.shadow.setYOffset(5)
        self.shadow.setColor(QColor(0, 0, 0, 150))

        # 设置窗口的位置和大小
        self.setGeometry(300, 300, 300, 200)
        # 设置窗口的标题
        self.setWindowTitle('Icon Button Example')
        # 显示窗口
        self.show()

    def toggleShadow(self):
        # 切换阴影效果
        if self.shadowApplied:
            self.button.setGraphicsEffect(None)
            self.shadowApplied = False
            self.button.setIconSize(QSize(60, 60))
        else:
            self.button.setGraphicsEffect(self.shadow)
            self.shadowApplied = True
            self.button.setIconSize(QSize(40, 40))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
