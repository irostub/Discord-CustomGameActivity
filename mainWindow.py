import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QDesktopWidget, QWidget, QPushButton, QLineEdit, QGridLayout, QLabel, QScrollArea, QVBoxLayout,QDialog, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from pypresence import Presence
import datetime
import webbrowser
import win32gui
import time
import psutil
import win32process


class AboutMe(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()




class Help(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        w = QWidget()
        sl = QVBoxLayout()
        for i in range (100):
            sl.addWidget(QLabel('count %02d' %i))
        w.setLayout(sl)
        sc = QScrollArea()
        sc.setWidgetResizable(True)
        sc.setWidget(w)
        layout = QHBoxLayout()
        layout.addWidget(sc)
        self.setLayout(layout)



class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.pypSet = False
        self.p = Help()

    #pyqt 종료 이벤트 override 됨
    def closeEvent(self, event):
        if self.pypSet == True:
            self.RPC.close()
            print("RPC Close success")
            print("close program")
        else:
            print("RPC is not set")
            print("close program")
            pass
        print("exit")

    def run_pypresence(self, *args):
        #pypresence 첫 실행 시
        #pypresence 주어진 client_id로 연결하고 상태를 업데이트
        if self.pypSet == False:
            self.client_id = args[0] #get Discord Developer Portal
            self.RPC = Presence(self.client_id,pipe=0)
            self.RPC.connect()
            self.pypSet = True
            startTime = datetime.datetime.today().timestamp()
            self.RPC.update(details=args[1], state=args[2], large_image=args[3],
                       start=startTime)
        #pypresence 첫 실행이 아닐 시 연결에 변화 없이 내용 업데이트
        elif self.pypSet == True:
            startTime = datetime.datetime.today().timestamp()
            self.RPC.update(details=args[1], state=args[2], large_image=args[3],
                       start=startTime)
            print(args)


    def initUI(self):
        #Get Foreground Window process name
        w = win32gui
        w.GetWindowText(w.GetForegroundWindow())
        pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow())
        print(psutil.Process(pid[-1]).name())
        #foreground 프로세스 변경 시 자동으로 사용자 상태가 현재 활성화 된 창을 표시할 수 있도록
        #SetWinEventHook 를 사용하여 foreground프로세스가 변경될 때 이벤트를 받을 수 있어야야함


        #메뉴바 액션
        exitAction = QAction('종료',self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('프로그램 종료')
        exitAction.triggered.connect(qApp.quit)

        aboutAction = QAction('제작자',self)
        aboutAction.setStatusTip('제작자의 정보 : iro_bound')
        #exitAction.triggered.connect()

        #스테이터스 바
        #첫번째 호출 시 statusbar 생성, 이후 호출시 상태바 객체 반환
        #showMessage(str) 로 상태 메세지 변경
        self.statusBar().showMessage('DCGA 준비됨')

        #메뉴 바
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False) #Mac OS sync
        filemenu = menubar.addMenu('&도움말')
        filemenu.addAction(exitAction)
        filemenu.addAction(aboutAction)

        #센트럴 위젯
        central = QWidget()
        self.idLine = QLineEdit()
        self.contentLine = QLineEdit()
        self.statusLine = QLineEdit()
        self.imageLine = QLineEdit()
        self.okButton = QPushButton("적용")
        self.doingButton = QPushButton("설정하기")

        labelID = QLabel("Client 설정 :")
        labelID.setAlignment(Qt.AlignCenter)
        label0 = QLabel("~하는 중 :")
        label0.setAlignment(Qt.AlignCenter)
        label1 = QLabel("내용 : ")
        label1.setAlignment(Qt.AlignCenter)
        label2 = QLabel("상태 : ")
        label2.setAlignment(Qt.AlignCenter)
        label3 = QLabel("이미지 : ")
        label3.setAlignment(Qt.AlignCenter)

        grid = QGridLayout()
        grid.setContentsMargins(50, 50, 50, 50)

        grid.addWidget(labelID, 0, 0)
        grid.addWidget(self.idLine, 0, 1)
        grid.addWidget(label0, 1, 0)
        grid.addWidget(self.doingButton, 1, 1)
        grid.addWidget(label1, 2, 0)
        grid.addWidget(self.contentLine, 2, 1)
        grid.addWidget(label2, 3, 0)
        grid.addWidget(self.statusLine, 3, 1)
        grid.addWidget(label3, 4, 0)
        grid.addWidget(self.imageLine, 4, 1)
        grid.addWidget(self.okButton, 5, 0, 1, 2)

        #grid.setColumnStretch(0, 2)
        #grid.setColumnStretch(1, 2)

        central.setLayout(grid)
        self.setCentralWidget(central)

        #윈도우 기본 셋
        self.setWindowTitle('Discord Custom GameActivity')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(400, 300)
        self.center()
        self.show()

        #이벤트
        self.doingButton.clicked.connect(self.onDoingButton)
        self.okButton.clicked.connect(self.onOkButton)
    #화면 창을 가운데로 정렬
    def center(self):
        qr = self.frameGeometry() #get 창의 위치, 크기 정보를
        cp = QDesktopWidget().availableGeometry().center()#get 현재 모니터 화면의 가운데 위치
        qr.moveCenter(cp) #qr에 담긴 프로그램 창의 중심정보를 화면의 중심으로 이동
        self.move(qr.topLeft()) #현재 창을 qr의 위치로 실제로 이동시킴, 의미 : topLeft => 모니터의 좌상단을 기준으로

    #액션
    def onDoingButton(self):
        webbrowser.open("https://discord.com/developers/applications")
        self.p.show()


    def onOkButton(self):
        id = self.idLine.text()
        content = self.contentLine.text()
        status = self.statusLine.text()
        image = self.imageLine.text()
        print(id, content, status, image)
        self.run_pypresence(id,content,status,image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())