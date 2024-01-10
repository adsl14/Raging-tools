# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'output_format.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Output_Format(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(252, 191)
        self.console_version = QtWidgets.QComboBox(Dialog)
        self.console_version.setGeometry(QtCore.QRect(10, 60, 111, 22))
        self.console_version.setObjectName("console_version")
        self.console_version.addItem("")
        self.console_version.addItem("")
        self.type_format_pack = QtWidgets.QComboBox(Dialog)
        self.type_format_pack.setGeometry(QtCore.QRect(70, 110, 111, 22))
        self.type_format_pack.setObjectName("type_format_pack")
        self.type_format_pack.addItem("")
        self.type_format_pack.addItem("")
        self.type_format_pack.addItem("")
        self.text_pack_format = QtWidgets.QLabel(Dialog)
        self.text_pack_format.setGeometry(QtCore.QRect(10, 10, 231, 20))
        self.text_pack_format.setAlignment(QtCore.Qt.AlignCenter)
        self.text_pack_format.setObjectName("text_pack_format")
        self.accept_pack_format = QtWidgets.QPushButton(Dialog)
        self.accept_pack_format.setGeometry(QtCore.QRect(40, 150, 75, 23))
        self.accept_pack_format.setObjectName("accept_pack_format")
        self.cancel_pack_format = QtWidgets.QPushButton(Dialog)
        self.cancel_pack_format.setGeometry(QtCore.QRect(140, 150, 75, 23))
        self.cancel_pack_format.setObjectName("cancel_pack_format")
        self.type_game = QtWidgets.QComboBox(Dialog)
        self.type_game.setGeometry(QtCore.QRect(130, 60, 111, 22))
        self.type_game.setObjectName("type_game")
        self.type_game.addItem("")
        self.type_game.addItem("")
        self.console_version_text = QtWidgets.QLabel(Dialog)
        self.console_version_text.setGeometry(QtCore.QRect(16, 40, 101, 20))
        self.console_version_text.setAlignment(QtCore.Qt.AlignCenter)
        self.console_version_text.setObjectName("console_version_text")
        self.type_game_text = QtWidgets.QLabel(Dialog)
        self.type_game_text.setGeometry(QtCore.QRect(136, 40, 101, 20))
        self.type_game_text.setAlignment(QtCore.Qt.AlignCenter)
        self.type_game_text.setObjectName("type_game_text")
        self.type_format_pack_text = QtWidgets.QLabel(Dialog)
        self.type_format_pack_text.setGeometry(QtCore.QRect(76, 90, 101, 20))
        self.type_format_pack_text.setAlignment(QtCore.Qt.AlignCenter)
        self.type_format_pack_text.setObjectName("type_format_pack_text")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "output format"))
        self.console_version.setItemText(0, _translate("Dialog", "PS3"))
        self.console_version.setItemText(1, _translate("Dialog", "XBOX 360"))
        self.type_format_pack.setItemText(0, _translate("Dialog", "vram / ioram"))
        self.type_format_pack.setItemText(1, _translate("Dialog", "spr (character)"))
        self.type_format_pack.setItemText(2, _translate("Dialog", "Other"))
        self.text_pack_format.setText(_translate("Dialog", "Choose the output format:"))
        self.accept_pack_format.setText(_translate("Dialog", "Accept"))
        self.cancel_pack_format.setText(_translate("Dialog", "Cancel"))
        self.type_game.setItemText(0, _translate("Dialog", "Raging Blast 1 & 2"))
        self.type_game.setItemText(1, _translate("Dialog", "Ultimate Tenkaichi"))
        self.console_version_text.setToolTip(_translate("Dialog", "<html><head/><body><p>Select the console version you want to pack the data</p></body></html>"))
        self.console_version_text.setText(_translate("Dialog", "Console"))
        self.type_game_text.setToolTip(_translate("Dialog", "<html><head/><body><p>Select the game you want to pack the data</p></body></html>"))
        self.type_game_text.setText(_translate("Dialog", "Game"))
        self.type_format_pack_text.setToolTip(_translate("Dialog", "<html><head/>\n"
"<body>\n"
"<p>Select the type of zpak you\'re trying to pack. In order to select the proper one, follow these rules:</p>\n"
"<ul>\n"
"<li> vram / ioram -> select this type when the original zpak <b>only</b> have vram <b>or</b> ioram files. </li>\n"
"<li> spr -> select this type when the original zpak is from a spr of a character who has his vram and ioram in their separated correspond zpak files.</li>\n"
"<li> Other -> select this type when the conditions explained in the previous options aren\'t applied.</li>\n"
"</ul></body></html>"))
        self.type_format_pack_text.setText(_translate("Dialog", "Type zpak"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

