# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pack_format.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Pack_Format(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 166)
        self.console_version = QtWidgets.QComboBox(Dialog)
        self.console_version.setGeometry(QtCore.QRect(10, 40, 81, 22))
        self.console_version.setObjectName("console_version")
        self.console_version.addItem("")
        self.console_version.addItem("")
        self.type_format_pack = QtWidgets.QComboBox(Dialog)
        self.type_format_pack.setGeometry(QtCore.QRect(110, 40, 81, 22))
        self.type_format_pack.setObjectName("type_format_pack")
        self.type_format_pack.addItem("")
        self.type_format_pack.addItem("")
        self.type_format_pack.addItem("")
        self.text_pack_format = QtWidgets.QLabel(Dialog)
        self.text_pack_format.setGeometry(QtCore.QRect(10, 10, 180, 16))
        self.text_pack_format.setAlignment(QtCore.Qt.AlignCenter)
        self.text_pack_format.setObjectName("text_pack_format")
        self.accept_pack_format = QtWidgets.QPushButton(Dialog)
        self.accept_pack_format.setGeometry(QtCore.QRect(20, 130, 75, 23))
        self.accept_pack_format.setObjectName("accept_pack_format")
        self.cancel_pack_format = QtWidgets.QPushButton(Dialog)
        self.cancel_pack_format.setGeometry(QtCore.QRect(100, 130, 75, 23))
        self.cancel_pack_format.setObjectName("cancel_pack_format")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "pack format"))
        self.console_version.setItemText(0, _translate("Dialog", "PS3"))
        self.console_version.setItemText(1, _translate("Dialog", "XBOX 360"))
        self.type_format_pack.setItemText(0, _translate("Dialog", "vram/ioram"))
        self.type_format_pack.setItemText(1, _translate("Dialog", "spr"))
        self.type_format_pack.setItemText(2, _translate("Dialog", "Other"))
        self.text_pack_format.setText(_translate("Dialog", "Choose the format for packing:"))
        self.accept_pack_format.setText(_translate("Dialog", "Accept"))
        self.cancel_pack_format.setText(_translate("Dialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

