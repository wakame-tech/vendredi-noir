class FallsPosition:

    def __init__(self):

        pass
        

    def z_p(self, h, w, r, data_position_p):
        
        if r == 1:
            ix_li = [[0, 1], [1, 1], [1, 0], [2, 0]]
        elif r == 2 and w < 8:
            ix_li = [[0, 0], [0, 1], [1, 1], [1, 2]]
        elif r == 3:
            ix_li = [[0, 1], [1, 1], [1, 0], [2, 0]]
        elif r == 0 and w < 8:
            ix_li = [[0, 0], [0, 1], [1, 1], [1, 2]]
        elif w > 7:
            data_position_p[h][w+1] = 1
            ix_li = [[0, 1], [1, 1], [1, 0], [2, 0]]

        for ix in ix_li:
            data_position_p[h+ix[0]][w+ix[1]] = 1

        return data_position_p


    def r_z_p(self,h,w,r,data_position_p):
        
        if r == 1:
            ix_li = [[0, 0], [1, 0], [1, 1], [2, 1]]
        elif r == 2 and w < 8:
            ix_li = [[0, 1], [0, 2], [1, 1], [1, 0]]
        elif r == 3:
            ix_li = [[0, 0], [1, 0], [1, 1], [2, 1]]
        elif r == 0 and w < 8:
            ix_li = [[0, 1], [0, 2], [1, 1], [1, 0]]
        elif w > 7:
            ix_li = [[0, 0], [1, 0], [1, 1], [2, 1]]

        for ix in ix_li:
            data_position_p[h+ix[0]][w+ix[1]] = 1
            
        return data_position_p


    def stick_p(self,h,w,r,data_position_p):
        
        if r == 0:
            ix_li = [[0, 0], [1, 0], [2, 0], [3, 0]]
        if r == 1 and w < 9 and w > 1:
            ix_li = [[2, -2], [2, -1], [2, 0], [2, 1]]
        if r == 2:
            ix_li = [[0, 0], [1, 0], [2, 0], [3, 0]]
        if r == 3 and w < 9 and w > 1:
            ix_li = [[1, -2], [1, -1], [1, 0], [1, 1]]
        elif w > 8 or w < 2:    
            ix_li = [[0, 0], [1, 0], [2, 0], [3, 0]]

        for ix in ix_li:
            data_position_p[h+ix[0]][w+ix[1]] = 1

        return data_position_p


    def l_p(self,h,w,r,data_position_p):
        
        if r == 0:
            ix_li = [[0, 0], [1, 0], [2, 0], [2, 1]]
        if r == 1 and w < 8:
            ix_li = [[0, 2], [1, 2], [1, 1], [1, 0]]
        elif r == 1 and w > 7:
            ix_li = [[0, 0], [1, 0], [2, 0], [2, 1]]
        if r == 2:
            ix_li = [[0, 0], [0, 1], [1, 1], [2, 1]]
        if r == 3 and w < 8:
            ix_li = [[2, 0], [1, 0], [1, 1], [1, 2]]
        elif r == 3 and w > 7:
            ix_li = [[0, 0], [0, 1], [1, 1], [2, 1]]
        
        for ix in ix_li:
            data_position_p[h+ix[0]][w+ix[1]] = 1

        return data_position_p

    def r_l_p(self,h,w,r,data_position_p):
        
        if r == 0:
            ix_li = [[0, 1], [1, 1], [2, 1], [2, 0]]
        if r == 1 and w < 8:
            ix_li = [[0, 0], [0, 1], [0, 2], [1, 0]]
        elif r == 1 and w > 7:
            ix_li = [[0, 1], [1, 1], [2, 1], [2, 0]]
        if r == 2:
            ix_li = [[0, 0], [1, 0], [2, 0], [0, 1]]
        if r == 3 and w < 8:
            ix_li = [[0, 0], [1, 0], [1, 1], [1, 2]]
        elif r == 3 and w > 7:
            ix_li = [[0, 0], [1, 0], [2, 0], [0, 1]]

        for ix in ix_li:
            data_position_p[h+ix[0]][w+ix[1]] = 1

        return data_position_p


    def rec_p(self, h, w, r, data_position_p):
        
        if r == 0 or r == 1 or r == 2 or r == 3:
            ix_li = [[0, 0], [0, 1], [1, 1], [1, 0]]

        for ix in ix_li:
            data_position_p[h+ix[0]][w+ix[1]] = 1

        return data_position_p


    def r_t_p(self, h, w, r, data_position_p):
        
        if r == 0 and w < 9 and w > 0:
            ix_li = [[0, 0], [1, 1], [1, 0], [1, -1]]
        elif r == 0 and w > 8:
            ix_li = [[0, 0], [1, 0], [1, -1], [2, 0]]
        elif r == 0 and w < 1:
            ix_li = [[0, 0], [1, 0], [1, 1], [2, 0]]
        if r == 1 and w > 0:
            ix_li = [[0, 0], [1, 0], [1, -1], [2, 0]]
        elif r == 1 and w < 1:    
            ix_li = [[0, 0], [1, 0], [1, 1], [2, 0]]
        if r == 2 and w < 9 and w > 0:
            ix_li = [[1, 0], [1, -1], [2, 0], [1, 1]]
        elif r == 2 and w > 8:
            ix_li = [[0, 0], [1, 0], [1, -1], [2, 0]]
        elif r == 2 and w < 1:    
            ix_li = [[0, 0], [1, 0], [1, 1], [2, 0]]
        if r == 3 and w < 9:
            ix_li = [[0, 0], [1, 0], [1, 1], [2, 0]]
        elif r == 3 and w > 8:
            ix_li = [[0, 0], [1, 0], [1, -1], [2, 1]]

        for ix in ix_li:
            data_position_p[h+ix[0]][w+ix[1]] = 1

        return data_position_p
