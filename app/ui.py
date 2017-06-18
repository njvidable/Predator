import cv2
import numpy as np
from PyQt4 import QtCore, QtGui
from sys import exit, argv, path 
from os import listdir
from imghdr import what
from run_rf import run
from measure_functions import transform
from painting.paint_functions import paint_circles, cross_info
from math_util.circle_functions import is_within_circles, round_circles_coord
from math_util.r3_functions import get_rot_mtx
from math_util.distance_functions import get_closest, cal_dist
path.insert(1, "../")
from json_trade.json_functions import json_to_data

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.showMaximized()
        self.rf_run_executed = False
        self.om_run_executed = False
        self.process = None
        self.mode_dic = {True : 0, False: 3}
        self.measure_dic = {True: self.measure_lines,\
            False: self.measure_contour}
        self.disable_run_buttons()
        self.undistort_parameters = None
    
    """
    Creates and configures the elements of the ui.
    Connects element-element signals and slots.
    Connects signals to other methods.
    """
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(804, 579)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        Form.setFont(font)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum,\
            QtGui.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.tab)
        self.lineEdit.setMinimumSize(QtCore.QSize(300, 0))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton = QtGui.QPushButton(self.tab)
        self.pushButton.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        spacerItem4 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum,\
            QtGui.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem4)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem5)
        self.pushButton_4 = QtGui.QPushButton(self.tab)
        self.pushButton_4.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_9.addWidget(self.pushButton_4)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem6)
        self.progressBar = QtGui.QProgressBar(self.tab)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout_9.addWidget(self.progressBar)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        spacerItem8 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum,\
            QtGui.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem8)
        self.line_2 = QtGui.QFrame(self.tab)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout_3.addWidget(self.line_2)
        spacerItem9 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum,\
            QtGui.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem9)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem10 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem10)
        self.label_2 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_4.addWidget(self.label_2)
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem11)
        self.lcdNumber = QtGui.QLCDNumber(self.tab)
        self.lcdNumber.setMinimumSize(QtCore.QSize(90, 70))
        self.lcdNumber.setMaximumSize(QtCore.QSize(90, 70))
        self.lcdNumber.setFrameShape(QtGui.QFrame.NoFrame)
        self.lcdNumber.setNumDigits(3)
        self.lcdNumber.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumber.setProperty("intValue", 222)
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.horizontalLayout_4.addWidget(self.lcdNumber)
        self.horizontalSlider = QtGui.QSlider(self.tab)
        self.horizontalSlider.setMinimumSize(QtCore.QSize(100, 0))
        self.horizontalSlider.setMaximumSize(QtCore.QSize(100, 16777215))
        self.horizontalSlider.setMaximum(255)
        self.horizontalSlider.setProperty("value", 222)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.horizontalLayout_4.addWidget(self.horizontalSlider)
        spacerItem12 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem12)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem13 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem13)
        self.label_3 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_5.addWidget(self.label_3)
        spacerItem14 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem14)
        self.radioButton = QtGui.QRadioButton(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton.setFont(font)
        self.radioButton.setChecked(True)
        self.radioButton.setAutoExclusive(False)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.horizontalLayout_5.addWidget(self.radioButton)
        spacerItem15 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem15)
        self.radioButton_2 = QtGui.QRadioButton(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setAutoExclusive(False)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.horizontalLayout_5.addWidget(self.radioButton_2)
        spacerItem16 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem16)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem17 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem17)
        self.label_4 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_6.addWidget(self.label_4)
        spacerItem18 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem18)
        self.lcdNumber_2 = QtGui.QLCDNumber(self.tab)
        self.lcdNumber_2.setMinimumSize(QtCore.QSize(90, 70))
        self.lcdNumber_2.setMaximumSize(QtCore.QSize(90, 70))
        self.lcdNumber_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.lcdNumber_2.setNumDigits(3)
        self.lcdNumber_2.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumber_2.setProperty("intValue", 60)
        self.lcdNumber_2.setObjectName(_fromUtf8("lcdNumber_2"))
        self.horizontalLayout_6.addWidget(self.lcdNumber_2)
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_6.addWidget(self.label_6)
        self.horizontalSlider_2 = QtGui.QSlider(self.tab)
        self.horizontalSlider_2.setMinimumSize(QtCore.QSize(70, 0))
        self.horizontalSlider_2.setMaximumSize(QtCore.QSize(70, 16777215))
        self.horizontalSlider_2.setMinimum(30)
        self.horizontalSlider_2.setMaximum(100)
        self.horizontalSlider_2.setSliderPosition(60)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName(_fromUtf8("horizontalSlider_2"))
        self.horizontalLayout_6.addWidget(self.horizontalSlider_2)
        spacerItem19 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem19)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        spacerItem20 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem20)
        self.label_5 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_7.addWidget(self.label_5)
        spacerItem21 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem21)
        self.lcdNumber_3 = QtGui.QLCDNumber(self.tab)
        self.lcdNumber_3.setMinimumSize(QtCore.QSize(60, 70))
        self.lcdNumber_3.setMaximumSize(QtCore.QSize(60, 70))
        self.lcdNumber_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.lcdNumber_3.setNumDigits(2)
        self.lcdNumber_3.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumber_3.setProperty("intValue", 25)
        self.lcdNumber_3.setObjectName(_fromUtf8("lcdNumber_3"))
        self.horizontalLayout_7.addWidget(self.lcdNumber_3)
        self.horizontalSlider_3 = QtGui.QSlider(self.tab)
        self.horizontalSlider_3.setMinimumSize(QtCore.QSize(30, 0))
        self.horizontalSlider_3.setMaximumSize(QtCore.QSize(30, 16777215))
        self.horizontalSlider_3.setMinimum(1)
        self.horizontalSlider_3.setMaximum(30)
        self.horizontalSlider_3.setSliderPosition(25)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName(_fromUtf8("horizontalSlider_3"))
        self.horizontalLayout_7.addWidget(self.horizontalSlider_3)
        spacerItem22 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem22)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        spacerItem23 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem23)
        self.line_3 = QtGui.QFrame(self.tab)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.horizontalLayout_3.addWidget(self.line_3)
        spacerItem24 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem24)
        self.scrollArea = QtGui.QScrollArea(self.tab)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.\
            setGeometry(QtCore.QRect(0, 0, 218, 300))
        self.scrollAreaWidgetContents_2.\
            setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.horizontalLayout_11 =\
            QtGui.QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_11.\
            setObjectName(_fromUtf8("horizontalLayout_11"))
        self.imageLabel = QtGui.QLabel(self.scrollAreaWidgetContents_2)
        self.imageLabel.setText(_fromUtf8(""))
        self.imageLabel.setObjectName(_fromUtf8("imageLabel"))
        self.horizontalLayout_11.addWidget(self.imageLabel)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_3.addWidget(self.scrollArea)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        spacerItem25 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum,\
            QtGui.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem25)
        self.line = QtGui.QFrame(self.tab)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_3.addWidget(self.line)
        spacerItem26 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum,\
            QtGui.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem26)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem27 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem27)
        self.pushButton_2 = QtGui.QPushButton(self.tab)
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        spacerItem28 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem28)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.scrollArea_3 = QtGui.QScrollArea(self.tab_3)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName(_fromUtf8("scrollArea_3"))
        self.scrollAreaWidgetContents_3 = QtGui.QWidget()
        self.scrollAreaWidgetContents_3.\
            setGeometry(QtCore.QRect(0, 0, 758, 478))
        self.scrollAreaWidgetContents_3.\
            setObjectName(_fromUtf8("scrollAreaWidgetContents_3"))
        self.horizontalLayout_13 =\
            QtGui.QHBoxLayout(self.scrollAreaWidgetContents_3)
        self.horizontalLayout_13.\
            setObjectName(_fromUtf8("horizontalLayout_13"))
        self.imageLabel_3 = QtGui.QLabel(self.scrollAreaWidgetContents_3)
        self.imageLabel_3.setText(_fromUtf8(""))
        self.imageLabel_3.setObjectName(_fromUtf8("imageLabel_3"))
        self.horizontalLayout_13.addWidget(self.imageLabel_3)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout_9.addWidget(self.scrollArea_3)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.\
            setObjectName(_fromUtf8("horizontalLayout_12"))
        spacerItem29 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem29)
        self.radioButton_7 = QtGui.QRadioButton(self.tab_3)
        self.radioButton_7.setChecked(True)
        self.radioButton_7.setAutoExclusive(False)
        self.radioButton_7.setObjectName(_fromUtf8("radioButton_7"))
        self.horizontalLayout_12.addWidget(self.radioButton_7)
        spacerItem30 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem30)
        self.radioButton_8 = QtGui.QRadioButton(self.tab_3)
        self.radioButton_8.setAutoExclusive(False)
        self.radioButton_8.setObjectName(_fromUtf8("radioButton_8"))
        self.horizontalLayout_12.addWidget(self.radioButton_8)
        spacerItem31 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem31)
        self.pushButton_5 = QtGui.QPushButton(self.tab_3)
        self.pushButton_5.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout_12.addWidget(self.pushButton_5)
        spacerItem32 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem32)
        spacerItem33 = QtGui.QSpacerItem(100, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem33)
        self.pushButton_6 = QtGui.QPushButton(self.tab_3)
        self.pushButton_6.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.horizontalLayout_12.addWidget(self.pushButton_6)
        spacerItem34 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem34)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        self.verticalLayout_9.addLayout(self.verticalLayout_8)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.scrollArea_2 = QtGui.QScrollArea(self.tab_2)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 756, 478))
        self.scrollAreaWidgetContents.\
            setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.horizontalLayout_10 =\
            QtGui.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_10.\
            setObjectName(_fromUtf8("horizontalLayout_10"))
        self.imageLabel_2 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.imageLabel_2.setText(_fromUtf8(""))
        self.imageLabel_2.setObjectName(_fromUtf8("imageLabel_2"))
        self.horizontalLayout_10.addWidget(self.imageLabel_2)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_5.addWidget(self.scrollArea_2)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        spacerItem35 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem35)
        self.radioButton_3 = QtGui.QRadioButton(self.tab_2)
        self.radioButton_3.setChecked(True)
        self.radioButton_3.setAutoExclusive(False)
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.horizontalLayout_8.addWidget(self.radioButton_3)
        spacerItem36 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem36)
        self.radioButton_4 = QtGui.QRadioButton(self.tab_2)
        self.radioButton_4.setAutoExclusive(False)
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.horizontalLayout_8.addWidget(self.radioButton_4)
        spacerItem37 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem37)
        spacerItem38 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem38)
        self.pushButton_3 = QtGui.QPushButton(self.tab_2)
        self.pushButton_3.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_8.addWidget(self.pushButton_3)
        spacerItem39 = QtGui.QSpacerItem(100, 20, QtGui.QSizePolicy.Fixed,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem39)
        spacerItem40 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem40)
        self.radioButton_5 = QtGui.QRadioButton(self.tab_2)
        self.radioButton_5.setChecked(True)
        self.radioButton_5.setAutoExclusive(False)
        self.radioButton_5.setObjectName(_fromUtf8("radioButton_5"))
        self.horizontalLayout_8.addWidget(self.radioButton_5)
        spacerItem41 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem41)
        self.radioButton_6 = QtGui.QRadioButton(self.tab_2)
        self.radioButton_6.setAutoExclusive(False)
        self.radioButton_6.setObjectName(_fromUtf8("radioButton_6"))
        self.horizontalLayout_8.addWidget(self.radioButton_6)
        spacerItem42 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,\
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem42)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.verticalLayout_7.addLayout(self.verticalLayout_5)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL\
            (_fromUtf8("clicked()")), self.radioButton_2.toggle)
        QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL\
            (_fromUtf8("clicked()")), self.radioButton.toggle)
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL\
            (_fromUtf8("valueChanged(int)")), self.lcdNumber.display)
        QtCore.QObject.connect(self.horizontalSlider_2, QtCore.SIGNAL\
            (_fromUtf8("valueChanged(int)")), self.lcdNumber_2.display)
        QtCore.QObject.connect(self.horizontalSlider_3, QtCore.SIGNAL\
            (_fromUtf8("valueChanged(int)")), self.lcdNumber_3.display)
        QtCore.QObject.connect(self.radioButton_3, QtCore.SIGNAL\
            (_fromUtf8("clicked()")), self.radioButton_4.toggle)
        QtCore.QObject.connect(self.radioButton_4, QtCore.SIGNAL\
            (_fromUtf8("clicked()")), self.radioButton_3.toggle)
        QtCore.QObject.connect(self.radioButton_5, QtCore.SIGNAL\
            (_fromUtf8("clicked()")), self.radioButton_6.toggle)
        QtCore.QObject.connect(self.radioButton_6, QtCore.SIGNAL\
            (_fromUtf8("clicked()")), self.radioButton_5.toggle)
        QtCore.QObject.connect(self.radioButton_7, QtCore.SIGNAL\
            (_fromUtf8("clicked()")), self.radioButton_8.toggle)
        QtCore.QObject.connect(self.radioButton_8, QtCore.SIGNAL\
            (_fromUtf8("clicked()")), self.radioButton_7.toggle)
        QtCore.QObject.connect(self.tabWidget, QtCore.SIGNAL\
            (_fromUtf8("currentChanged(int)")), self.cross_msg)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL\
            (_fromUtf8("clicked()")), self.browsing)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL\
            ("clicked()"), self.go_rf)
        QtCore.QObject.connect(self.pushButton_5, QtCore.SIGNAL\
            ("clicked()"), self.go_pt)
        QtCore.QObject.connect(self.pushButton_6, QtCore.SIGNAL\
            ("clicked()"), self.go_rp)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL\
            ("clicked()"), self.go_om)
        QtCore.QObject.connect(self.radioButton_3, QtCore.SIGNAL\
            ("toggled(bool)"), self.erase_measure_points)
        QtCore.QObject.connect(self.radioButton_4, QtCore.SIGNAL\
            ("toggled(bool)"), self.erase_measure_points)
        QtCore.QObject.connect(self.radioButton_5, QtCore.SIGNAL\
            ("toggled(bool)"), self.unit_changed)
        QtCore.QObject.connect(self.radioButton_6, QtCore.SIGNAL\
            ("toggled(bool)"), self.unit_changed)
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL\
            ("clicked()"), self.undistort)
        QtCore.QMetaObject.connectSlotsByName(Form)
    
    """
    Assings the names of buttons and labels
    """
    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "RAFIPETOM", None))
        self.label.setText(_translate("Form", "Source Folder:", None))
        self.pushButton.setText(_translate("Form", "Browse", None))
        self.pushButton_4.setText(_translate("Form", "Undistort Images", None))
        self.label_2.setText(_translate("Form", "Threshold Value:", None))
        self.label_3.setText(_translate("Form", "Threshold Mode:", None))
        self.radioButton.setText(_translate("Form", "BINARY", None))
        self.radioButton_2.setText(_translate("Form", "TOZERO", None))
        self.label_4.setText(_translate("Form", "Area ratio:", None))
        self.label_6.setText(_translate("Form", "%", None))
        self.label_5.setText(_translate("Form", "Hunt range:", None))
        self.pushButton_2.setText(_translate("Form", "Run", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),
            _translate("Form", "Range Finder", None))
        self.radioButton_7.setText\
            (_translate("Form", "Src points (Blue)", None))
        self.radioButton_8.setText\
            (_translate("Form", "Dst points (Green)", None))
        self.pushButton_5.setText(_translate("Form", "Run", None))
        self.pushButton_6.setText(_translate("Form", "Reset", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), 
            _translate("Form", "Perspective Transnform", None))
        self.radioButton_3.setText(_translate("Form", "Lines", None))
        self.radioButton_4.setText(_translate("Form", "Contour", None))
        self.pushButton_3.setText(_translate("Form", "Run", None))
        self.radioButton_5.setText(_translate("Form", "m", None))
        self.radioButton_6.setText(_translate("Form", "cm", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), 
            _translate("Form", "Object Measurement", None))
    
    """
    Displays a message in "Ok" boxes
    """
    def display_message(self, icon, title, text):
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(icon)
        msgBox.setWindowTitle("RAFIPETOM: " + title)
        msgBox.setText(text)
        msgBox.exec_()
    
    """
    Uses display_message with "Error" parameters to inform
    an error, using the Critical error icon, the tittle "Error"
    and a message explaining the reason.
    """    
    def error_msgbox(self, error_msg):
        self.display_message(QtGui.QMessageBox.Critical,
            "Error!", error_msg)
    
    """
    Uses display_message with "Information" parameters to show the user
    an advice or somethig useful to know about, using Information icon,
    the tittle "Information" and the message.
    """  
    def info_msgbox(self, info):
        self.display_message(QtGui.QMessageBox.Information,
            "Information", info)
    
    """
    Asks the user a yes/no question about to proceed or not, because the
    the user is going to change data for good.
    """
    def question_box(self, question):
        return QtGui.QMessageBox.question(self, 'RAFIPETOM', question,\
            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No) ==\
                QtGui.QMessageBox.Yes
    
    """
    <Enable-Disable buttons according the state of the ui>
    """
    def running_rf_disable(self):
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_4.setEnabled(False)
    
    def rf_done_enable(self):
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        
    def disable_run_buttons(self):
        self.progressBar.reset()
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.radioButton_3.setEnabled(False)
        self.radioButton_4.setEnabled(False)
        self.radioButton_7.setEnabled(False)
        self.radioButton_8.setEnabled(False)
        self.radioButton_5.setEnabled(False)
        self.radioButton_6.setEnabled(False)
    """
    </Enable-Disable buttons according the state of the ui>
    """
    
    """
    Examinates the folder selected...
    informs if:
                - it's empty
                - No folder was selected
                - The files inside are not '.jpg" images
    otherwise enables "run" and "undistort" buttons.
    """
    def browsing(self):
        folder_path = str(QtGui.QFileDialog.\
            getExistingDirectory(self, "Select Directory"))
        self.lineEdit.setText(folder_path)
        self.folder_path = folder_path
        try: self.images_names = listdir(folder_path)
        except: 
            self.error_msgbox("Insert folder path")
            return
        if not self.images_names: self.error_msgbox("Empty Folder")
        else:
            for x in self.images_names:
                ext = what(self.folder_path + "/" + x)
                if not ext == 'jpeg':
                    self.error_msgbox("At least one file is not a .jpg image")
                    self.disable_run_buttons()
                    return
            self.pushButton_2.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.progressBar.reset()
    """
    Reads and loads the undistort parameters, if they haven't been loaded
    already. Then applys the undistort operation in every imagen (Enclosing 
    the valid area of the image)in the folder changing the files for good.
    """
    def undistort(self):
        if self.question_box("This will modify the images "\
            "within selected folder... \nProceed?"):
            self.pushButton_2.setEnabled(False)
            if self.undistort_parameters is None:
                with open("./camera_data/camera_parameters.txt", "r") as fd:
                    self.undistort_parameters =\
                        [json_to_data(line) for line in fd]
                    
            for fname in self.images_names:
                path = self.folder_path + "/" + fname
                img = cv2.imread(path)
                if img.shape != self.undistort_parameters[0]:
                    self.error_msgbox("Resolution of the images must match"\
                        " with the calibration resolution.")
                    return
                dst = cv2.undistort(img, self.undistort_parameters[1],\
                    self.undistort_parameters[2], None,\
                        self.undistort_parameters[4])
                x, y, w, h = self.undistort_parameters[3]
                cv2.line(dst, (x, y), (x + w, y), (0, 0, 255), 1)
                cv2.line(dst, (x + w, y), (x + w, y + h), (0, 0, 255), 1)
                cv2.line(dst, (x, y + h), (x + w, y + h), (0, 0, 255), 1)
                cv2.line(dst, (x, y), (x, y + h), (0, 0, 255), 1)
                cv2.imwrite(path, dst)
                self.progressBar.setValue((self.images_names.index(fname) + 1)\
                    * 100 / self.images_names.__len__())
            self.pushButton_4.setEnabled(False)
            self.pushButton_2.setEnabled(True)
    
    """
    Draws a cross in the center of the working image to inform about
    the perspective of this one.
    """
    def draw_cross(self):
        cross =  self.cal_cross_dots()
        paint_circles(self.work_raw_img, cross, (0, 255, 255))
    
    """
    A Perspective transform changes the cross. To show how the new cross
    if deformed, the yellow points must be detected and measured, then the new
    cross is drawn in the working image.
    """
    def add_cross_info(self, img):
        detected =  self.detect_cross()
        cross_info(img, detected, (self.w / 2, self.h / 2))
    
    """
    This is the function that makes the detecction of the cross. Finding
    the points filtering the yellow color, detecting the contours of the
    remaining circles, analyzes their position in order to sort them. Then
    delivers the points to the paintin function "cross_info" to draw the cross
    arms and their length
    """
    def detect_cross(self):
        def sort_cross_points(points):
            south = get_closest((self.w / 2, self.h), points)
            points.remove(south)
            east = get_closest((self.w, self.h / 2), points)
            points.remove(east)
            west = get_closest((0, self.h / 2), points)
            points.remove(west)
            return [south, east, west, points[0]]
        
        hsv_img = cv2.cvtColor(self.work_pt_img, cv2.COLOR_BGR2HSV)
        color = np.array([30, 255, 255])
        circles = round_circles_coord([cv2.minEnclosingCircle(x)
            for x in cv2.findContours(cv2.medianBlur(cv2.inRange(hsv_img,\
                color, color), 9), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]])
        return sort_cross_points([x[0] for x in circles])
    
    """
    Calculates points of the cross according the perspective. Anlizing the
    vertical and the horizontal angle rotates four vectors in the xy plane. The
    outcome is the points of the cross deformed because the inclination.
    """
    def cal_cross_dots(self):
        vangle_sign = 1
        if self.nv[1]: vangle_sign = - self.nv[1] / self.nv[1]
        hangle_sign = 1
        if self.nv[0]: hangle_sign = self.nv[0] / self.nv[0]
        cross_vecs = [[1, 0, 0], [0, 1, 0],[-1, 0, 0], [0, -1, 0]]
        cross_vecs = [np.dot(get_rot_mtx([0, 1, 0],\
            self.hangle * hangle_sign), x) for x in cross_vecs]
        cross_vecs = [np.dot(get_rot_mtx(cross_vecs[0],\
            self.vangle * vangle_sign), x) for x in cross_vecs]
        cross_vecs = [np.dot(self.px_length, x) for x in cross_vecs]
        return [((int(round(self.w / 2 + x[0])),\
            int(round(self.h / 2 - x[1]))), 5) for x in cross_vecs]
    
    """
    rf: range finder.
    Performs the detection of the projection of the laser points, shows the
    outcome:
            No error: - Distance
                      - Inclination
            Error:
                  - Can't find laser dots
                  - Can't find the triangle
    if no errors, then sets up everything for the perspective
    transform and the object measurement. 
    """
    def go_rf(self):
        self.running_rf_disable()
        if self.process is not None: self.process.terminate()
        error, r_data, img = run(self.folder_path, self.images_names,\
            self.horizontalSlider_2.value() / 100.0,\
                self.horizontalSlider.value(),\
                    self.mode_dic[self.radioButton.isChecked()],\
                        self.horizontalSlider_3.value())
        self.display_img(img, [], self.imageLabel)
        
        if error:
            self.rf_run_executed = False
            self.error_msgbox(r_data)
            self.pushButton_3.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.imageLabel_3.mousePressEvent = self.not_successfull_rf
            self.imageLabel_2.mousePressEvent = self.not_successfull_rf

        else:
            self.rf_run_executed = True
            self.nv = r_data[0]
            self.factor = r_data[1]
            self.vangle = r_data[2]
            self.hangle = r_data[3]
            self.process = r_data[4]
            self.px_length = transform(r_data[5])
            self.enable_pt()
            self.enable_om()
            self.work_raw_img = cv2.imread\
                (self.folder_path + "/" + self.images_names[0])
            self.w = self.work_raw_img.shape[1]
            self.h = self.work_raw_img.shape[0]
            self.draw_cross()
            self.work_pt_img = self.work_raw_img
            self.display_img(self.work_pt_img,\
                [self.add_cross_info], self.imageLabel_3)
            self.src_points = []
            self.dst_points = []
            self.pt_dic = {(True, False) : (self.src_points, " Src"),
                           (False, True) : (self.dst_points, " Dst")}
            self.work_om_img = self.work_raw_img
            self.display_img(self.work_raw_img, [], self.imageLabel_2)
            self.img_om_points = []
            self.imageLabel_3.mousePressEvent = self.pt_point_event
            self.imageLabel_2.mousePressEvent = self.om_point_event
        self.rf_done_enable()
            
    """
    Enables buttons for the perspective transform.
    """
    def enable_pt(self):
        self.radioButton_7.setEnabled(True)
        self.radioButton_8.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        
    """
    Enables buttons for the object measurement.    
    """    
    def enable_om(self):
        self.pushButton_3.setEnabled(True)
        self.radioButton_3.setEnabled(True)
        self.radioButton_4.setEnabled(True)
        self.radioButton_5.setEnabled(True)
        self.radioButton_6.setEnabled(True)
        
    """
    Bounded to the click event of the object perspective transform and object 
    measurement, to inform the user that to use those tabs triangle must be
    found. 
    """       
    def not_successfull_rf(self, event):
        self.error_msgbox("Triangle must be found")
    
    """
    Just draws the circles marked by the user, in order to perform the
    perspective transform.
    """    
    def draw_ptp(self, img):
        paint_circles(img, self.src_points, (255, 0, 0))
        paint_circles(img, self.dst_points, (0, 255, 0))
    
    """
    Records every click on the perspective transform image, its position
    in order to save a new one or delete if it already exists.
    """
    def pt_point_event(self, event):
        points_list, p_type = self.pt_dic[self.radioButton_7.isChecked(),\
            self.radioButton_8.isChecked()]
        pos = (event.pos().x(), event.pos().y())
        bool_tuple = is_within_circles(pos, points_list)
        if bool_tuple[0]: points_list.pop(bool_tuple[1])
        else:
            if points_list.__len__() >= 4: 
                self.error_msgbox("Four "+ p_type + " points is the limit")
            else: points_list.append((pos, 8))
        self.display_img(self.work_pt_img, [self.draw_ptp], self.imageLabel_3)
    
    """
    Informs about the shape the cross must have to ensure a decent measure.
    """
    def cross_msg(self):
        if self.tabWidget.currentIndex() == 1 and self.rf_run_executed:
            self.info_msgbox(" Cross must be perfect and arms measure "\
                + str(int(round(self.px_length))))
    
    def go_pt(self):
        def quad_sort_points(points):
            return [get_closest((0, 0), points), 
                get_closest((self.w - 1, 0), points),
                    get_closest((0, self.h - 1), points), 
                        get_closest((self.w - 1, self.h - 1), points)]
        
        if self.src_points.__len__() < 4:
            self.error_msgbox("Four Src points are needed")
            return
        if self.dst_points.__len__() < 4:
            self.error_msgbox("Four Dst points are needed")
            return
        sorted_sp = quad_sort_points([x[0] for x in self.src_points])
        sorted_dp = quad_sort_points([x[0] for x in self.dst_points])
        pts1 = np.float32([[sorted_sp[0][0], sorted_sp[0][1]], 
            [sorted_sp[1][0], sorted_sp[1][1]],
                [sorted_sp[2][0], sorted_sp[2][1]],
                    [sorted_sp[3][0], sorted_sp[3][1]]])
        pts2 = np.float32([[sorted_dp[0][0], sorted_dp[0][1]],
            [sorted_dp[1][0], sorted_dp[1][1]],
                [sorted_dp[2][0], sorted_dp[2][1]],
                    [sorted_dp[3][0], sorted_dp[3][1]]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        self.work_pt_img = cv2.warpPerspective(self.work_raw_img,
            M, (self.w, self.h))
        self.work_om_img = self.work_pt_img
        self.pushButton_6.setEnabled(True)
        self.display_img(self.work_pt_img, [self.draw_ptp,
            self.add_cross_info], self.imageLabel_3)
        self.display_img(self.work_om_img, [], self.imageLabel_2)
        self.erase_measure_points()
        
    """
    Resets to the original perspetive; PET's image.
    """
    def go_rp(self):
        self.work_pt_img = self.work_raw_img
        self.work_om_img = self.work_raw_img
        del self.src_points[:]
        del self.dst_points[:]
        self.display_img(self.work_om_img,\
            [self.add_cross_info], self.imageLabel_3)
        self.erase_measure_points()
        
    """
    Draws the simple lines or contuor due to the checked measure mode.
    """
    def draw_om(self, img):
        def draw_lines(img, size):
            for x in xrange(0, size - size % 2, 2):
                cv2.line(img, self.img_om_points[x][0],\
                    self.img_om_points[(x + 1)][0], (0, 255, 0), 3)
    
        def draw_contour(img, size):
            for x in xrange(size):
                cv2.line(img, self.img_om_points[x][0],\
                    self.img_om_points[(x + 1) % size][0], (0, 255, 0), 3)
        
        draw_om_dic = {True: draw_lines, False: draw_contour}
        f = draw_om_dic[self.radioButton_3.isChecked()]
        if self.img_om_points.__len__() > 1: 
            f(img, self.img_om_points.__len__())
        paint_circles(img, self.img_om_points, (0, 255, 0))

    """
    Saves/Deletes points for the object measurement
    """
    def om_point_event(self, event):
        pos = (event.pos().x(), event.pos().y())
        bool_tuple = is_within_circles(pos, self.img_om_points)
        if bool_tuple[0]:
            self.img_om_points.pop(bool_tuple[1])
            if self.radioButton_3.isChecked() and\
                self.img_om_points.__len__() % 2 == 1:
                    self.img_om_points.pop\
                        (bool_tuple[1] - int(bool_tuple[1] % 2 == 1))
        else: 
            self.img_om_points.append((pos, 5))
        self.display_img(self.work_om_img, [self.draw_om], self.imageLabel_2)
        self.om_run_executed = False
    
    """
    Given an image, applys on it a list of functions. Then displays it in
    the given image label.
    """
    def display_img(self, img, functs, label):
        if functs:
            cv2_img = np.copy(img)
            for x in functs:
                x(cv2_img)
        else: cv2_img = img 
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        qimg = QtGui.QImage(cv2_img.data, cv2_img.shape[1], cv2_img.shape[0],\
            QtGui.QImage.Format_RGB888)
        label.setMinimumSize(qimg.size())
        label.setPixmap(QtGui.QPixmap.fromImage(qimg))

    """
    Clears the list of points saved for the object measurement.
    """
    def erase_measure_points(self):
        if self.pushButton_2.isEnabled() and self.img_om_points:
            del self.img_om_points[:]
            self.om_run_executed = False
            self.display_img(self.work_om_img, [], self.imageLabel_2)
    
    """
    Given two numbers it returns the average value.
    """
    def avg(self, a, b):
        return (a + b) / 2
    
    """
    From the list of saved points takes pairs, and calculates the
    distance between them. Then uses the convertion factor to get mtrs measures.
    """
    def measure_lines(self, img):
        for i in xrange(0, self.img_om_points.__len__(), 2):
            x1, y1 = self.img_om_points[i][0][0], self.img_om_points[i][0][1]
            x2, y2 = self.img_om_points[i + 1][0][0],\
                self.img_om_points[i + 1][0][1]
            distance = cal_dist((x1, y1), (x2, y2)) * self.factor
            unit = " m"
            if self.radioButton_6.isChecked():
                distance = distance * 100
                unit = " cm"
            cv2.putText(img, "{0:.3f}".format(distance) + unit,\
                (int(self.avg(x1, x2)), int(self.avg(y1, y2))),\
                    cv2.FONT_HERSHEY_COMPLEX, .75, (0, 0, 255), 2)
    
    """
    The first and the last point saved in the "img_om_points" list are the
    first and the last of the closed contour. This function finds a point
    in the center then subdivide the contour into triangles in onder to 
    calculate area and perimeter. 
    """
    def measure_contour(self, img):
        px, py = zip(*[x[0] for x in self.img_om_points])
        point = (sum(px)/px.__len__(), sum(py)/py.__len__())    
        area = 0
        perimeter = 0
        for i in xrange(0, self.img_om_points.__len__()):
            x1, y1 = self.img_om_points[i][0][0], self.img_om_points[i][0][1]
            x2, y2 = self.img_om_points[(i + 1) %\
                self.img_om_points.__len__()][0][0], self.img_om_points\
                    [(i + 1) % self.img_om_points.__len__()][0][1]
            edge1 = cal_dist(( point[0], point[1]), (x1, y1)) * self.factor
            edge2 = cal_dist((x1, y1),( x2, y2)) * self.factor
            edge3 = cal_dist(( x2, y2), (point[0], point[1])) * self.factor
            sp = (edge1 + edge2 + edge3) / 2
            arg = sp * (sp - edge1) * (sp - edge2) * (sp - edge3)
            if arg > 0: area = area + arg ** 0.5
            perimeter = perimeter + edge2
        unit = " m"
        if self.radioButton_6.isChecked():
            area = area * 10000
            perimeter = perimeter * 100
            unit = " cm"
        cv2.putText(img, "Area: "+ "{0:.3f}".format(area) + unit + " x" +\
            unit, (int(point[0]) - 80, int(point[1])),\
                cv2.FONT_HERSHEY_COMPLEX, .75, (0, 0, 255), 2)
        cv2.putText(img, "Perimeter: " + "{0:.3f}".format(perimeter) + unit,\
            (int(point[0]) - 80, int(point[1]) + 30),\
                cv2.FONT_HERSHEY_COMPLEX, .75, (0, 0, 255), 2)
    
    """
    Performs the linear measures when the radioButton "lines" is checked
    otherwise measures area and perimeter of a closed contour.
    Check for the amount of points to be correct.
    """
    def go_om(self):
        if self.radioButton_3.isChecked():
            if self.img_om_points.__len__() % 2 == 1 or\
                self.img_om_points.__len__() < 1: 
                    self.error_msgbox("The number of points must be "\
                        "even\n and greater than 0")
                    return
        else:
            if self.img_om_points.__len__() < 3:
                self.error_msgbox("The number of points must be 3 (at least)") 
                return
        self.om_run_executed = True
        self.display_img(self.work_om_img, [self.draw_om,
            self.measure_dic[self.radioButton_3.isChecked()]],
                self.imageLabel_2)
        
    """
    If the unit is changed, updates the results recalculating the measures 
    """
    def unit_changed(self):
        if self.om_run_executed:
            self.display_img(self.work_om_img, [self.draw_om,
                self.measure_dic[self.radioButton_3.isChecked()]],
                    self.imageLabel_2)

    """
    shuts down the process that show the detected plane when the main
    window is closed.
    """
    def closeEvent(self, event):
        if self.process is not None:
            self.process.terminate()
