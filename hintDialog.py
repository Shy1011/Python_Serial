# Hint the port has been opened by other app
from errorDealwith import Ui_Dialog
from PyQt5.QtWidgets import *
import sys

class portHasBeenOpened(Ui_Dialog,QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# app = QApplication(sys.argv)
# win =  portHasBeenOpened()
# win.show()
# sys.exit(app.exec_())  # 运行应用程序，直到退出
