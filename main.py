import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("我的第一个 PyQt5")
window.resize(400, 300)

layout = QVBoxLayout()

label = QLabel("欢迎来到 PyQt5")

button = QPushButton("点我")

def click():
    label.setText("按钮被点击了")

button.clicked.connect(click)

layout.addWidget(label)
layout.addWidget(button)

window.setLayout(layout)

window.show()

sys.exit(app.exec_())