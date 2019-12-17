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
from time import sleep
import json
import cv2
import numpy as np
from socketio.exceptions import ConnectionError
from api_wrapper import Api, event
sys.path.append('../alg')
from os.path import abspath
from Tetris import Game, Board, Tetrimino, list2board
from PyQt5.QtWidgets import(
    QLabel, QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QAction, QFrame
)
from PyQt5.QtGui import (
    QIcon, QKeySequence, QPainter, QColor, QPixmap, QImage
)

from PyQt5.QtCore import(
    QTimer
)

ENDPOINT = 'https://vendredi-noir.herokuapp.com'
# ENDPOINT = 'http://localhost:5000'


class MyFrame(QFrame):

    def __init__(self, board_size: [int]):

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
        self.board_size = board_size
        self.part_board = Board(self.board_size)
        self.to = Tetrimino()


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


    def update_next(self, next_cur: int):

        t4mino = self.to.t4mino_li[next_cur][0]
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                self.part_board[i, j] = next_cur + 1 if [i, j] in t4mino else 0


        self.update()



class TetrisWindow(QMainWindow, Api):

    def __init__(self):
        app = QApplication(sys.argv)
        self.debugging = False
        print('RUNNING PROGRAMME')
        super(TetrisWindow, self).__init__()
        super(Api, self).__init__()
        g = self.game = Game()
        self.size_li_rg = [range(size) for size in g.board_size]
        self.initUI()
        # 顔画像を人質に取る
        self.set_loser_image()

        # python main.py --join で 部屋に参加する
        self.is_host = not (len(sys.argv) >= 2 and sys.argv[1] == '--join')
        # 待ち時間[s]
        self.matching_seconds = 10
        # 部屋名(固定)
        self.room_name = 'AAA'

        self.show()
        g._pt, g._rot = [-1, -1], -1

        while True:
            try:
                self.connect_server()
            except ConnectionError:
                from traceback import print_exc; print_exc()
                sleep(1)
            else:
                break

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        interval = 300 # ms
        self.timer.start(interval)

        app.exec_()


    def initUI(self):
        """ UIの初期化 """
        self.resize(750, 750)
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
        nextVbox = QVBoxLayout(spacing=50)
        oppoVbox = QVBoxLayout()

        # Playerのゲームボード
        yourHbox1 = QHBoxLayout(spacing=1)  # Labelが追加されるbox
        yourHbox2 = QHBoxLayout(spacing=1)  # boardが描画されるbox
        yourLabel = QLabel('You')
        yourHbox1.addWidget(yourLabel)
        self.your_fr = MyFrame([20, 10])
        yourHbox2.addWidget(self.your_fr)
        yourVbox.addLayout(yourHbox1, 1)
        yourVbox.addLayout(yourHbox2, 5)

        # 次のテトリミノ
        nextHbox1 = QHBoxLayout(spacing=1)  # Labelが追加されるbox
        nextHbox2 = QHBoxLayout(spacing=1)  # next tetrimino が描画される
        nextHbox3 = QHBoxLayout(spacing=1)
        nextLabel = QLabel('next 1')
        nextHbox1.addWidget(nextLabel)
        self.next_fr = MyFrame([4, 4])
        self.next_fr.update_next(self.game.cur_li[1])
        spaceLabel = QLabel('copyright')
        nextHbox3.addWidget(spaceLabel)
        nextHbox2.addWidget(self.next_fr)
        nextVbox.addLayout(nextHbox1, 1)
        nextVbox.addLayout(nextHbox2, 2)
        nextVbox.addLayout(nextHbox3, 5)

        # 対戦相手のゲームボード
        oppoHbox1 = QHBoxLayout(spacing=1)  # Labelが追加されるbox
        oppoHbox2 = QHBoxLayout(spacing=1)  # boardが描画されるbox
        oppoLabel = QLabel('Opponent')
        oppoHbox1.addWidget(oppoLabel)
        self.oppo_fr = MyFrame([20, 10])
        oppoHbox2.addWidget(self.oppo_fr)
        oppoVbox.addLayout(oppoHbox1, 1)
        oppoVbox.addLayout(oppoHbox2, 5)


        mainLayout.addLayout(yourVbox, 2)
        mainLayout.addLayout(nextVbox, 1)
        mainLayout.addLayout(oppoVbox, 2)
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
                self.close()

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
            self.next_fr.update_next(g.cur_li[1])

        g._pt, g._rot = g.pt.copy(), g.rot
        if not g.yet():
            loser_img = self.get_loser_image()
            cv2.imwrite('LOSER.PNG', loser_img)
            vd = QMessageBox()
            # TODO: この部分でnumpyのエラーが起きているので、多分QPixmapはnumpyを引き受けないんだと思う、知らんけど
            # vd.information(self, "勝敗", "You Lose...")
            vd.information(self, "勝敗", "You Lose...")
            self.closer()


    def get_state(self) -> {str: object}:
        
        g = self.game
        state = {
            'id'        : self.socketid,
            'board'     : g.board.board,
            'cur'       : g.cur,
            'cur_li'    : g.cur_li,
            'board_size': g.board_size
        }
        return state


    def connect_server(self):
        # TODO: refactoring
        self.started = False
        self.connect(ENDPOINT)

        print(f'id: {self.socketid}')

        if self.is_host:
            self.create_room(self.room_name)
            print(f'matching {self.matching_seconds}s ...')
            sleep(self.matching_seconds)
            self.game_start(self.room_name)
        else:
            self.join_room(self.room_name)
            print('start waiting ...')
            while not self.started:
                sleep(1)


    def send_board(self):

        state = self.get_state()
        self.send_state(state)


    def get_loser_image(self) -> np.ndarray:

        g = self.game
        frame = self.loser_img
        loser_size_tup = (320, 640)

        board_np = np.array(g.board.board)
        repeater = loser_size_tup[1] // board_np.shape[0]
        filt = board_np.repeat(repeater, axis=0).repeat(repeater, axis=1)
        filt[filt >= 1] = 1
        loser_img = np.zeros_like(frame)
        for ix in range(3):
            loser_img[..., ix] = frame[..., ix] * filt

        return loser_img


    def set_loser_image(self):

        loser_size_tup = (320, 640)

        cap = cv2.VideoCapture(0)
        sleep(2)    # 2 秒待ってからインカメ、本当は顔認証とか使えばもっと楽しくなる
        frame = cap.read()[1]
        height = frame.shape[0]
        width = height // 2
        frame = frame[:, frame.shape[1]//2-width//2:frame.shape[1]//2+width//2]
        self.loser_img = cv2.resize(frame, loser_size_tup)

        cap.release()
        del cap


    @event('connected')
    def connected(self):
        print('[Connected from Class]')


    @event('updated')
    def sync_status(self, state) -> None:
        if self.socketid == state['id']:
            return
        if self.debugging:
            # mirroring
            state = json.loads(json.dumps(self.get_state()))

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
        print(f'[info] created {res["room_name"]} by {res["id"]}')


    @event('room_joined')
    def room_joined(self, res):
        print(f'[info] joined {res["room_name"]} by {res["id"]}')


    @event('game_started')
    def game_started(self, res):
        print('[info] game started')
        self.started = True


    @event('game_ended')
    def game_ended(self, res):
        print('[info] game ended')
        QMessageBox.information(self, "勝敗", "You Win!")
        sys.exit()



if __name__ == '__main__':

    TetrisWindow()
