# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'folderTreeView.ui'
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

class Ui_folderTreeViewWidget(object):
    def setupUi(self, folderTreeViewWidget):
        if not folderTreeViewWidget.objectName():
            folderTreeViewWidget.setObjectName(u"folderTreeViewWidget")
        folderTreeViewWidget.resize(598, 423)
        self.verticalLayout = QVBoxLayout(folderTreeViewWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.folderTreeView = QTreeView(folderTreeViewWidget)
        self.folderTreeView.setObjectName(u"folderTreeView")

        self.verticalLayout.addWidget(self.folderTreeView)


        self.retranslateUi(folderTreeViewWidget)

        QMetaObject.connectSlotsByName(folderTreeViewWidget)
    # setupUi

    def retranslateUi(self, folderTreeViewWidget):
        folderTreeViewWidget.setWindowTitle(QCoreApplication.translate("folderTreeViewWidget", u"Form", None))
    # retranslateUi

