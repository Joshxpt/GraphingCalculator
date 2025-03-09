import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow,QLabel,QWidget,
                             QVBoxLayout, QHBoxLayout, QGridLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt # alignments
from PyQt5.QtGui import QPixmap

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI Test")
        self.setGeometry(250, 250, 1000, 700)

        '''
        LABELS
        label = QLabel("Hi there", self)
        label.setFont(QFont("Helvetica", 20))
        label.setGeometry(0,0,500,100)
        label.setStyleSheet("color:red;"
                            "background-color:green;"
                            "font-size:30px;"
                            "font-weight:bold;"
                            "font-style:italic;"
                            "text-decoration:underline;")

        label.setAlignment(Qt.AlignCenter)'''


        '''
        IMAGES
        label = QLabel(self)
        label.setGeometry(0,0,250,250)
        pixmap = QPixmap("assets/phoenix.png")
        label.setPixmap(pixmap)
        label.setScaledContents(True)

        label.setGeometry((self.width() - label.width()) // 2, (self.height() - label.height()) // 2 , label.width(), label.height())
        '''

        self.initUI()

    def initUI(self): # common method for initalising UI
        # self always = window
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        label1 = QLabel("1", self)
        label2 = QLabel("2", self)
        label3 = QLabel("3", self)
        label4 = QLabel("4", self)
        label5 = QLabel("5", self)

        label1.setStyleSheet("background-color:green")
        label2.setStyleSheet("background-color:yellow")
        label3.setStyleSheet("background-color:red")
        label4.setStyleSheet("background-color:blue")
        label5.setStyleSheet("background-color:purple")

        #these overlap! so use a layout manager

        vbox = QVBoxLayout()
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(label3)
        vbox.addWidget(label4)
        vbox.addWidget(label5)

        central_widget.setLayout(vbox)

        #for horizontal - replace vbox with hbox
        #can also do grid = QGridLayout
        #eg. grid = addWidget(label, 0 , 0) where numbers are rows and columns


# for learning purposes // TO DELETE
def main():
    pass

if __name__ == '__main__': # if we are running the file directly
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())