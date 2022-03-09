# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'material_children.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Material_Child_Editor(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(463, 580)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.save_material_button = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_material_button.sizePolicy().hasHeightForWidth())
        self.save_material_button.setSizePolicy(sizePolicy)
        self.save_material_button.setObjectName("save_material_button")
        self.horizontalLayout.addWidget(self.save_material_button)
        self.cancel_material_button = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_material_button.sizePolicy().hasHeightForWidth())
        self.cancel_material_button.setSizePolicy(sizePolicy)
        self.cancel_material_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cancel_material_button.setObjectName("cancel_material_button")
        self.horizontalLayout.addWidget(self.cancel_material_button)
        self.gridLayout_2.addWidget(self.frame, 6, 2, 1, 1)
        self.brightness_glow = QtWidgets.QFrame(Dialog)
        self.brightness_glow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.brightness_glow.setFrameShadow(QtWidgets.QFrame.Raised)
        self.brightness_glow.setObjectName("brightness_glow")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.brightness_glow)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.brightness_glow_slider = QtWidgets.QSlider(self.brightness_glow)
        self.brightness_glow_slider.setMaximum(100)
        self.brightness_glow_slider.setOrientation(QtCore.Qt.Horizontal)
        self.brightness_glow_slider.setObjectName("brightness_glow_slider")
        self.gridLayout_7.addWidget(self.brightness_glow_slider, 1, 0, 1, 1)
        self.brightness_glow_value = QtWidgets.QSpinBox(self.brightness_glow)
        self.brightness_glow_value.setAlignment(QtCore.Qt.AlignCenter)
        self.brightness_glow_value.setMaximum(100)
        self.brightness_glow_value.setObjectName("brightness_glow_value")
        self.gridLayout_7.addWidget(self.brightness_glow_value, 1, 1, 1, 1)
        self.brightness_glow_text = QtWidgets.QLabel(self.brightness_glow)
        self.brightness_glow_text.setAlignment(QtCore.Qt.AlignCenter)
        self.brightness_glow_text.setObjectName("brightness_glow_text")
        self.gridLayout_7.addWidget(self.brightness_glow_text, 0, 0, 1, 2)
        self.gridLayout_2.addWidget(self.brightness_glow, 2, 2, 1, 1)
        self.brightness_base = QtWidgets.QFrame(Dialog)
        self.brightness_base.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.brightness_base.setFrameShadow(QtWidgets.QFrame.Raised)
        self.brightness_base.setObjectName("brightness_base")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.brightness_base)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.brightness_base_value = QtWidgets.QSpinBox(self.brightness_base)
        self.brightness_base_value.setAlignment(QtCore.Qt.AlignCenter)
        self.brightness_base_value.setMaximum(100)
        self.brightness_base_value.setObjectName("brightness_base_value")
        self.gridLayout_6.addWidget(self.brightness_base_value, 1, 1, 1, 1)
        self.brightness_base_value_2 = QtWidgets.QSlider(self.brightness_base)
        self.brightness_base_value_2.setMaximum(100)
        self.brightness_base_value_2.setOrientation(QtCore.Qt.Horizontal)
        self.brightness_base_value_2.setObjectName("brightness_base_value_2")
        self.gridLayout_6.addWidget(self.brightness_base_value_2, 1, 0, 1, 1)
        self.brightness_base_text = QtWidgets.QLabel(self.brightness_base)
        self.brightness_base_text.setAlignment(QtCore.Qt.AlignCenter)
        self.brightness_base_text.setObjectName("brightness_base_text")
        self.gridLayout_6.addWidget(self.brightness_base_text, 0, 0, 1, 2)
        self.gridLayout_2.addWidget(self.brightness_base, 2, 1, 1, 1)
        self.shadow_orienation = QtWidgets.QFrame(Dialog)
        self.shadow_orienation.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.shadow_orienation.setFrameShadow(QtWidgets.QFrame.Raised)
        self.shadow_orienation.setObjectName("shadow_orienation")
        self.gridLayout = QtWidgets.QGridLayout(self.shadow_orienation)
        self.gridLayout.setContentsMargins(11, -1, -1, 11)
        self.gridLayout.setObjectName("gridLayout")
        self.shadow_orienation_slider = QtWidgets.QSlider(self.shadow_orienation)
        self.shadow_orienation_slider.setMinimum(-100)
        self.shadow_orienation_slider.setMaximum(100)
        self.shadow_orienation_slider.setPageStep(10)
        self.shadow_orienation_slider.setProperty("value", 0)
        self.shadow_orienation_slider.setOrientation(QtCore.Qt.Horizontal)
        self.shadow_orienation_slider.setObjectName("shadow_orienation_slider")
        self.gridLayout.addWidget(self.shadow_orienation_slider, 2, 0, 1, 1)
        self.shadow_orienation_value = QtWidgets.QSpinBox(self.shadow_orienation)
        self.shadow_orienation_value.setAlignment(QtCore.Qt.AlignCenter)
        self.shadow_orienation_value.setMinimum(-100)
        self.shadow_orienation_value.setMaximum(100)
        self.shadow_orienation_value.setObjectName("shadow_orienation_value")
        self.gridLayout.addWidget(self.shadow_orienation_value, 2, 1, 1, 1)
        self.shadow_orienation_text = QtWidgets.QLabel(self.shadow_orienation)
        self.shadow_orienation_text.setAlignment(QtCore.Qt.AlignCenter)
        self.shadow_orienation_text.setObjectName("shadow_orienation_text")
        self.gridLayout.addWidget(self.shadow_orienation_text, 0, 0, 1, 2)
        self.gridLayout_2.addWidget(self.shadow_orienation, 0, 1, 1, 1)
        self.saturation_base = QtWidgets.QFrame(Dialog)
        self.saturation_base.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.saturation_base.setFrameShadow(QtWidgets.QFrame.Raised)
        self.saturation_base.setObjectName("saturation_base")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.saturation_base)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.saturation_base_slider = QtWidgets.QSlider(self.saturation_base)
        self.saturation_base_slider.setMaximum(100)
        self.saturation_base_slider.setOrientation(QtCore.Qt.Horizontal)
        self.saturation_base_slider.setObjectName("saturation_base_slider")
        self.gridLayout_5.addWidget(self.saturation_base_slider, 1, 0, 1, 1)
        self.saturation_base_text = QtWidgets.QLabel(self.saturation_base)
        self.saturation_base_text.setAlignment(QtCore.Qt.AlignCenter)
        self.saturation_base_text.setObjectName("saturation_base_text")
        self.gridLayout_5.addWidget(self.saturation_base_text, 0, 0, 1, 2)
        self.saturation_base_value = QtWidgets.QSpinBox(self.saturation_base)
        self.saturation_base_value.setAlignment(QtCore.Qt.AlignCenter)
        self.saturation_base_value.setMaximum(100)
        self.saturation_base_value.setObjectName("saturation_base_value")
        self.gridLayout_5.addWidget(self.saturation_base_value, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.saturation_base, 1, 1, 1, 1)
        self.saturation_glow = QtWidgets.QFrame(Dialog)
        self.saturation_glow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.saturation_glow.setFrameShadow(QtWidgets.QFrame.Raised)
        self.saturation_glow.setObjectName("saturation_glow")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.saturation_glow)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.saturation_glow_slider = QtWidgets.QSlider(self.saturation_glow)
        self.saturation_glow_slider.setMaximum(100)
        self.saturation_glow_slider.setOrientation(QtCore.Qt.Horizontal)
        self.saturation_glow_slider.setObjectName("saturation_glow_slider")
        self.gridLayout_4.addWidget(self.saturation_glow_slider, 1, 0, 1, 1)
        self.saturation_glow_value = QtWidgets.QSpinBox(self.saturation_glow)
        self.saturation_glow_value.setAlignment(QtCore.Qt.AlignCenter)
        self.saturation_glow_value.setMaximum(100)
        self.saturation_glow_value.setObjectName("saturation_glow_value")
        self.gridLayout_4.addWidget(self.saturation_glow_value, 1, 1, 1, 1)
        self.saturation_glow_text = QtWidgets.QLabel(self.saturation_glow)
        self.saturation_glow_text.setAlignment(QtCore.Qt.AlignCenter)
        self.saturation_glow_text.setObjectName("saturation_glow_text")
        self.gridLayout_4.addWidget(self.saturation_glow_text, 0, 0, 1, 2)
        self.gridLayout_2.addWidget(self.saturation_glow, 1, 2, 1, 1)
        self.border_color = QtWidgets.QFrame(Dialog)
        self.border_color.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.border_color.sizePolicy().hasHeightForWidth())
        self.border_color.setSizePolicy(sizePolicy)
        self.border_color.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.border_color.setFrameShadow(QtWidgets.QFrame.Raised)
        self.border_color.setObjectName("border_color")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.border_color)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.border_color_G = QtWidgets.QLabel(self.border_color)
        self.border_color_G.setAlignment(QtCore.Qt.AlignCenter)
        self.border_color_G.setObjectName("border_color_G")
        self.gridLayout_8.addWidget(self.border_color_G, 11, 0, 1, 1)
        self.border_color_R_slider = QtWidgets.QSlider(self.border_color)
        self.border_color_R_slider.setMaximum(255)
        self.border_color_R_slider.setSingleStep(1)
        self.border_color_R_slider.setOrientation(QtCore.Qt.Horizontal)
        self.border_color_R_slider.setObjectName("border_color_R_slider")
        self.gridLayout_8.addWidget(self.border_color_R_slider, 9, 0, 1, 1)
        self.border_color_R_value = QtWidgets.QSpinBox(self.border_color)
        self.border_color_R_value.setAlignment(QtCore.Qt.AlignCenter)
        self.border_color_R_value.setMaximum(255)
        self.border_color_R_value.setObjectName("border_color_R_value")
        self.gridLayout_8.addWidget(self.border_color_R_value, 9, 1, 1, 1)
        self.border_color_A_value = QtWidgets.QSpinBox(self.border_color)
        self.border_color_A_value.setAlignment(QtCore.Qt.AlignCenter)
        self.border_color_A_value.setMaximum(255)
        self.border_color_A_value.setObjectName("border_color_A_value")
        self.gridLayout_8.addWidget(self.border_color_A_value, 16, 1, 1, 1)
        self.border_color_B_value = QtWidgets.QSpinBox(self.border_color)
        self.border_color_B_value.setAlignment(QtCore.Qt.AlignCenter)
        self.border_color_B_value.setMaximum(255)
        self.border_color_B_value.setObjectName("border_color_B_value")
        self.gridLayout_8.addWidget(self.border_color_B_value, 14, 1, 1, 1)
        self.border_color_A_slider = QtWidgets.QSlider(self.border_color)
        self.border_color_A_slider.setMaximum(255)
        self.border_color_A_slider.setSingleStep(1)
        self.border_color_A_slider.setOrientation(QtCore.Qt.Horizontal)
        self.border_color_A_slider.setObjectName("border_color_A_slider")
        self.gridLayout_8.addWidget(self.border_color_A_slider, 16, 0, 1, 1)
        self.border_color_G_slider = QtWidgets.QSlider(self.border_color)
        self.border_color_G_slider.setMaximum(255)
        self.border_color_G_slider.setSingleStep(1)
        self.border_color_G_slider.setOrientation(QtCore.Qt.Horizontal)
        self.border_color_G_slider.setObjectName("border_color_G_slider")
        self.gridLayout_8.addWidget(self.border_color_G_slider, 12, 0, 1, 1)
        self.border_color_B = QtWidgets.QLabel(self.border_color)
        self.border_color_B.setAlignment(QtCore.Qt.AlignCenter)
        self.border_color_B.setObjectName("border_color_B")
        self.gridLayout_8.addWidget(self.border_color_B, 13, 0, 1, 1)
        self.border_color_G_value = QtWidgets.QSpinBox(self.border_color)
        self.border_color_G_value.setAlignment(QtCore.Qt.AlignCenter)
        self.border_color_G_value.setMaximum(255)
        self.border_color_G_value.setObjectName("border_color_G_value")
        self.gridLayout_8.addWidget(self.border_color_G_value, 12, 1, 1, 1)
        self.border_color_B_slider = QtWidgets.QSlider(self.border_color)
        self.border_color_B_slider.setMaximum(255)
        self.border_color_B_slider.setSingleStep(1)
        self.border_color_B_slider.setOrientation(QtCore.Qt.Horizontal)
        self.border_color_B_slider.setObjectName("border_color_B_slider")
        self.gridLayout_8.addWidget(self.border_color_B_slider, 14, 0, 1, 1)
        self.border_color_A = QtWidgets.QLabel(self.border_color)
        self.border_color_A.setAlignment(QtCore.Qt.AlignCenter)
        self.border_color_A.setObjectName("border_color_A")
        self.gridLayout_8.addWidget(self.border_color_A, 15, 0, 1, 1)
        self.border_color_text = QtWidgets.QLabel(self.border_color)
        self.border_color_text.setAlignment(QtCore.Qt.AlignCenter)
        self.border_color_text.setObjectName("border_color_text")
        self.gridLayout_8.addWidget(self.border_color_text, 3, 0, 1, 2)
        self.border_color_R = QtWidgets.QLabel(self.border_color)
        self.border_color_R.setAlignment(QtCore.Qt.AlignCenter)
        self.border_color_R.setObjectName("border_color_R")
        self.gridLayout_8.addWidget(self.border_color_R, 7, 0, 1, 1)
        self.border_color_color = QtWidgets.QLabel(self.border_color)
        self.border_color_color.setAutoFillBackground(False)
        self.border_color_color.setStyleSheet("background-color: rgba(0, 0, 0, 255);")
        self.border_color_color.setFrameShadow(QtWidgets.QFrame.Plain)
        self.border_color_color.setLineWidth(1)
        self.border_color_color.setText("")
        self.border_color_color.setObjectName("border_color_color")
        self.gridLayout_8.addWidget(self.border_color_color, 4, 0, 2, 2)
        self.gridLayout_2.addWidget(self.border_color, 3, 1, 1, 1)
        self.light_orientation_glow = QtWidgets.QFrame(Dialog)
        self.light_orientation_glow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.light_orientation_glow.setFrameShadow(QtWidgets.QFrame.Raised)
        self.light_orientation_glow.setObjectName("light_orientation_glow")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.light_orientation_glow)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.light_orientation_glow_slider = QtWidgets.QSlider(self.light_orientation_glow)
        self.light_orientation_glow_slider.setMinimum(-100)
        self.light_orientation_glow_slider.setMaximum(100)
        self.light_orientation_glow_slider.setOrientation(QtCore.Qt.Horizontal)
        self.light_orientation_glow_slider.setObjectName("light_orientation_glow_slider")
        self.gridLayout_3.addWidget(self.light_orientation_glow_slider, 1, 0, 1, 1)
        self.light_orientation_glow_value = QtWidgets.QSpinBox(self.light_orientation_glow)
        self.light_orientation_glow_value.setAlignment(QtCore.Qt.AlignCenter)
        self.light_orientation_glow_value.setMinimum(-100)
        self.light_orientation_glow_value.setMaximum(100)
        self.light_orientation_glow_value.setObjectName("light_orientation_glow_value")
        self.gridLayout_3.addWidget(self.light_orientation_glow_value, 1, 1, 1, 1)
        self.light_orientation_glow_text = QtWidgets.QLabel(self.light_orientation_glow)
        self.light_orientation_glow_text.setAlignment(QtCore.Qt.AlignCenter)
        self.light_orientation_glow_text.setObjectName("light_orientation_glow_text")
        self.gridLayout_3.addWidget(self.light_orientation_glow_text, 0, 0, 1, 2)
        self.gridLayout_2.addWidget(self.light_orientation_glow, 0, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.shadow_orienation_value.valueChanged['int'].connect(self.shadow_orienation_slider.setValue)
        self.shadow_orienation_slider.valueChanged['int'].connect(self.shadow_orienation_value.setValue)
        self.light_orientation_glow_slider.valueChanged['int'].connect(self.light_orientation_glow_value.setValue)
        self.light_orientation_glow_value.valueChanged['int'].connect(self.light_orientation_glow_slider.setValue)
        self.saturation_base_slider.valueChanged['int'].connect(self.saturation_base_value.setValue)
        self.saturation_glow_value.valueChanged['int'].connect(self.saturation_glow_slider.setValue)
        self.brightness_glow_value.valueChanged['int'].connect(self.brightness_glow_slider.setValue)
        self.brightness_glow_slider.valueChanged['int'].connect(self.brightness_glow_value.setValue)
        self.brightness_base_value.valueChanged['int'].connect(self.brightness_base_value_2.setValue)
        self.brightness_base_value_2.valueChanged['int'].connect(self.brightness_base_value.setValue)
        self.border_color_A_value.valueChanged['int'].connect(self.border_color_A_slider.setValue)
        self.border_color_A_slider.valueChanged['int'].connect(self.border_color_A_value.setValue)
        self.saturation_base_value.valueChanged['int'].connect(self.saturation_base_slider.setValue)
        self.saturation_glow_slider.valueChanged['int'].connect(self.saturation_glow_value.setValue)
        self.border_color_R_slider.valueChanged['int'].connect(self.border_color_R_value.setValue)
        self.border_color_B_slider.valueChanged['int'].connect(self.border_color_B_value.setValue)
        self.border_color_G_slider.valueChanged['int'].connect(self.border_color_G_value.setValue)
        self.border_color_R_value.valueChanged['int'].connect(self.border_color_R_slider.setValue)
        self.border_color_B_value.valueChanged['int'].connect(self.border_color_B_slider.setValue)
        self.border_color_G_value.valueChanged['int'].connect(self.border_color_G_slider.setValue)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Material children editor"))
        self.save_material_button.setText(_translate("Dialog", "Save"))
        self.cancel_material_button.setText(_translate("Dialog", "Cancel"))
        self.brightness_glow_text.setText(_translate("Dialog", "Brightness glow"))
        self.brightness_base_text.setText(_translate("Dialog", "Brightness base"))
        self.shadow_orienation_text.setText(_translate("Dialog", "Shadow orientation"))
        self.saturation_base_text.setText(_translate("Dialog", "Saturation base"))
        self.saturation_glow_text.setText(_translate("Dialog", "Saturation glow"))
        self.border_color_G.setText(_translate("Dialog", "G"))
        self.border_color_B.setText(_translate("Dialog", "B"))
        self.border_color_A.setText(_translate("Dialog", "A"))
        self.border_color_text.setText(_translate("Dialog", "Border color"))
        self.border_color_R.setText(_translate("Dialog", "R"))
        self.light_orientation_glow_text.setText(_translate("Dialog", "Light orientation glow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Material_Child_Editor()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())