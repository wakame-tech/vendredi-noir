# coding: UTF-8

import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QLabel, QWidget
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtCore import Qt, QTimer


class Test(QWidget):

    def __init__(self):
        app = QApplication(sys.argv)

        super().__init__()
        self.init_ui()
        self.show()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)#一秒間隔で更新

        app.exec_()


    def init_ui(self):
        self.setWindowTitle("PyQt5")
        self.resize(640, 400)
        self.frameGeometry()\
            .moveCenter(
                        QDesktopWidget()
                        .availableGeometry()
                        .center()
                        )
        self.x = 0
        self.y =200


    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(Qt.red)

        self.x += 1
        if self.x > 640:
            self.x = 0

        painter.drawRect(self.x, self.y, 10, 10)


if __name__ == '__main__':
    Test()
