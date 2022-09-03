import os, re, stat, shutil, struct, functools, stat, numpy as np
from shutil import rmtree, copyfile, move, copytree
from pyglet import image
from datetime import datetime
from natsort import natsorted
from PyQt5.QtGui import QImage, QPixmap, QStandardItem, QColor, QStandardItemModel
from PyQt5.QtWidgets import QLabel, QFileDialog, QMessageBox, QInputDialog, QLineEdit