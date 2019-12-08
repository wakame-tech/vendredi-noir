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


# ★今までに作成したコードからGameクラスをコピー★
# コピーせずに上位ディレクトリから import する方が保守的に良いため、その方法をとった。
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


    def initUI(self):
        """ UIの初期化 """
        self.resize(500, 500)
        self.setWindowTitle('Tetris')

        self.statusBar().showMessage('h: 左、l: 右')  # ステータスバーに文言を表示
        self.__set_game_board()


    def __set_game_board(self):
        # ゲームボードを構築する.

        vbox = QVBoxLayout(spacing=0)
        self.button_dic = {}
        for i in self.size_li_rg[0]:
            hbox = QHBoxLayout()
            for j in self.size_li_rg[1]:
                button = MyLabel(self)
                button.set_bg_color()

                # button と関数をつなげる。
                self.button_dic[i, j] = button
                hbox.addWidget(button)
            vbox.addLayout(hbox)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)
        self.show()


    def show_cell_status(self):

        g = self.game
        for i in self.size_li_rg[0]:
            for j in self.size_li_rg[1]:
                part = g.board[i, j]
                # ここで button を書き換える操作を記述する。
                button = self.button_dic[i, j]
                button.set_bg_color('blue')



def main():
    app = QApplication(sys.argv)
    w = TetrisWindow()
    app.exec_()


if __name__ == '__main__':
    main()
