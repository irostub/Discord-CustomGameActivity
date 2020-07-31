import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QDesktopWidget, QTextEdit, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from mainWidget import CentralWidget
from pypresence import Presence
import datetime
import win32gui
import time
import psutil
import win32process

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def run_pypresence(self,arg1):
        client_id = 'ID' #get Discord Developer Portal
        RPC = Presence(client_id)
        RPC.connect()
        startTime = datetime.datetime.today().timestamp()
        RPC.update(details=arg1, state="CustomGameActivity.py", large_image="discord",
                   start=startTime)

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

        #센트럴 위젯
        self.central = CentralWidget()
        self.central.okSignal.connect(self.receive_ok) #mainWidget의 signalTest의 시그널과 연결
        self.central.okSignal2.connect(self.statusReceive_ok)
        self.setCentralWidget(self.central)

        #윈도우 기본 셋
        self.setWindowTitle('Discord Custom GameActivity')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(400, 500)
        self.center()
        self.show()

    #화면 창을 가운데로 정렬
    def center(self):
        qr = self.frameGeometry() #get 창의 위치, 크기 정보를
        cp = QDesktopWidget().availableGeometry().center()#get 현재 모니터 화면의 가운데 위치
        qr.moveCenter(cp) #qr에 담긴 프로그램 창의 중심정보를 화면의 중심으로 이동
        self.move(qr.topLeft()) #현재 창을 qr의 위치로 실제로 이동시킴, 의미 : topLeft => 모니터의 좌상단을 기준으로

    #액션
    def receive_ok(self,a):
        self.run_pypresence(a)
        print(a)
        print("receive")

    def statusReceive_ok(self,a):
        self.run_pypresence(a)
        print(a)
        print("receive2")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())