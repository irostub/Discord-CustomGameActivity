import os.path
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QDesktopWidget, QWidget, QPushButton, QLineEdit, QGridLayout, QLabel, \
    QScrollArea, QVBoxLayout,QDialog, QHBoxLayout, QSizePolicy, QMessageBox, QSystemTrayIcon, QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from pypresence import Presence
import datetime
import webbrowser
import win32gui
import time
import psutil
import win32process
import json

class AboutMe(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        scrollWidget = QWidget()
        scrollLayout = QVBoxLayout()
        scrollWidget.setLayout(scrollLayout)
        sl = QVBoxLayout()

        for i in range(100):
            sl.addWidget(QLabel('count %02d' %i))
        scrollWidget.setLayout(sl)
        sc = QScrollArea()
        sc.setWidgetResizable(True)
        sc.setWidget(scrollWidget)
        layout = QHBoxLayout()
        layout.addWidget(sc)
        self.setLayout(layout)


class Help(QWidget):
    def __init__(self):
        super().__init__()
        print("ready Help Widget")
        self.initUI()


    def initUI(self):
        scrollwidget = QWidget() #스크롤 시킬 위젯
        scrolllayout = QVBoxLayout() #스크롤 시킬 위젯의 레이아웃
        scrollwidget.setLayout(scrolllayout)
        scrolllayout.addWidget(QLabel("1-1. discord developer 사이트에서 애플리케이션을 생성"))
        scrolllayout.addWidget(QLabel("1-2. 생성한 애플리케이션의 이름이 디스코드에서 ~~하는 중으로 표시됨"))
        scrolllayout.addWidget(QLabel("2. 생성한 애플리케이션의 Client ID를 프로그램의 Client 설정에 입력"))
        scrolllayout.addWidget(QLabel("3. 표시하기 원하는 내용과 상태를 작성"))
        scrolllayout.addWidget(QLabel("4. 표시하기 원하는 사진을 Discord developer 사이트의 Rich presence에 업로드 후 업로드한 이름을 입력"))
        #gif 나 사진으로 대채할 것

        scroll = QScrollArea() #스크롤 입힐 영역
        scroll.setWidgetResizable(True) 
        scroll.setWidget(scrollwidget) #누구를 스크롤 시킬지
        layout = QHBoxLayout() #스크롤 시킬 위젯을 담을 박스
        layout.addWidget(scroll) #스크롤 시킬 영역 전체를 담는다
        self.setLayout(layout) #Help의 창에 적용


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        print("ready MainWindow")
        self.initUI()
        self.pypSet = False
        self.p = Help()
        loadContent = './config.json'
        if os.path.isfile(loadContent):
            print("file enter")
            with open("config.json", "r") as f:
                readfile = json.load(f)
                self.idLine.setText(readfile[0])
                self.contentLine.setText(readfile[1])
                self.statusLine.setText(readfile[2])
                self.imageLine.setText(readfile[3])
                print(readfile)
        else:
            print("file not in here")

    #pyqt 종료 이벤트 override 됨
    def closeEvent(self, event):
        if self.pypSet == True:
            self.RPC.close()
            print("RPC Close success")
            print("close program")

        else:
            print("RPC is not set")
            print("close program")
            print("check line empty:" + str(self.checkEmptyLine()))
            if self.checkEmptyLine():
                pass
            else:
                writeContent = [self.idLine.text(), self.contentLine.text(), self.statusLine.text(), self.imageLine.text()]
                with open("config.json", "w") as json_file:
                    json.dump(writeContent, json_file)
                    print(writeContent)
            self.p.close() #메인창을 꺼도 help widget이 닫히지 않으므로 직접 제거
        print("exit")

    def run_pypresence(self, *args):
        print("enter run_pypresence")
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
        #self.statusBar().hide() #hide status bar
        #메뉴 바
        tray = QSystemTrayIcon(QIcon('whatsapp.png'),parent=self)
        tray.setToolTip("check out this app on tray icon")
        tray.setVisible(True)
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False) #Mac OS sync
        menu = QMenu('&도움말')
        menu2 = QMenu("what")
        exitact = menu2.addAction('종료')
        exitact.triggered.connect(qApp.quit)
        filemenu = menu
        tray.setContextMenu(menu2)
        filemenu.addAction(exitAction)
        filemenu.addAction(aboutAction)
        menubar.addMenu(menu2)

        #센트럴 위젯
        central = QWidget()
        #central.setStyleSheet("background-color:#333333; border-style:solid; border-width: 1px; border-color: #555555; border-radius: 4px;")

        self.idLine = QLineEdit()
        self.idLine.setPlaceholderText("Client ID를 입력")
        self.contentLine = QLineEdit()
        self.contentLine.setPlaceholderText("원하는 내용을 입력")
        self.statusLine = QLineEdit()
        self.statusLine.setPlaceholderText("원하는 상태를 입력")
        self.imageLine = QLineEdit()
        self.imageLine.setPlaceholderText("이미지 이름")
        self.okButton = QPushButton("적용")
        self.okButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        grid.setContentsMargins(59,50,50,50)

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

        #self.setWindowFlags(Qt.FramelessWindowHint) #window frame hide
        #self.setAttribute(Qt.WA_TranslucentBackground) #remove border top side grabage
        self.center()
        self.show()
        #self.setStyleSheet("background-color: #333333;") #self -> style css type

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

        if self.checkEmptyLine():
            print("Enter onOkButton event -> checkEmptyLine False Enter here")
            x = QMessageBox.question(self, '경고', '입력 항목을 다시 확인해주세요', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            self.run_pypresence(id, content, status, image)

    def checkEmptyLine(self):
        check = True
        if self.idLine.text() == "" or self.contentLine.text() == "" or self.statusLine.text() == "" or self.imageLine.text() == "":
            check = True
        else:
            check = False
        return check


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
    
##TODO:https://doc.qt.io/qt-5/qtwidgets-desktop-systray-example.html 트레이 아이콘을 만들고 종료 시 트레이로 보내는 방법