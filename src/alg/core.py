import numpy as np


class T(object):


    def __init__(self):

        self.board_size = [20, 10]
        self.init_t4mino()
        self.init_cur_li()
        self.init_board()
        self.gen_t4mino()


    def init_t4mino(self) -> None:
        
        self.t4mino_li = [
            # i
            [[[1, i] for i in range(4)],
             [[i, 1] for i in range(4)]] * 2,
            # o
            [[[0, 0], [0, 1], [1, 0], [1, 1]]] * 4,
            # t
            [[[0, 1]] + [[1, i] for i in range(3)],
             [[1, 2]] + [[i, 1] for i in range(3)],
             [[2, 1]] + [[1, i] for i in range(3)],
             [[1, 0]] + [[i, 1] for i in range(3)]],
            # j
            [[[0, 0]] + [[1, i] for i in range(3)],
             [[0, 2]] + [[i, 1] for i in range(3)],
             [[2, 2]] + [[1, i] for i in range(3)],
             [[2, 0]] + [[i, 1] for i in range(3)]],
            # l
            [[[0, 2]] + [[1, i] for i in range(3)],
             [[2, 2]] + [[i, 1] for i in range(3)],
             [[2, 0]] + [[1, i] for i in range(3)],
             [[0, 0]] + [[i, 1] for i in range(3)]],
            # s
            [[[0, 1], [0, 2], [1, 0], [1, 1]],
             [[0, 0], [1, 0], [1, 1], [2, 1]]] * 2,
            # t
            [[[0, 0], [0, 1], [1, 1], [1, 2]],
             [[0, 1], [1, 0], [1, 1], [2, 0]]] * 2
        ]

        return

    def init_cur_li(self) -> None:

        self.cur_li = [np.random.randint(7) for _ in range(4)]

        return


    def update_cur_li(self) -> None:

        self.cur_li.pop(0)

        return


    def init_board(self) -> None:

        self.board = np.zeros(self.board_size, dtype=np.int)

        return


    def game(self) -> None:

        while True:

            self.display()
            _pt = self.pt.copy()
            self.move(input())
            self.move('')
            if _pt == self.pt:
                self.save_board()
                self.update_cur_li()
                self.gen_t4mino()

        return


    def save_board(self) -> None:

        pt = self.pt
        for ix in self.t4mino_li[self.cur][self.rot]:
            self.board[ix[0]+pt[0], ix[1]+pt[1]] = self.cur + 1

        # flush
        for i in range(self.board_size[0]):
            if (self.board[i] != 0).all():
                for i_ in reversed(range(i)):
                    self.board[i_+1] = self.board[i_]

        return None


    def move(self, to: str) -> None:

        pt = self.pt
        # left
        if   to == 'h':
            q_li = [pt[0]  , pt[1]-1, self.rot]
        # right
        elif to == 'l':
            q_li = [pt[0]  , pt[1]+1, self.rot]
        # rotate
        elif to == ' ':
            q_li = [pt[0]  , pt[1]  ,(self.rot+1)%4]
        # down
        else:
            q_li = [pt[0]+1, pt[1]  , self.rot]

        for ix in self.t4mino_li[self.cur][q_li[-1]]:
            if ix[0]+q_li[0] >= self.board_size[0]          \
            or ix[1]+q_li[1] < 0                            \
            or ix[1]+q_li[1] >= self.board_size[1]          \
            or self.board[ix[0]+q_li[0], ix[1]+q_li[1]] != 0:
                return

        pt[0], pt[1], self.rot = q_li

        return


    def element(self, i: int, j: int) -> str:

        ix_li = self.t4mino_li[self.cur][self.rot]
        pt = self.pt

        for ix in ix_li:
            if ix[0]+pt[0] == i and ix[1]+pt[1] == j:
                return self.cur + 1

        tmp = self.board[i, j]
        return ' ' if tmp == 0 else tmp


    def display(self) -> None:

        ix_li = self.t4mino_li[self.cur][self.rot]
        pt = self.pt
        for i in range(self.board_size[0]):
            print('{:>2}|'.format(i), end='')
            for j in range(self.board_size[1]):
                print(self.element(i, j), end='')

            print()

        print('--+' + '-' * self.board_size[1])

        print(f'next: {self.cur_li}')

        return

    
    def gen_t4mino(self) -> None:

        self.cur_li.append(np.random.randint(7))    # current tetrimino index
        cur = self.cur_li[0]
        # i
        if   cur == 0:
            pt = [0, self.board_size[1] // 2 - 2]
        # otjlst
        else:
            pt = [0, self.board_size[1] // 2 - 1]

        self.cur = cur
        self.pt = pt
        self.rot = 0

        return



if __name__ == '__main__':

    t = T()
    t.game()
