import sys
from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication,QMainWindow,QPushButton,QProgressBar
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.SetupUi()
        
    def SetupUi(self):

        # Main Window Ayarları
        self.setGeometry(300,300,800,500)
        self.setWindowTitle('thread template')
        # Button Configuration
        self.start_button = QPushButton('Start Thread 1',self )
        self.stop_button = QPushButton('Stop Thread 1',self )
        self.start_button2 = QPushButton('Start Thread 2',self)
        self.stop_button2 = QPushButton('Stop Thread 2',self)

        self.start_button.setGeometry(50,20,100,70)
        self.stop_button.setGeometry(50,120,100,70)
        self.start_button2.setGeometry(170,20,100,70)
        self.stop_button2.setGeometry(170,120,100,70)
        
        #PROGRESS BAR CONFİG
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(290,20,300,70)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(50)
        self.progress_bar2 = QProgressBar(self)
        self.progress_bar2.setGeometry(290,120,300,70)
        self.progress_bar2.setMinimum(0)
        self.progress_bar2.setMaximum(100)
        self.progress_bar2.setValue(50)
        #CONNECT FUCTİONS
        self.start_button.clicked.connect(self.start_thread1)
        self.stop_button.clicked.connect(self.stop_thread1)
        self.start_button2.clicked.connect(self.start_thread2)
        self.stop_button2.clicked.connect(self.stop_thread2)

    #FUNCTİONS
    def start_thread1(self):
        self.stop_button.setEnabled(True)
        self.worker1 = WorkerThread(index = 0)
        self.worker1.signal.connect(self.SignalProccessing)
        self.worker1.start()
        self.start_button.setEnabled(False)

    def stop_thread1(self):
        self.worker1.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def start_thread2(self):
        self.stop_button2.setEnabled(True)
        self.worker2 = WorkerThread(index=1)
        self.worker2.signal.connect(self.SignalProccessing)
        self.worker2.start()
        self.start_button2.setEnabled(False)

    def stop_thread2(self):
        self.worker2.stop()
        self.start_button2.setEnabled(True)
        self.stop_button2.setEnabled(False)

    
    def SignalProccessing(self,cnt):
        
        sender = self.sender().index

        if sender == 0:
            self.progress_bar.setValue(cnt)
        if sender == 1:
            self.progress_bar2.setValue(cnt)

class WorkerThread(QThread):
    signal = pyqtSignal(int)
    def __init__(self,index=0):
        super(WorkerThread,self).__init__()
        self.index = index
        self.isRunning=False


    def run(self):
        print('\nStarting thread: ',self.index)
        cnt=0
        while True:
            if cnt == 99: cnt = 0
            cnt+=1
            time.sleep(0.01)
            self.signal.emit(cnt)

    def stop(self):
        self.isRunning=False
        print('\nTerminate Thread: ',self.index)
        self.terminate()



app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())

