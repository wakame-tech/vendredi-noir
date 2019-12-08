# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Wed Oct  9 10:45:35 2019

マインスイーパー
URL: https://github.com/278Mt/taniguchi/blob/master/04_1010_qt/Tetris_gui.py
@author: n_toba
@id: 4617054
"""

from platform import python_version
if python_version() != '3.8.0':
    raise Exception('your python is not 3.8.0')
import sys
from os.path import abspath
from Tetris import Game
from PyQt5.QtWidgets import(
    QLabel, QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QKeySequence
)


class MyLabel(QLabel):

    def __init__(self, parent):

        super(MyLabel, self).__init__(parent)
        self.parent = parent
        self.setMinimumSize(7, 7)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)


    def set_bg_color(self, colorname: str='#444'):

        self.setStyleSheet(f'MyLabel{{background-color: {colorname}}}')



class TetrisWindow(QMainWindow):

    def __init__(self):

        print('RUNNING PROGRAMME')
        super(TetrisWindow, self).__init__()
        g = self.game = Game()
        self.size_li_rg = [range(size) for size in g.board_size]
        self.initUI()

        self.show()


    def initUI(self):
        """ UIの初期化 """
        self.resize(500, 500)
        self.setWindowTitle('Tetris')

        self.statusBar().showMessage('h: 左、l: 右')  # ステータスバーに文言を表示
        self.init_game_board()


    def init_game_board(self):
        # ゲームボードを構築する。

        vbox = QVBoxLayout(spacing=0)
        self.label_dic = {}
        for i in self.size_li_rg[0]:
            hbox = QHBoxLayout()
            for j in self.size_li_rg[1]:
                label = MyLabel(self)
                label.set_bg_color()

                # label と関数をつなげる。
                self.label_dic[i, j] = label
                hbox.addWidget(label)
            vbox.addLayout(hbox)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)


    # keyPressEvent 関数のオーバーライド
    def keyPressEvent(self, event):

        g = self.game
        key = QKeySequence(event.key()).toString()
        if key == 'Q':
            exit()

        print(key)
        g.move(key.lower())
        print(g.display())
        self.update_cell_status()

        super(TetrisWindow, self).keyPressEvent(event)


    def update_cell_status(self):

        g = self.game
        for i in self.size_li_rg[0]:
            for j in self.size_li_rg[1]:
                part = g.board[i, j]
                # ここで label を書き換える操作を記述する。
                label = self.label_dic[i, j]
                label.set_bg_color('blue')



def main():

    app = QApplication(sys.argv)
    w = TetrisWindow()
    app.exec_()


if __name__ == '__main__':

    main()
