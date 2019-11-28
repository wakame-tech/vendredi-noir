import numpy as np


class TetrisAlg(object):

    def __init__(self, ):

        self.width = 10
        self.height = 20

        self.board_init()
        self.generate_block()


    def board_init(self):

        self.board = np.zeros([self.height, self.width], dtype=np.int)


    def update(self):

        self.point_y += 1

        return


    def game(self, display_mode=False):

        from time import sleep

        self.generate_block()
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

        if   to == 'r':     # rigth
            self.point_x += 1
        elif to == 'l':     # left
            self.point_x -= 1
        elif to == ' ':
            self.move()

        return


    def is_cont(self) -> bool:

        return True


    def display(self) -> None:

        for h in range(self.height):
            print('{:>2}|'.format(h), end='')
            for w in range(self.width):
                part = self.board[h, w]
                print(f'{part}' if part != 0 else ' ', end='')

            print()

        print('--+' + '-' * self.width)


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

