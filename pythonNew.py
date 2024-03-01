from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

def on_button_click():
    label.setText("Hello, PyQt!")

app = QApplication([])

window = QWidget()
layout = QVBoxLayout()

label = QLabel('Press the button')
layout.addWidget(label)

button = QPushButton('Click me')
button.clicked.connect(on_button_click)
layout.addWidget(button)

window.setLayout(layout)
window.show()

app.exec_()