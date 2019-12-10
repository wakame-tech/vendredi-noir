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
from api_wrapper import Api, NdArrayJsonEncoder, event
sys.path.append('../alg')
from os.path import abspath
from Tetris import Game
from PyQt5.QtWidgets import(
    QLabel, QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QMessageBox, QAction
)
from PyQt5.QtGui import (
    QKeySequence
)

from PyQt5.QtCore import QTimer

ENDPOINT = 'https://vendredi-noir.herokuapp.com'
# ENDPOINT = 'http://localhost:5000'

# TODO
global started

class MyLabel(QLabel):

    def __init__(self, parent):

        super(MyLabel, self).__init__(parent)
        self.parent = parent
        self.setMinimumSize(7, 7)
        self.setMaximumSize(25, 25)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)


    def set_bg_color(self, colorname: str=None):
        
        self.setStyleSheet(f'MyLabel{{background-color: {colorname if colorname is not None else "#aaa"}}}')



class TetrisWindow(QMainWindow, Api):

    def __init__(self):
        app = QApplication(sys.argv)
        print('RUNNING PROGRAMME')
        super(TetrisWindow, self).__init__()
        super(Api, self).__init__()
        g = self.game = Game()
        self.color_dic = [
            None,       # nothing, space
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
        self.resize(750, 500)
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
        v1box.addWidget(player1_label)
        self.label_dic = {}
        for i in self.size_li_rg[0]:
            h1box = QHBoxLayout()
            for j in self.size_li_rg[1]:
                label = MyLabel(self)
                label.set_bg_color()

                # label と関数をつなげる。
                self.label_dic[i, j] = label
                h1box.addWidget(label)
            v1box.addLayout(h1box)

        # 次のミノを表示するスペース
        nextbox = QVBoxLayout(spacing=1)
        next_label = QLabel('Next mino')
        nextbox.addWidget(next_label)
        for i in range(4):
            nexthbox = QHBoxLayout()
            for j in range(4):
                label = MyLabel(self)
                label.set_bg_color()
                nexthbox.addWidget(label)
            nextbox.addLayout(nexthbox)

        # Hold中のミノを表示するスペース
        holdbox = QVBoxLayout(spacing=1)
        hold_label = QLabel('Holding mino')
        holdbox.addWidget(hold_label)
        for i in range(4):
            holdhbox = QHBoxLayout()
            for j in range(4):
                label = MyLabel(self)
                label.set_bg_color()
                holdhbox.addWidget(label)
            holdbox.addLayout(holdhbox)

        # 対戦相手のゲームボード
        v2box = QVBoxLayout(spacing=1)
        player2_label = QLabel('Opponent')
        v2box.addWidget(player2_label)
        self.opponent_label_dic = {}
        for i in self.size_li_rg[0]:
            h2box = QHBoxLayout()
            for j in self.size_li_rg[1]:
                label = MyLabel(self)
                label.set_bg_color()
                # label と関数をつなげる。
                self.opponent_label_dic[i, j] = label
                h2box.addWidget(label)
            v2box.addLayout(h2box)

        sidebox.addLayout(nextbox)
        sidebox.addLayout(holdbox)
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
            self.update_board()

            super(TetrisWindow, self).keyPressEvent(event)


    def update_status(self):

        g = self.game
        g.move()
        self.update_board()
        self.send_board()
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


    def get_state(self) -> {str: object}:
        
        g = self.game
        state = {
            'board'     : g.board,
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
        global started
        started = False
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
            while not started:
                print(f'waiting start ... {started}')
                time.sleep(1)


    def send_board(self):

        state = self.get_state()

        print('[Send]')
        self.send_state(state)


    @event('connected')
    def connected(self):
        print('[Connected from Class]')


    @event('updated')
    def sync_status(self, state):
        # mirroring for debug ---------
        g = self.game
        state = json.loads(json.dumps(self.get_state(), cls=NdArrayJsonEncoder))
        # -----------------------------

        print('[Recv]')
        [height, width] = state['board_size']
        board = state['board']

        # reflect to board
        for i in range(height):
            for j in range(width):
                label = self.opponent_label_dic[i, j]
                label.set_bg_color(self.color_dic[board[i][j]])


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
        global started
        started = True


    @event('game_ended')
    def game_ended(self, res):
        print('game ended')
        sys.exit()



if __name__ == '__main__':

    TetrisWindow()
