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
import time
import json
import cv2
import numpy as np
from api_wrapper import Api, event
sys.path.append('../alg')
from os.path import abspath
from Tetris import Game, Board, list2board
from PyQt5.QtWidgets import(
    QLabel, QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QMessageBox, QAction, QFrame
)
from PyQt5.QtGui import (
    QKeySequence, QPainter, QColor, QPixmap, QImage
)

from PyQt5.QtCore import(
    QTimer, Qt, QRect
)

ENDPOINT = 'https://vendredi-noir.herokuapp.com'
# ENDPOINT = 'http://localhost:5000'


class MyFrame(QFrame):

    def __init__(self):

        super().__init__()

        self.color_dic = [
            0x808080,   # nothing, space
            0x00ffff,   # i, cyan
            0xffff00,   # o, yellow
            0xff00ff,   # t, purple
            0x0000ff,   # j, blue
            0xff8000,   # l, orange
            0x00ff00,   # s, green
            0xff0000    # t, red
        ]
        self.board_size = [20, 10]
        self.part_board = Board(self.board_size)


    def paintEvent(self, event):

        rect = self.contentsRect()

        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                self.draw_square(i, j)

        self.update()



    def draw_square(self, i: int, j: int):

        rect_h = self.contentsRect().height() / self.board_size[0]
        rect_w = self.contentsRect().width() / self.board_size[1]

        painter = QPainter(self)

        color = QColor(self.color_dic[self.part_board[i, j]])
        i *= rect_h
        j *= rect_w
        painter.fillRect(j+1, i+1, j+rect_w-2, i+rect_h-2, color)

        painter.setPen(color.lighter())
        painter.drawLine(j, i+rect_h-1, j, i)
        painter.drawLine(j, i, j+rect_w-2, i)

        painter.setPen(color.darker())
        painter.drawLine(j+1, i+rect_h-1, j+rect_w-1, i+rect_h-1)
        painter.drawLine(j+rect_w-1, i+rect_h-1, j+rect_w-1, i+1)


    def update_board(self, fn):

        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                self.part_board[i, j] = fn(i, j)

        self.update()



class TetrisWindow(QMainWindow, Api):

    def __init__(self):
        app = QApplication(sys.argv)
        print('RUNNING PROGRAMME')
        super(TetrisWindow, self).__init__()
        super(Api, self).__init__()
        g = self.game = Game()
        self.color_dic = [
            '#aaa',       # nothing, space
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
        img = self.make_loser_image()
        h, w, c = img.shape
        bytesPerLine = 3 * w
        qimg = QImage(img.data, w, h, bytesPerLine, QImage.Format_RGB888)
        vd = QMessageBox()
        vd.setIconPixmap(QPixmap(qimg))
        vd.information(self, "勝敗", "You Lose...")

        self.show()
        g._pt, g._rot = [-1, -1], -1

        self.connect_server()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        interval = 300 # ms
        self.timer.start(interval)

        app.exec_()


    def initUI(self):
        """ UIの初期化 """
        self.resize(750, 1000)
        self.setWindowTitle('Tetris')

        # 終了ボタン
        exitAction = QAction('&Exit Game', self)
        exitAction.triggered.connect(self.close)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Menu')
        fileMenu.addAction(exitAction)

        self.statusBar().showMessage('h: 左, l: 右, f: 右回転, a: 左回転')  # ステータスバーに文言を表示
        self.init_game_board()


    def init_game_board(self):
        # ゲームボードを構築する。

        mainLayout = QHBoxLayout()
        yourVbox = QVBoxLayout()            # youが追加されるLayout
        sidebox = QVBoxLayout(spacing=50)
        oppoVbox = QVBoxLayout()

        # Playerのゲームボード
        yourHbox1 = QHBoxLayout(spacing=1)  # Labelが追加されるbox
        yourHbox2 = QHBoxLayout(spacing=1)  # boardが描画されるbox
        yourLabel = QLabel('You')
        yourHbox1.addWidget(yourLabel)
        self.your_fr = MyFrame()
        yourHbox2.addWidget(self.your_fr)
        yourVbox.addLayout(yourHbox1, 1)
        yourVbox.addLayout(yourHbox2, 5)

        # 対戦相手のゲームボード
        oppoHbox1 = QHBoxLayout(spacing=1)  # Labelが追加されるbox
        oppoHbox2 = QHBoxLayout(spacing=1)  # boardが描画されるbox
        oppoLabel = QLabel('Opponent')
        oppoHbox1.addWidget(oppoLabel)
        self.oppo_fr = MyFrame()
        oppoHbox2.addWidget(self.oppo_fr)
        oppoVbox.addLayout(oppoHbox1, 1)
        oppoVbox.addLayout(oppoHbox2, 5)


        mainLayout.addLayout(yourVbox)
        mainLayout.addLayout(sidebox)
        mainLayout.addLayout(oppoVbox)
        container = QWidget()
        container.setLayout(mainLayout)
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
            self.your_fr.update_board(lambda i, j: g.element(i, j))

            super(TetrisWindow, self).keyPressEvent(event)


    def update_status(self):

        g = self.game
        g.move()
        self.your_fr.update_board(lambda i, j: g.element(i, j))
        self.send_board()
        if g._pt == g.pt and g._rot == g.rot:
            g.save_board()
            g.update_cur_li()
            g.gen_t4mino()

        g._pt, g._rot = g.pt.copy(), g.rot
        if not g.yet():
            img = self.make_loser_image()
            vd = QMessageBox
            vd.setIconPixmap(Qpixmap(img))
            vd.information(self, "勝敗", "You Lose...")
            exit() 


    def get_state(self) -> {str: object}:
        
        g = self.game
        state = {
            'board'     : g.board.board,
            'cur'       : g.cur,
            'cur_li'    : g.cur_li,
            'board_size': g.board_size
        }
        return state


    def connect_server(self):
        # TODO: refactoring
        self.connect(ENDPOINT)
        is_host = not (len(sys.argv) >= 2 and sys.argv[1] == '--join')
        room_name = 'AAA'
        self.started = False
        if is_host:
            self.create_room(room_name)
        else:
            self.join_room(room_name)

        if is_host:
            limit = 5
            print(f'matching {limit}s ...')
            time.sleep(limit)
            self.game_start(room_name)
        else:
            while not self.started:
                print(f'waiting start ... {self.started}')
                time.sleep(1)


    def send_board(self):

        state = self.get_state()

        print('[Send]')
        self.send_state(state)

    def make_loser_image(self):
        g = self.game
        capture = cv2.VideoCapture(0)
        ret, cv_img = capture.read()
        if ret is False:
            return
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        a = np.array(g.board.board)
        proc = a / 7
        # cv_img[:,:,0] = cv_img[:,:,0] * proc
        # cv_img[:,:,1] = cv_img[:,:,1] * proc
        # cv_img[:,:,2] = cv_img[:,:,2] * proc
        return cv_img

    @event('connected')
    def connected(self):
        print('[Connected from Class]')


    @event('updated')
    def sync_status(self, state):
        # mirroring for debug ---------
        g = self.game
        state = json.loads(json.dumps(self.get_state()))
        # -----------------------------

        print('[Recv]')
        [height, width] = state['board_size']
        board = list2board(state['board'])

        # reflect to board
        self.oppo_fr.update_board(lambda i, j: board[i, j])


    @event('disconnected')
    def disconnected(self):
        print('[Disconnected]')
        sys.exit()


    @event('room_created')
    def room_created(self, res):
        print('created')


    @event('room_joined')
    def room_joined(self, res):
        print('joined')


    @event('game_started')
    def game_started(self, res):
        print('game started')
        self.started = True


    @event('game_ended')
    def game_ended(self, res):
        QMessageBox.information(self, "勝敗", "You Win!")
        sys.exit()



if __name__ == '__main__':

    TetrisWindow()
