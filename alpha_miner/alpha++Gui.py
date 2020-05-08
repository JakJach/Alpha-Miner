# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from parsers.txt_parser import read
from miners.alpha import Alpha
from miners.aplha_plus import AlphaPlus
from miners.alpha_plus_plus import AlphaPlusPlus
from representation.petri_net import PetriNet
from subprocess import check_call
import os.path

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1031, 904)
        MainWindow.setStyleSheet("background-color: rgb(149, 149, 149);\n"
"font: 10pt \"Lucida Console\";")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(40, 10, 951, 731))
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(200, 800, 631, 28))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(250, 840, 541, 16))
        self.label_6.setObjectName("label_6")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(400, 760, 251, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButton_2 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_2.addWidget(self.radioButton_2)
        self.radioButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_2.addWidget(self.radioButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1031, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.isScaledSize = False
        self.fileName = None
        self.isDefaultImage = True
        self.imagePath = None
        self.setButtons()
        self.setDefaultImage()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Alpha++"))
        self.pushButton_3.setText(_translate("MainWindow", "REMOVE"))
        self.pushButton.setText(_translate("MainWindow", "LOAD"))
        self.pushButton_2.setText(_translate("MainWindow", "DRAW"))
        self.label_6.setText(_translate("MainWindow", ""))
        self.radioButton_2.setText(_translate("MainWindow", "Scaled"))
        self.radioButton.setText(_translate("MainWindow", "Original"))

    def setButtons(self):
        self.pushButton.clicked.connect(self.getFile)
        self.pushButton_2.clicked.connect(self.draw)
        self.pushButton_3.clicked.connect(self.removeFile)
        self.radioButton.clicked.connect(self.setOriginal)
        self.radioButton_2.clicked.connect(self.setScaled)
        self.radioButton.setChecked(True)

    def setScaled(self):
        self.isScaledSize = True
        if (self.isDefaultImage == False):
            scene = QtWidgets.QGraphicsScene()
            pixmap = QtGui.QPixmap(self.imagePath)
            pixmap = pixmap.scaled(940, 720, QtCore.Qt.KeepAspectRatio)
            scene.addPixmap(pixmap)
            self.graphicsView.setScene(scene)


    def setOriginal(self):
        self.isScaledSize = False
        if (self.isDefaultImage == False):
            scene = QtWidgets.QGraphicsScene()
            pixmap = QtGui.QPixmap(self.imagePath)
            scene.addPixmap(pixmap)
            self.graphicsView.setScene(scene)

    def setDefaultImage(self):
        scene = QtWidgets.QGraphicsScene()
        self.pixmap = QtGui.QPixmap("background.jpeg")
        self.pixmap = self.pixmap.scaled(940, 720)
        scene.addPixmap(self.pixmap)
        self.graphicsView.setScene(scene)
        self.isDefaultImage = True
        self.imagePath = None

    def getFile(self):
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(caption="QFileDialog.getOpenFileName()")
        text = "Selected file: " + self.fileName
        self.label_6.setText(text)
        self.setDefaultImage()
        '''

        if self.fileName == '' and (lastFileName is not None or lastFileName is not ''):
            self.fileName = lastFileName
            text = "Selected file: " + self.fileName
        elif self.fileName == '':
            return
        else:
            text = "Selected file: " + self.fileName
            self.label_6.setText(text)
            self.setDefaultImage()
        '''

    def removeFile(self):
        self.fileName = None
        self.label_6.setText("There is no selected file")
        self.setDefaultImage()

    def useMiner(self):
        file_path = self.fileName
        log = read(file_path)
        alpha_model = AlphaPlusPlus(log)
        pn = PetriNet()
        pn.generate_with_alpha(alpha_model, dotfile="{}.dot".format(filename))
        check_call(["dot", "-Tpng", "{}.dot".format(filename), "-o", "{}.png".format(filename)])
        return "{}.png".format(os.getcwd()+r"\result")

    def draw(self):
        if self.fileName is None or self.fileName == '':
            self.label_6.setText("First choose file to parse!")
        else:
            self.imagePath = self.useMiner()
            if self.imagePath == None:
                text = "Cannot generate graph for: " + self.fileName
                self.label_6.setText(text)
            else:
                scene = QtWidgets.QGraphicsScene()
                pixmap = QtGui.QPixmap(self.imagePath)
                if self.isScaledSize:
                    pixmap = pixmap.scaled(940, 720, QtCore.Qt.KeepAspectRatio)
                scene.addPixmap(pixmap)
                self.graphicsView.setScene(scene)
                self.isDefaultImage = False
                text = "Generated graph for: " + self.fileName
                self.label_6.setText(text)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
