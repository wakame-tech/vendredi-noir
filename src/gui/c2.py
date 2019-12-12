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
from api_wrapper import Api, event
sys.path.append('../alg')
from os.path import abspath
from Tetris import Game, Board, list2board
from PyQt5.QtWidgets import(
    QLabel, QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QMessageBox, QAction, QFrame
)
from PyQt5.QtGui import (
    QKeySequence, QPainter, QColor
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
        self.part_board = Board([20, 10])
        self.setGeometry(QRect(0, 0, 200, 400))


    def paintEvent(self, event):

        rect = self.contentsRect()

        for i in range(20):
            for j in range(10):
                self.draw_square(i, j)

        self.update()


    def draw_square(self, i: int, j: int):

        painter = QPainter(self)

        color = QColor(self.color_dic[self.part_board[i, j]])
        i *= 20
        j *= 20
        painter.fillRect(j+1, i+1, j+20-2, i+20-2, color)

        painter.setPen(color.lighter())
        painter.drawLine(j, i+20-1, j, i)
        painter.drawLine(j, i, j+20-2, i)

        painter.setPen(color.darker())
        painter.drawLine(j+1, i+20-1, j+20-1, i+20-1)
        painter.drawLine(j+20-1, i+20-1, j+20-1, i+1)


    def update_board(self, fn):

        for i in range(20):
            for j in range(10):
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

        box1 = QHBoxLayout()
        sidebox = QVBoxLayout(spacing=50)
        box2 = QHBoxLayout()

        # Playerのゲームボード
        v1box = QVBoxLayout(spacing=1)
        player1_label = QLabel('You')
        player1_label.setGeometry(QRect(0, 0, 250, 12))
        v1box.addWidget(player1_label)
        self.your_fr = MyFrame()
        v1box.addWidget(self.your_fr)

        # 対戦相手のゲームボード
        v2box = QVBoxLayout(spacing=1)
        player2_label = QLabel('Opponent')
        player2_label.setGeometry(QRect(0, 0, 250, 12))
        v2box.addWidget(player2_label)
        self.oppo_fr = MyFrame()
        v2box.addWidget(self.oppo_fr)

        box1.addLayout(v1box)
        box1.addLayout(sidebox)
        box2.addLayout(box1)
        box2.addLayout(v2box)
        container = QWidget()
        container.setLayout(box2)
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
            'board'     : g.board.tolist(),
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
        ret, cv_img = self.capture.read()
        if ret is False:
            return
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        proc = self.game.board / 7
        cv_img = cv_img * proc
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
