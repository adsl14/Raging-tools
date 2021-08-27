# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Raging_tools.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(952, 855)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 20, 931, 781))
        self.tabWidget.setObjectName("tabWidget")
        self.vram_explorer = QtWidgets.QWidget()
        self.vram_explorer.setObjectName("vram_explorer")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.vram_explorer)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 70, 821, 651))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listView = QtWidgets.QListView(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setObjectName("listView")
        self.horizontalLayout.addWidget(self.listView)
        self.frame = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.frame.setEnabled(True)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.imageTexture = QtWidgets.QLabel(self.frame)
        self.imageTexture.setGeometry(QtCore.QRect(40, 60, 461, 501))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageTexture.sizePolicy().hasHeightForWidth())
        self.imageTexture.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.imageTexture.setPalette(palette)
        self.imageTexture.setAutoFillBackground(False)
        self.imageTexture.setText("")
        self.imageTexture.setScaledContents(False)
        self.imageTexture.setAlignment(QtCore.Qt.AlignCenter)
        self.imageTexture.setObjectName("imageTexture")
        self.exportButton = QtWidgets.QPushButton(self.frame)
        self.exportButton.setGeometry(QtCore.QRect(370, 580, 75, 23))
        self.exportButton.setObjectName("exportButton")
        self.importButton = QtWidgets.QPushButton(self.frame)
        self.importButton.setGeometry(QtCore.QRect(450, 580, 75, 23))
        self.importButton.setObjectName("importButton")
        self.sizeImageText = QtWidgets.QLabel(self.frame)
        self.sizeImageText.setGeometry(QtCore.QRect(20, 10, 150, 16))
        self.sizeImageText.setText("")
        self.sizeImageText.setAlignment(QtCore.Qt.AlignCenter)
        self.sizeImageText.setObjectName("sizeImageText")
        self.encodingImageText = QtWidgets.QLabel(self.frame)
        self.encodingImageText.setGeometry(QtCore.QRect(379, 10, 150, 16))
        self.encodingImageText.setText("")
        self.encodingImageText.setAlignment(QtCore.Qt.AlignCenter)
        self.encodingImageText.setObjectName("encodingImageText")
        self.mipMapsImageText = QtWidgets.QLabel(self.frame)
        self.mipMapsImageText.setGeometry(QtCore.QRect(200, 10, 150, 16))
        self.mipMapsImageText.setText("")
        self.mipMapsImageText.setAlignment(QtCore.Qt.AlignCenter)
        self.mipMapsImageText.setObjectName("mipMapsImageText")
        self.horizontalLayout.addWidget(self.frame)
        self.exportAllButton = QtWidgets.QPushButton(self.vram_explorer)
        self.exportAllButton.setGeometry(QtCore.QRect(130, 40, 75, 23))
        self.exportAllButton.setObjectName("exportAllButton")
        self.fileNameText = QtWidgets.QLabel(self.vram_explorer)
        self.fileNameText.setGeometry(QtCore.QRect(40, 20, 841, 20))
        self.fileNameText.setText("")
        self.fileNameText.setAlignment(QtCore.Qt.AlignCenter)
        self.fileNameText.setObjectName("fileNameText")
        self.tabWidget.addTab(self.vram_explorer, "")
        self.character_parameters_editor = QtWidgets.QWidget()
        self.character_parameters_editor.setObjectName("character_parameters_editor")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.character_parameters_editor)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 30, 871, 701))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.horizontalLayoutWidget_2)
        self.frame_2.setAutoFillBackground(False)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.portrait = QtWidgets.QLabel(self.frame_2)
        self.portrait.setGeometry(QtCore.QRect(50, 180, 461, 461))
        self.portrait.setText("")
        self.portrait.setPixmap(QtGui.QPixmap("../character parameters editor/images/large/chara_up_chips_l_000.png"))
        self.portrait.setScaledContents(True)
        self.portrait.setObjectName("portrait")
        self.panel = QtWidgets.QFrame(self.frame_2)
        self.panel.setGeometry(QtCore.QRect(100, 480, 681, 201))
        self.panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.panel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.panel.setObjectName("panel")
        self.label_67 = QtWidgets.QLabel(self.panel)
        self.label_67.setGeometry(QtCore.QRect(40, 40, 41, 41))
        self.label_67.setText("")
        self.label_67.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_67.setScaledContents(True)
        self.label_67.setWordWrap(False)
        self.label_67.setObjectName("label_67")
        self.label_72 = QtWidgets.QLabel(self.panel)
        self.label_72.setGeometry(QtCore.QRect(40, 80, 41, 41))
        self.label_72.setText("")
        self.label_72.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_72.setScaledContents(True)
        self.label_72.setObjectName("label_72")
        self.label_71 = QtWidgets.QLabel(self.panel)
        self.label_71.setGeometry(QtCore.QRect(40, 120, 41, 41))
        self.label_71.setText("")
        self.label_71.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_71.setScaledContents(True)
        self.label_71.setObjectName("label_71")
        self.label_78 = QtWidgets.QLabel(self.panel)
        self.label_78.setGeometry(QtCore.QRect(40, 160, 41, 41))
        self.label_78.setText("")
        self.label_78.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_78.setScaledContents(True)
        self.label_78.setObjectName("label_78")
        self.label_93 = QtWidgets.QLabel(self.panel)
        self.label_93.setGeometry(QtCore.QRect(0, 120, 41, 41))
        self.label_93.setText("")
        self.label_93.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_93.setScaledContents(True)
        self.label_93.setObjectName("label_93")
        self.label_77 = QtWidgets.QLabel(self.panel)
        self.label_77.setGeometry(QtCore.QRect(80, 40, 41, 41))
        self.label_77.setText("")
        self.label_77.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_77.setScaledContents(True)
        self.label_77.setObjectName("label_77")
        self.label_66 = QtWidgets.QLabel(self.panel)
        self.label_66.setGeometry(QtCore.QRect(80, 160, 41, 41))
        self.label_66.setText("")
        self.label_66.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_66.setScaledContents(True)
        self.label_66.setObjectName("label_66")
        self.label_63 = QtWidgets.QLabel(self.panel)
        self.label_63.setGeometry(QtCore.QRect(80, 120, 41, 41))
        self.label_63.setText("")
        self.label_63.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_63.setScaledContents(True)
        self.label_63.setObjectName("label_63")
        self.label_62 = QtWidgets.QLabel(self.panel)
        self.label_62.setGeometry(QtCore.QRect(80, 80, 41, 41))
        self.label_62.setText("")
        self.label_62.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_62.setScaledContents(True)
        self.label_62.setObjectName("label_62")
        self.label_85 = QtWidgets.QLabel(self.panel)
        self.label_85.setGeometry(QtCore.QRect(120, 40, 41, 41))
        self.label_85.setText("")
        self.label_85.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_85.setScaledContents(True)
        self.label_85.setObjectName("label_85")
        self.label_76 = QtWidgets.QLabel(self.panel)
        self.label_76.setGeometry(QtCore.QRect(120, 160, 41, 41))
        self.label_76.setText("")
        self.label_76.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_76.setScaledContents(True)
        self.label_76.setObjectName("label_76")
        self.label_58 = QtWidgets.QLabel(self.panel)
        self.label_58.setGeometry(QtCore.QRect(120, 120, 41, 41))
        self.label_58.setText("")
        self.label_58.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_58.setScaledContents(True)
        self.label_58.setObjectName("label_58")
        self.label_84 = QtWidgets.QLabel(self.panel)
        self.label_84.setGeometry(QtCore.QRect(120, 80, 41, 41))
        self.label_84.setText("")
        self.label_84.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_84.setScaledContents(True)
        self.label_84.setObjectName("label_84")
        self.label_16 = QtWidgets.QLabel(self.panel)
        self.label_16.setGeometry(QtCore.QRect(160, 40, 41, 41))
        self.label_16.setText("")
        self.label_16.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_16.setScaledContents(True)
        self.label_16.setObjectName("label_16")
        self.label_74 = QtWidgets.QLabel(self.panel)
        self.label_74.setGeometry(QtCore.QRect(160, 160, 41, 41))
        self.label_74.setText("")
        self.label_74.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_74.setScaledContents(True)
        self.label_74.setObjectName("label_74")
        self.label_39 = QtWidgets.QLabel(self.panel)
        self.label_39.setGeometry(QtCore.QRect(160, 120, 41, 41))
        self.label_39.setText("")
        self.label_39.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_39.setScaledContents(True)
        self.label_39.setObjectName("label_39")
        self.label_38 = QtWidgets.QLabel(self.panel)
        self.label_38.setGeometry(QtCore.QRect(160, 80, 41, 41))
        self.label_38.setText("")
        self.label_38.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_38.setScaledContents(True)
        self.label_38.setObjectName("label_38")
        self.label_70 = QtWidgets.QLabel(self.panel)
        self.label_70.setGeometry(QtCore.QRect(200, 40, 41, 41))
        self.label_70.setText("")
        self.label_70.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_70.setScaledContents(True)
        self.label_70.setObjectName("label_70")
        self.label_21 = QtWidgets.QLabel(self.panel)
        self.label_21.setGeometry(QtCore.QRect(200, 160, 41, 41))
        self.label_21.setText("")
        self.label_21.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_21.setScaledContents(True)
        self.label_21.setObjectName("label_21")
        self.label_90 = QtWidgets.QLabel(self.panel)
        self.label_90.setGeometry(QtCore.QRect(200, 120, 41, 41))
        self.label_90.setText("")
        self.label_90.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_90.setScaledContents(True)
        self.label_90.setObjectName("label_90")
        self.label_92 = QtWidgets.QLabel(self.panel)
        self.label_92.setGeometry(QtCore.QRect(200, 80, 41, 41))
        self.label_92.setText("")
        self.label_92.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_92.setScaledContents(True)
        self.label_92.setObjectName("label_92")
        self.label_29 = QtWidgets.QLabel(self.panel)
        self.label_29.setGeometry(QtCore.QRect(240, 40, 41, 41))
        self.label_29.setText("")
        self.label_29.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_29.setScaledContents(True)
        self.label_29.setObjectName("label_29")
        self.label_36 = QtWidgets.QLabel(self.panel)
        self.label_36.setGeometry(QtCore.QRect(240, 160, 41, 41))
        self.label_36.setText("")
        self.label_36.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_36.setScaledContents(True)
        self.label_36.setObjectName("label_36")
        self.label_31 = QtWidgets.QLabel(self.panel)
        self.label_31.setGeometry(QtCore.QRect(240, 120, 41, 41))
        self.label_31.setText("")
        self.label_31.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_31.setScaledContents(True)
        self.label_31.setObjectName("label_31")
        self.label_27 = QtWidgets.QLabel(self.panel)
        self.label_27.setGeometry(QtCore.QRect(240, 80, 41, 41))
        self.label_27.setText("")
        self.label_27.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_27.setScaledContents(True)
        self.label_27.setObjectName("label_27")
        self.label_04 = QtWidgets.QLabel(self.panel)
        self.label_04.setGeometry(QtCore.QRect(280, 40, 41, 41))
        self.label_04.setText("")
        self.label_04.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_04.setScaledContents(True)
        self.label_04.setObjectName("label_04")
        self.label_73 = QtWidgets.QLabel(self.panel)
        self.label_73.setGeometry(QtCore.QRect(280, 160, 41, 41))
        self.label_73.setText("")
        self.label_73.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_73.setScaledContents(True)
        self.label_73.setObjectName("label_73")
        self.label_08 = QtWidgets.QLabel(self.panel)
        self.label_08.setGeometry(QtCore.QRect(280, 120, 41, 41))
        self.label_08.setText("")
        self.label_08.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_08.setScaledContents(True)
        self.label_08.setObjectName("label_08")
        self.label_05 = QtWidgets.QLabel(self.panel)
        self.label_05.setGeometry(QtCore.QRect(280, 80, 41, 41))
        self.label_05.setText("")
        self.label_05.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_05.setScaledContents(True)
        self.label_05.setObjectName("label_05")
        self.label_00 = QtWidgets.QLabel(self.panel)
        self.label_00.setGeometry(QtCore.QRect(320, 40, 41, 41))
        self.label_00.setText("")
        self.label_00.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_00.setScaledContents(True)
        self.label_00.setObjectName("label_00")
        self.label_24 = QtWidgets.QLabel(self.panel)
        self.label_24.setGeometry(QtCore.QRect(320, 160, 41, 41))
        self.label_24.setText("")
        self.label_24.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_24.setScaledContents(True)
        self.label_24.setObjectName("label_24")
        self.label_13 = QtWidgets.QLabel(self.panel)
        self.label_13.setGeometry(QtCore.QRect(320, 120, 41, 41))
        self.label_13.setText("")
        self.label_13.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_13.setScaledContents(True)
        self.label_13.setObjectName("label_13")
        self.label_12 = QtWidgets.QLabel(self.panel)
        self.label_12.setGeometry(QtCore.QRect(320, 80, 41, 41))
        self.label_12.setText("")
        self.label_12.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_12.setScaledContents(True)
        self.label_12.setObjectName("label_12")
        self.label_17 = QtWidgets.QLabel(self.panel)
        self.label_17.setGeometry(QtCore.QRect(360, 40, 41, 41))
        self.label_17.setText("")
        self.label_17.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_17.setScaledContents(True)
        self.label_17.setObjectName("label_17")
        self.label_15 = QtWidgets.QLabel(self.panel)
        self.label_15.setGeometry(QtCore.QRect(360, 160, 41, 41))
        self.label_15.setText("")
        self.label_15.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_15.setScaledContents(True)
        self.label_15.setObjectName("label_15")
        self.label_14 = QtWidgets.QLabel(self.panel)
        self.label_14.setGeometry(QtCore.QRect(360, 120, 41, 41))
        self.label_14.setText("")
        self.label_14.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_14.setScaledContents(True)
        self.label_14.setObjectName("label_14")
        self.label_11 = QtWidgets.QLabel(self.panel)
        self.label_11.setGeometry(QtCore.QRect(360, 80, 41, 41))
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_11.setScaledContents(True)
        self.label_11.setObjectName("label_11")
        self.label_37 = QtWidgets.QLabel(self.panel)
        self.label_37.setGeometry(QtCore.QRect(400, 40, 41, 41))
        self.label_37.setText("")
        self.label_37.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_37.setScaledContents(True)
        self.label_37.setObjectName("label_37")
        self.label_34 = QtWidgets.QLabel(self.panel)
        self.label_34.setGeometry(QtCore.QRect(400, 160, 41, 41))
        self.label_34.setText("")
        self.label_34.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_34.setScaledContents(True)
        self.label_34.setObjectName("label_34")
        self.label_88 = QtWidgets.QLabel(self.panel)
        self.label_88.setGeometry(QtCore.QRect(400, 120, 41, 41))
        self.label_88.setText("")
        self.label_88.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_88.setScaledContents(True)
        self.label_88.setObjectName("label_88")
        self.label_22 = QtWidgets.QLabel(self.panel)
        self.label_22.setGeometry(QtCore.QRect(400, 80, 41, 41))
        self.label_22.setText("")
        self.label_22.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_22.setScaledContents(True)
        self.label_22.setObjectName("label_22")
        self.label_48 = QtWidgets.QLabel(self.panel)
        self.label_48.setGeometry(QtCore.QRect(440, 40, 41, 41))
        self.label_48.setText("")
        self.label_48.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_48.setScaledContents(True)
        self.label_48.setObjectName("label_48")
        self.label_81 = QtWidgets.QLabel(self.panel)
        self.label_81.setGeometry(QtCore.QRect(440, 160, 41, 41))
        self.label_81.setText("")
        self.label_81.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_81.setScaledContents(True)
        self.label_81.setObjectName("label_81")
        self.label_79 = QtWidgets.QLabel(self.panel)
        self.label_79.setGeometry(QtCore.QRect(440, 120, 41, 41))
        self.label_79.setText("")
        self.label_79.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_79.setScaledContents(True)
        self.label_79.setObjectName("label_79")
        self.label_82 = QtWidgets.QLabel(self.panel)
        self.label_82.setGeometry(QtCore.QRect(440, 80, 41, 41))
        self.label_82.setText("")
        self.label_82.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_82.setScaledContents(True)
        self.label_82.setObjectName("label_82")
        self.label_43 = QtWidgets.QLabel(self.panel)
        self.label_43.setGeometry(QtCore.QRect(480, 40, 41, 41))
        self.label_43.setText("")
        self.label_43.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_43.setScaledContents(True)
        self.label_43.setObjectName("label_43")
        self.label_46 = QtWidgets.QLabel(self.panel)
        self.label_46.setGeometry(QtCore.QRect(480, 160, 41, 41))
        self.label_46.setText("")
        self.label_46.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_46.setScaledContents(True)
        self.label_46.setObjectName("label_46")
        self.label_45 = QtWidgets.QLabel(self.panel)
        self.label_45.setGeometry(QtCore.QRect(480, 120, 41, 41))
        self.label_45.setText("")
        self.label_45.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_45.setScaledContents(True)
        self.label_45.setObjectName("label_45")
        self.label_44 = QtWidgets.QLabel(self.panel)
        self.label_44.setGeometry(QtCore.QRect(480, 80, 41, 41))
        self.label_44.setText("")
        self.label_44.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_44.setScaledContents(True)
        self.label_44.setObjectName("label_44")
        self.label_47 = QtWidgets.QLabel(self.panel)
        self.label_47.setGeometry(QtCore.QRect(520, 40, 41, 41))
        self.label_47.setText("")
        self.label_47.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_47.setScaledContents(True)
        self.label_47.setObjectName("label_47")
        self.label_98 = QtWidgets.QLabel(self.panel)
        self.label_98.setGeometry(QtCore.QRect(520, 160, 41, 41))
        self.label_98.setText("")
        self.label_98.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_98.setScaledContents(True)
        self.label_98.setObjectName("label_98")
        self.label_97 = QtWidgets.QLabel(self.panel)
        self.label_97.setGeometry(QtCore.QRect(520, 120, 41, 41))
        self.label_97.setText("")
        self.label_97.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_97.setScaledContents(True)
        self.label_97.setObjectName("label_97")
        self.label_96 = QtWidgets.QLabel(self.panel)
        self.label_96.setGeometry(QtCore.QRect(520, 80, 41, 41))
        self.label_96.setText("")
        self.label_96.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_96.setScaledContents(True)
        self.label_96.setObjectName("label_96")
        self.label_91 = QtWidgets.QLabel(self.panel)
        self.label_91.setGeometry(QtCore.QRect(560, 40, 41, 41))
        self.label_91.setText("")
        self.label_91.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_91.setScaledContents(True)
        self.label_91.setObjectName("label_91")
        self.label_87 = QtWidgets.QLabel(self.panel)
        self.label_87.setGeometry(QtCore.QRect(560, 160, 41, 41))
        self.label_87.setText("")
        self.label_87.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_87.setScaledContents(True)
        self.label_87.setObjectName("label_87")
        self.label_42 = QtWidgets.QLabel(self.panel)
        self.label_42.setGeometry(QtCore.QRect(560, 120, 41, 41))
        self.label_42.setText("")
        self.label_42.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_42.setScaledContents(True)
        self.label_42.setObjectName("label_42")
        self.label_40 = QtWidgets.QLabel(self.panel)
        self.label_40.setGeometry(QtCore.QRect(560, 80, 41, 41))
        self.label_40.setText("")
        self.label_40.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_40.setScaledContents(True)
        self.label_40.setObjectName("label_40")
        self.label_54 = QtWidgets.QLabel(self.panel)
        self.label_54.setGeometry(QtCore.QRect(600, 40, 41, 41))
        self.label_54.setText("")
        self.label_54.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_54.setScaledContents(True)
        self.label_54.setObjectName("label_54")
        self.label_57 = QtWidgets.QLabel(self.panel)
        self.label_57.setGeometry(QtCore.QRect(600, 160, 41, 41))
        self.label_57.setText("")
        self.label_57.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_57.setScaledContents(True)
        self.label_57.setObjectName("label_57")
        self.label_56 = QtWidgets.QLabel(self.panel)
        self.label_56.setGeometry(QtCore.QRect(600, 120, 41, 41))
        self.label_56.setText("")
        self.label_56.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_56.setScaledContents(True)
        self.label_56.setObjectName("label_56")
        self.label_55 = QtWidgets.QLabel(self.panel)
        self.label_55.setGeometry(QtCore.QRect(600, 80, 41, 41))
        self.label_55.setText("")
        self.label_55.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_55.setScaledContents(True)
        self.label_55.setObjectName("label_55")
        self.label_99 = QtWidgets.QLabel(self.panel)
        self.label_99.setGeometry(QtCore.QRect(640, 120, 41, 41))
        self.label_99.setText("")
        self.label_99.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_99.setScaledContents(True)
        self.label_99.setObjectName("label_99")
        self.label_trans_0 = QtWidgets.QLabel(self.panel)
        self.label_trans_0.setGeometry(QtCore.QRect(280, 0, 41, 41))
        self.label_trans_0.setText("")
        self.label_trans_0.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_trans_0.setScaledContents(True)
        self.label_trans_0.setObjectName("label_trans_0")
        self.label_trans_1 = QtWidgets.QLabel(self.panel)
        self.label_trans_1.setGeometry(QtCore.QRect(240, 0, 41, 41))
        self.label_trans_1.setText("")
        self.label_trans_1.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_trans_1.setScaledContents(True)
        self.label_trans_1.setObjectName("label_trans_1")
        self.label_trans_2 = QtWidgets.QLabel(self.panel)
        self.label_trans_2.setGeometry(QtCore.QRect(200, 0, 41, 41))
        self.label_trans_2.setText("")
        self.label_trans_2.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_trans_2.setScaledContents(True)
        self.label_trans_2.setObjectName("label_trans_2")
        self.label_trans_3 = QtWidgets.QLabel(self.panel)
        self.label_trans_3.setGeometry(QtCore.QRect(160, 0, 41, 41))
        self.label_trans_3.setText("")
        self.label_trans_3.setPixmap(QtGui.QPixmap("../character parameters editor/images/small/sc_chara_000.bmp"))
        self.label_trans_3.setScaledContents(True)
        self.label_trans_3.setObjectName("label_trans_3")
        self.panel2 = QtWidgets.QFrame(self.frame_2)
        self.panel2.setGeometry(QtCore.QRect(430, 20, 191, 221))
        self.panel2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.panel2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.panel2.setObjectName("panel2")
        self.transPanel = QtWidgets.QLabel(self.panel2)
        self.transPanel.setGeometry(QtCore.QRect(-36, -10, 251, 231))
        self.transPanel.setText("")
        self.transPanel.setPixmap(QtGui.QPixmap("../character parameters editor/images/fourSlot/pl_transform.png"))
        self.transPanel.setScaledContents(False)
        self.transPanel.setObjectName("transPanel")
        self.transSlotPanel0 = QtWidgets.QLabel(self.panel2)
        self.transSlotPanel0.setEnabled(True)
        self.transSlotPanel0.setGeometry(QtCore.QRect(28, 75, 61, 61))
        self.transSlotPanel0.setText("")
        self.transSlotPanel0.setPixmap(QtGui.QPixmap("../character parameters editor/images/fourSlot/small/sc_chara_s_000.png"))
        self.transSlotPanel0.setScaledContents(False)
        self.transSlotPanel0.setObjectName("transSlotPanel0")
        self.transSlotPanel1 = QtWidgets.QLabel(self.panel2)
        self.transSlotPanel1.setGeometry(QtCore.QRect(60, 43, 61, 61))
        self.transSlotPanel1.setText("")
        self.transSlotPanel1.setPixmap(QtGui.QPixmap("../character parameters editor/images/fourSlot/small/sc_chara_s_000.png"))
        self.transSlotPanel1.setScaledContents(False)
        self.transSlotPanel1.setObjectName("transSlotPanel1")
        self.transSlotPanel2 = QtWidgets.QLabel(self.panel2)
        self.transSlotPanel2.setGeometry(QtCore.QRect(94, 75, 61, 61))
        self.transSlotPanel2.setText("")
        self.transSlotPanel2.setPixmap(QtGui.QPixmap("../character parameters editor/images/fourSlot/small/sc_chara_s_000.png"))
        self.transSlotPanel2.setScaledContents(False)
        self.transSlotPanel2.setObjectName("transSlotPanel2")
        self.transSlotPanel3 = QtWidgets.QLabel(self.panel2)
        self.transSlotPanel3.setGeometry(QtCore.QRect(60, 110, 61, 61))
        self.transSlotPanel3.setText("")
        self.transSlotPanel3.setPixmap(QtGui.QPixmap("../character parameters editor/images/fourSlot/small/sc_chara_s_000.png"))
        self.transSlotPanel3.setScaledContents(False)
        self.transSlotPanel3.setObjectName("transSlotPanel3")
        self.transText = QtWidgets.QLabel(self.panel2)
        self.transText.setGeometry(QtCore.QRect(26, 10, 131, 21))
        self.transText.setText("")
        self.transText.setPixmap(QtGui.QPixmap("../character parameters editor/images/fourSlot/tx_transform_US.png"))
        self.transText.setScaledContents(True)
        self.transText.setObjectName("transText")
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.tabWidget.addTab(self.character_parameters_editor, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 952, 26))
        self.menubar.setObjectName("menubar")
        self.menuFIle = QtWidgets.QMenu(self.menubar)
        self.menuFIle.setObjectName("menuFIle")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionAuthor = QtWidgets.QAction(MainWindow)
        self.actionAuthor.setObjectName("actionAuthor")
        self.actionCredits = QtWidgets.QAction(MainWindow)
        self.actionCredits.setObjectName("actionCredits")
        self.menuFIle.addAction(self.actionOpen)
        self.menuFIle.addAction(self.actionSave)
        self.menuFIle.addAction(self.actionClose)
        self.menuAbout.addAction(self.actionAuthor)
        self.menuAbout.addAction(self.actionCredits)
        self.menubar.addAction(self.menuFIle.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Raging tools 1.0"))
        self.exportButton.setText(_translate("MainWindow", "E&xport..."))
        self.importButton.setText(_translate("MainWindow", "I&mport..."))
        self.exportAllButton.setText(_translate("MainWindow", "Export all"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.vram_explorer), _translate("MainWindow", "vram explorer"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.character_parameters_editor), _translate("MainWindow", "character parameters editor"))
        self.menuFIle.setTitle(_translate("MainWindow", "&File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionOpen.setText(_translate("MainWindow", "O&pen..."))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionClose.setText(_translate("MainWindow", "&Exit"))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionAuthor.setText(_translate("MainWindow", "A&uthor"))
        self.actionAuthor.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionCredits.setText(_translate("MainWindow", "C&redits"))
        self.actionCredits.setShortcut(_translate("MainWindow", "Ctrl+C"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
