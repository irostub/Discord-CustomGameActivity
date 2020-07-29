from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit,QLabel
from PyQt5.QtCore import pyqtSignal


class CentralWidget(QWidget):
    okSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        nowPlayOkButton = QPushButton('설정하러가기')
        contentOkButton = QPushButton('OK')
        statusOkButton = QPushButton('OK')
        contentLine = QLineEdit()
        statusLine = QLineEdit()

        contentOkButton.clicked.connect(self.contentOkEmit)

        nowPlayBox = QHBoxLayout()
        nowPlayBox.addWidget(QLabel("~하는 중\t: "))
        nowPlayBox.addWidget(nowPlayOkButton)

        contentBox = QHBoxLayout()
        contentBox.addWidget(QLabel("내용\t: "))
        contentBox.addWidget(contentLine)
        contentBox.addWidget(contentOkButton)

        statusBox = QHBoxLayout()
        statusBox.addWidget(QLabel("현재 상태\t: "))
        statusBox.addWidget(statusLine)
        statusBox.addWidget(statusOkButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(nowPlayBox)
        vbox.addLayout(contentBox)
        vbox.addLayout(statusBox)
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.setWindowTitle('Box Layout')
        self.show()

    def contentOkEmit(self):
        self.okSignal.emit()
