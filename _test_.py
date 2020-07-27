import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QDesktopWidget, QTextEdit, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
import win32gui
import time
import psutil
import win32process

class MyApp2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        okButton = QPushButton('OK')
        textEdit = QTextEdit()

        hbox = QHBoxLayout()
        hbox.addWidget(textEdit)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.setLayout(vbox)


        self.show()

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''Get Foreground Window process name
        w = win32gui
        w.GetWindowText(w.GetForegroundWindow())
        pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow())
        print(psutil.Process(pid[-1]).name())
        '''

        #메뉴바 액션
        exitAction = QAction('Exit',self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        #스테이터스 바
        #첫번째 호출 시 statusbar 생성, 이후 호출시 상태바 객체 반환
        #showMessage(str) 로 상태 메세지 변경
        self.statusBar().showMessage('Ready')

        #메뉴 바
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False) #Mac OS sync
        filemenu = menubar.addMenu('&Help')
        filemenu.addAction(exitAction)
        m = MyApp2()

        self.setCentralWidget(m)

        #윈도우 기본 셋
        self.setWindowTitle('Discord Custom GameActivity')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(500, 800)
        self.center()
        self.show()


    #화면 창을 가운데로 정렬
    def center(self):
        qr = self.frameGeometry() #get 창의 위치, 크기 정보를
        cp = QDesktopWidget().availableGeometry().center()#get 현재 모니터 화면의 가운데 위치
        qr.moveCenter(cp) #qr에 담긴 프로그램 창의 중심정보를 화면의 중심으로 이동
        self.move(qr.topLeft()) #현재 창을 qr의 위치로 실제로 이동시킴, 의미 : topLeft => 모니터의 좌상단을 기준으로



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())