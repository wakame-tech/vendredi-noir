import pygame
from pygame.locals import *
import sys
import random
from falls_position import FallsPosition


def minochoice(r):

    mino_choice = r
    if r == 0:
        mino_choice = random.randint(1, 7)
    return mino_choice


def main():
    c_0 = (200, 200, 200)
    c_1 = (242, 242, 242)

    x = 80
    y = 0
    r = 0
    a = 0
    gameover = 0
    touch = 0
    mino = 0
    fall_speed = 10

    pygame.init()
    screen = pygame.display.set_mode((200, 400))
    pygame.display.set_caption("Tetris")
    
    clock = pygame.time.Clock()

    num = 20
    data_position_p = []
    data_position = []
    data_color = []
    while num > 0:
        num_x = 10
        array_y = []
        while num_x > 0:
            array_y.append(c_1)
            num_x -= 1
        array = [0] * 10
        array_x = [0] * 10
        data_position.append(array)
        data_position_p.append(array_x)
        data_color.append(array_y)
        num -= 1

    while True:
        clock.tick(30)
        screen.fill(c_1)
        mino = minochoice(mino)
    
        for i, data in enumerate(data_color):
            for e, d in enumerate(data):
                h = i * 20
                w = e * 20
                pygame.draw.rect(screen, data_color[i][e], Rect(w, h, 20, 20), 0)

        if gameover == 0:

            for i, data in enumerate(data_position_p):
                for e, d in enumerate(data):
                    if data_position_p[i][e] == 1:
                        data_position_p[i][e] = 0

            w = round(x / 20)
            h = round(y / 20)

            fp = FallsPosition()
            if mino == 1:
                data_position_p = fp.z_p(h, w, r, data_position_p)
                color = (0, 255, 0)
            elif mino == 2:
                data_position_p = fp.r_z_p(h, w, r, data_position_p)    
                color = (0, 255, 0) 
            elif mino == 3:
                data_position_p = fp.stick_p(h, w, r, data_position_p)
                color = (0, 255, 255) 
            elif mino == 4:
                data_position_p = fp.l_p(h, w, r, data_position_p)
                color = (255, 127, 0)
            elif mino == 5:
                data_position_p = fp.r_l_p(h, w, r, data_position_p)
                color = (255, 127, 0)
            elif mino == 6:
                data_position_p = fp.rec_p(h, w, r, data_position_p)
                color = (255, 255, 0) 
            elif mino == 7:
                data_position_p = fp.r_t_p(h, w, r, data_position_p)
                color = (255, 0, 0)


            wr_over = 0
            wl_over = 0
            h_over = 0
            for i, data in enumerate(data_position):
                row_count = 0
                for e, d in enumerate(data):
                    if i < 19:
                        if data_position_p[i][e] == 1 and  data_position[i + 1][e] == 1:
                            touch = 1
                    if data_position_p[i][e] == 1:
                        h = i * 20 
                        w = e * 20
                        pygame.draw.rect(screen, color, Rect(w, h, 20, 20), 0)
                        if i > 18:
                            h_over = 1
                        if e > 8:
                            wr_over = 1
                        if e < 1:
                            wl_over = 1
                    if data_position[i][e] == 1:
                        row_count += 1
                    if row_count >= 10:
                        del data_position[i]
                        del data_color[i]
                        array_a = [0] * 10
                        array_b = [(c_1)] * 10
                        data_position.insert(0, array_a)
                        data_color.insert(0, array_b)
                        fall_speed -= 1
                        
        line_y = 20
        line_x = 20
        while line_y < 400:
            pygame.draw.line(screen, c_0, (0, line_y), (200, line_y))
            line_y += 20
        while line_x < 200:
            pygame.draw.line(screen, c_0, (line_x, 0), (line_x, 400))
            line_x += 20

        a += 1
        if a > fall_speed:
            count = 1
            a = 0
        else:
            count = 0
        
        if y < 400 and touch == 0 and h_over == 0:
            if count == 1:
                y += 20 
        else:
            if y == 0:
                gameover = 1
            x = 80
            y = 0
            r = 0
            touch = 0
            mino = 0
            for i, data in enumerate(data_position_p):
                for e, d in enumerate(data):
                    if data_position_p[i][e] == 1 and data_position[i][e] == 0:
                        data_position[i][e] = 1
                        data_color[i][e] = color
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == ord('l'): #K_RIGHT
                    if x < 200 and wr_over == 0:
                        x += 20
                if event.key == ord('h'): #K_LEFT:
                    if x > 0 and wl_over == 0:
                        x -= 20
                if event.key == ord(' '): #K_UP:
                    if r >= 3:
                        r = 0
                    else:
                        r += 1
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    main()
