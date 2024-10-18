# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fileTreeView.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTreeView,
    QVBoxLayout, QWidget)

class Ui_fileTreeViewWidget(object):
    def setupUi(self, fileTreeViewWidget):
        if not fileTreeViewWidget.objectName():
            fileTreeViewWidget.setObjectName(u"fileTreeViewWidget")
        fileTreeViewWidget.resize(598, 423)
        self.verticalLayout = QVBoxLayout(fileTreeViewWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.fileTreeView = QTreeView(fileTreeViewWidget)
        self.fileTreeView.setObjectName(u"fileTreeView")

        self.verticalLayout.addWidget(self.fileTreeView)


        self.retranslateUi(fileTreeViewWidget)

        QMetaObject.connectSlotsByName(fileTreeViewWidget)
    # setupUi

    def retranslateUi(self, fileTreeViewWidget):
        fileTreeViewWidget.setWindowTitle(QCoreApplication.translate("fileTreeViewWidget", u"Form", None))
    # retranslateUi

