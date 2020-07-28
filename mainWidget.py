from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal


class CentralWidget(QWidget):
    signalTest = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.okButton = QPushButton('OK')
        self.okButton.clicked.connect(self.emitTest)

        hbox = QHBoxLayout()
        hbox.addWidget(self.okButton)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.show()

    def emitTest(self):
        self.signalTest.emit()
