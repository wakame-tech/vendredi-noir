# -*- coding: utf-8 -*-
#!/usr/bin/env python3.8
"""
Created on Sun Dic  8 16:30:35 2019

テトリスGUI部分
URL: https://github.com/wakame-tech/vendredi-noir/blob/master/src/gui/main.py
@author: n_toba
@id: 4617054
"""

import sys
sys.path.append('../alg')
from os.path import abspath
from Tetris import Game
from PyQt5.QtWidgets import(
    QLabel, QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QMessageBox
)
from PyQt5.QtGui import (
    QKeySequence
)

from PyQt5.QtCore import QTimer



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

        app = QApplication(sys.argv)
        print('RUNNING PROGRAMME')
        super(TetrisWindow, self).__init__()
        g = self.game = Game()
        self.color_dic = [
            '#444',     # nothing, space
            'cyan',     # i
            'yellow',   # o
            'purple',   # t
            'blue',     # j
            'orange',   # l
            'green',    # s
            'red'       # t
        ]
        self.size_li_rg = [range(size) for size in g.board_size]
        self.initUI()

        self.show()
        g._pt, g._rot = [-1, -1], -1

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(300)  # updating per 1000 ms

        app.exec_()


    def initUI(self):
        """ UIの初期化 """
        self.resize(250, 500)
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
        _key = event.key()
        if ord('A') <= _key <= ord('Z'):
            key = QKeySequence(_key).toString()
            if key == 'Q':
                exit()

            g.move(key.lower())
            self.update_board()

            super(TetrisWindow, self).keyPressEvent(event)


    def update_status(self):

        g = self.game
        g.move()
        self.update_board()
        if g._pt == g.pt and g._rot == g.rot:
            g.save_board()
            g.update_cur_li()
            g.gen_t4mino()

        g._pt, g._rot = g.pt.copy(), g.rot
        if not g.yet():
            exit() 


    def update_board(self):

        g = self.game
        for i in self.size_li_rg[0]:
            for j in self.size_li_rg[1]:
                label = self.label_dic[i, j]
                label.set_bg_color(self.color_dic[g.element(i, j)])



if __name__ == '__main__':

    TetrisWindow()
