import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("我的第一个 PyQt")
window.resize(400, 300)

layout = QVBoxLayout()

label = QLabel("欢迎来到 PyQt")

button = QPushButton("点我")

def click():
    label.setText("按钮被点击了")


button.clicked.connect(click)

layout.addWidget(label)
layout.addWidget(button)

window.setLayout(layout)

window.show()

app.exec()