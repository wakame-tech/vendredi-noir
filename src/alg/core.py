import numpy as np


class TetrisAlg(object):

    def __init__(self, ):

        self.width = 10
        self.height = 20

        self.board_init()
        self.generate_block()


    def board_init(self):

        self.board = np.zeros([self.height, self.width], dtype=np.int)
        self.generate_block()


    def update(self):

        is_generatable = False
        point = self.point
        point[0] += 1
        # 左右めり込み評価
        ix_li = self.ix_li + point
        min_ix1 = np.min(ix_li[:, 1])
        max_ix1 = np.max(ix_li[:, 1])
        if min_ix1 < 0:
            point[1] += 1
        elif max_ix1 >= self.width:
            point[1] -= 1

        # 下めり込み評価
        max_ix0 = np.max(ix_li[:, 0])
        if max_ix0 >= self.height:
            point[0] -= 1
            is_generatable = True

        # 他ブロックめり込み評価

        # 消す評価
        for h in range(self.height):
            if np.all(self.board[h] != 0):
                self.board[h] = 0
                for _h in reversed(range(h)):
                    self.board[_h+1] = self.board[_h]

        # ブロック生成
        if is_generatable:
            self.store_board()
            self.generate_block()

        return


    def store_board(self):

        for ix in self.ix_li + self.point:
            self.board.__setitem__(tuple(ix), self.block_type)


    def game(self, display_mode=False):

        from time import sleep

        while self.is_cont():
            if display_mode:
                self.display()

            self.move(input())
            self.update()


    def rotate(self) -> None:

        rot = self.rotation
        # =========================
        #  x  |      |  x   |
        #  x  |      |  x   | xxxx
        #  x  | xxxx |  x   |
        #  x  |      |  x   |
        # =========================
        if self.block_type == 1:
            if   rot == 0:
                ix_li = [[0, 2], [1, 2], [2, 2], [3, 2]]
            elif rot == 1:
                ix_li = [[2, 0], [2, 1], [2, 2], [2, 3]]
            elif rot == 2:
                ix_li = [[0, 1], [1, 1], [2, 1], [3, 1]]
            elif rot == 3:
                ix_li = [[1, 0], [1, 1], [1, 2], [1, 3]]
        # =========================
        # xx
        # xx
        #
        #
        # =========================
        elif self.block_type == 2:
            ix_li = [[0, 0], [0, 1], [1, 0], [1, 1]]
        # =========================
        #  x   |  x   |      |  x
        # xxx  |  xx  | xxx  | xx
        #      |  x   |  x   |  x
        #      |      |      |
        # =========================
        elif self.block_type == 3:
            if   rot == 0:
                ix_li = [[0, 1], [2, 1], [1, 1], [1, 2]]
            elif rot == 1:
                ix_li = [[1, 0], [2, 1], [1, 1], [1, 2]]
            elif rot == 2:
                ix_li = [[1, 0], [2, 1], [1, 1], [0, 1]]
            elif rot == 3:
                ix_li = [[0, 1], [1, 0], [1, 1], [1, 2]]
        # =========================
        # xx   | xxx  |  x   | x
        # x    |   x  |  x   | xxx
        # x    |      | xx   |
        #      |      |      |
        # =========================
        elif self.block_type == 4:
            if   rot == 0:
                ix_li = [[0, 0], [0, 1], [1, 0], [2, 0]]
            elif rot == 1:
                ix_li = [[0, 0], [0, 1], [0, 2], [1, 2]]
            elif rot == 2:
                ix_li = [[0, 1], [1, 1], [2, 0], [2, 1]]
            elif rot == 3:
                ix_li = [[0, 0], [1, 0], [1, 1], [1, 2]]
        # =========================
        # x    | xxx  | xx   |   x
        # x    | x    |  x   | xxx
        # xx   |      |  x   |
        #      |      |      |
        # =========================
        elif self.block_type == 5:
            if   rot == 0:
                ix_li = [[0, 0], [1, 0], [2, 0], [2, 1]]
            elif rot == 1:
                ix_li = [[0, 0], [0, 1], [0, 2], [1, 0]]
            elif rot == 2:
                ix_li = [[0, 0], [0, 1], [1, 1], [2, 1]]
            elif rot == 3:
                ix_li = [[0, 2], [1, 0], [1, 1], [1, 2]]
        # =========================
        # x    |  xx
        # xx   | xx
        #  x   |
        #      |
        # =========================
        elif self.block_type == 6:
            if   rot % 2== 0:
                ix_li = [[0, 0], [1, 0], [1, 1], [2, 1]]
            elif rot % 2== 1:
                ix_li = [[0, 1], [0, 2], [1, 0], [1, 1]]
        # =========================
        #  x   | xx
        # xx   |  xx
        # x    |
        #      |
        # =========================
        elif self.block_type == 7:
            if   rot % 2 == 0:
                ix_li = [[0, 1], [1, 0], [1, 1], [2, 0]]
            elif rot % 2== 1:
                ix_li = [[0, 0], [0, 1], [1, 1], [1, 2]]

        self.ix_li = np.array(ix_li)
        self.rotation = (self.rotation + 1) % 4

        return


    def move(self, to: str='r') -> None:

        if   to == 'l':     # right
            self.point[1] += 1
        elif to == 'h':     # left
            self.point[1] -= 1
        elif to == ' ':
            self.rotate()

        return


    def is_cont(self) -> bool:

        return True


    def display(self) -> None:

        ix_li = self.ix_li + self.point
        for h in range(self.height):
            print('{:>2}|'.format(h), end='')
            for w in range(self.width):

                for ix in ix_li:
                    if h == ix[0] and w == ix[1]:
                        print(f'{self.block_type}', end='')
                        break
                else:
                    part = self.board[h, w]
                    print(f'{part}' if part != 0 else ' ', end='')

            print()

        print('--+' + '-' * self.width)

        return


    def generate_block(self) -> None:

        board = self.board

        block_type = np.random.randint(1, 7+1, 1)[0]

        # =========================
        #      | xx   |  x   | x    |   x |  xx  | xx
        # xxxx | xx   | xxx  | xxx  | xxx | xx   |  xx
        #      |      |      |      |     |      |
        #      |      |      |      |     |      |
        # =========================
        # case i
        if   block_type == 1:
            ix_li = [[1, 0], [1, 1], [1, 2], [1, 3]]
        # case o
        elif block_type == 2:
            ix_li = [[0, 0], [0, 1], [1, 0], [1, 1]]
        # case t
        elif block_type == 3:
            ix_li = [[0, 1], [1, 0], [1, 1], [1, 2]]
        # case j
        elif block_type == 4:
            ix_li = [[0, 0], [1, 0], [1, 1], [1, 2]]
        # case l
        elif block_type == 5:
            ix_li = [[0, 2], [1, 0], [1, 1], [1, 2]]
        # case s
        elif block_type == 6:
            ix_li = [[0, 1], [0, 2], [1, 0], [1, 1]]
        # case z
        elif block_type == 7:
            ix_li = [[0, 0], [0, 1], [1, 1], [1, 2]]

        self.ix_li      = np.array(ix_li)
        self.block_type = block_type
        self.point      = np.array([0, self.width // 2])
        self.rotation   = 0



if __name__ == '__main__':

    ta = TetrisAlg()

    ta.game(True)
