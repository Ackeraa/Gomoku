from math import inf as INF
from multiset import Multiset as set
import copy
import random

class AlphaBeta(object):
    def __init__(self, color, depth):
        self.color = color
        self.depth = depth
        self.board = [[-1 for _ in range(20)] for _ in range(20)]
        self.moveTo = None
        self.dirs = [[-1, 0], [1, 0], [0, -1], [0, 1], [1, 1], [-1, -1], [1, -1], [-1, 1]]
        self.evals = {"ooooo": 50000, "*oooo*": 4320, "*ooo**": 720, "**ooo*": 720,
                       "*oo*o*": 720, "*o*oo*": 720, "oooo*": 720, "*oooo": 720,
                       "oo*oo": 720, "o*ooo": 720, "ooo*o": 720, "**oo**": 120,
                       "**o*o*": 120, "*o*o**": 120, "***o**": 20, "**o***": 20, 
                       "**o**#": 20, "#**o**": 20
                     }
        self.legal_pos = set()
    
    def is_legal(self, x, y):
        return x >= 0 and x < 15 and y >= 0 and y < 15 and self.board[x][y] == -1
    
    def add_legal_pos(self, pos):
        # Remove the position moved to.
        if pos in self.legal_pos:
            self.legal_pos.remove(pos, 1)

        # Add surronded positions. 
        for i in range(1, 3):
            for j in range(1, 3):
                for dir in self.dirs:
                    x = pos[0] + i * dir[0]
                    y = pos[1] + j * dir[1]
                    if self.is_legal(x, y):
                        self.legal_pos.add((x, y))
    
    def remove_legal_pos(self, pos):
        # Add the position moved to.
        self.legal_pos.add(pos)

        # Remove surronded positions. 
        for i in range(1, 3):
            for j in range(1, 3):
                for dir in self.dirs:
                    x = pos[0] + i * dir[0]
                    y = pos[1] + j * dir[1]
                    if self.is_legal(x, y) and (x, y) in self.legal_pos:
                        self.legal_pos.remove((x, y), 1)

    def move(self, pos):
        # If AI move first, always move to (7, 7).
        if pos[0] == -1:
            self.board[7][7] = self.color
            return -1

        self.board[pos[0]][pos[1]] = self.color ^ 1
        if self.is_someone_win(pos[0], pos[1]):
            return [-1]
        
        # Add legal positions.
        self.legal_pos = set()
        for i in range(15):
            for j in range(15):
                if (self.board[i][j] != -1):
                    self.add_legal_pos((i, j))

        print("Legal positions: ")
        print(self.legal_pos.items())

        self.fuck = 0
        self.moveTo = [-1, -1]
        self.alphaBeta(self.color, self.depth, (0, 0), -INF, INF)

        print("---------SIZE:", len(self.legal_pos.items()))

        self.board[self.moveTo[0]][self.moveTo[1]] = self.color
        if self.is_someone_win(self.moveTo[0], self.moveTo[1]):
            return [self.moveTo[0], self.moveTo[1], -1]

        print("Player moved:", pos)
        print("AI moved:", self.moveTo)
        print("Total steps:", self.fuck)
        sum1 = self.evaluate(self.color, 1)
        sum2 = self.evaluate(self.color ^ 1, 1)
        print("SUM1:", sum1, "SUM2:", sum2)

        return self.moveTo

    def is_someone_win(self, x, y):
        # Check Column
        xx = x
        cnt = 0
        while xx < 15 and self.board[xx][y] == self.board[x][y]:
            xx += 1
            cnt += 1
        xx = x - 1
        while xx >= 0 and self.board[xx][y] == self.board[x][y]:
            xx -= 1
            cnt += 1
        if cnt >= 5:
            return True
        
        # Check Row
        yy = y
        cnt = 0
        while yy < 15 and self.board[x][yy] == self.board[x][y]:
            yy += 1
            cnt += 1
        yy = y - 1
        while yy >= 0 and self.board[x][yy] == self.board[x][y]:
            yy -= 1
            cnt += 1
        if cnt >= 5:
            return True
        
        # Check Diagonal
        xx = x
        yy = y
        cnt = 0
        while xx < 15 and yy < 15 and self.board[xx][yy] == self.board[x][y]:
            xx += 1
            yy += 1
            cnt += 1
        xx = x - 1
        yy = y - 1
        while xx >= 0 and yy >= 0 and self.board[xx][yy] == self.board[x][y]:
            xx -= 1
            yy -= 1
            cnt += 1
        if cnt >= 5:
            return True
        
        # Check Back-Diagonal
        xx = x
        yy = y
        cnt = 0
        while xx >= 0 and yy < 15 and self.board[xx][yy] == self.board[x][y]:
            xx -= 1
            yy += 1
            cnt += 1
        xx = x + 1
        yy = y - 1
        while xx < 15 and yy >= 0 and self.board[xx][yy] == self.board[x][y]:
            xx += 1
            yy -= 1
        if cnt >= 5:
            return True
        
        return False
        
    def evaluate(self, player, flag):
        lx = ly = 15
        rx = ry = 0
        for ((x, y), z) in self.legal_pos.items():
            lx = min(lx, x)
            rx = max(rx, x)
            ly = min(ly, y)
            ry = max(ry, y)
        rx += 1
        ry += 1
        print("CCCCCCCCCCCCCCCCCCCCCCCC", lx, rx, ly, ry)

        s = row = col = ""
        for i in range(lx, rx):
            for j in range(ly, ry):
                # Evaluate Row 
                if self.board[i][j] == player:
                    row += "o"
                elif self.board[i][j] == -1:
                    row += "*"
                else:
                    row += "#"

                # Evaluate Column 
                if self.board[j][i] == player:
                    col += "o"
                elif self.board[j][i] == -1:
                    col += "*"
                else:
                    col += "#" 
            row += "#"
            col += "#"

        s = s + row + col

        dia1 = dia2 = bdia1 = bdia2 = ""
        for i in range(lx, rx):
            if i + 1 > ry:
                break
            for j in range(ly, i + 1):
                # Evaluate Diagonal left bottom
                if self.board[15 - i - 1 + j][j] == player:
                    dia1 += "o"
                elif self.board[15 - i - 1 + j][j] == -1:
                    dia1 += "*"
                else:
                    dia1 += "#"
                
                # Evaluate Diagonal right top
                if i != 14:
                    if self.board[j][15 - i - 1 + j] == player:
                        dia2 += "o"
                    elif self.board[j][15 - i - 1 + j] == -1:
                        dia2 += "*"
                    else:
                        dia2 += "#"

                # Evaluate Back-Diagonal left top
                if self.board[j][i - j] == player:
                    bdia1 += "o"
                elif self.board[j][i - j] == -1:
                    bdia1 += "*"
                else:
                    bdia1 += "#"
                
                # Evaluate Back-Diagonal right bottom
                if i != 14:
                    if self.board[15 - i - 1 + j][15 - 1 - j] == player:
                        bdia2 += "o"
                    elif self.board[15 - i - 1 + j][15 - 1 - j] == -1:
                        bdia2 += "*"
                    else:
                        bdia2 += "#"

            dia1 += "#"
            dia2 += "#"
            bdia1 += "#"
            bdia2 += "#"

        s = s + dia1 + dia2 + bdia1 + bdia2
        
        if flag:
            print("dia1:")
            num = 0
            for i in range(lx, rx):
                if i + 1 > ry:
                    break
                for j in range(ly, i + 1):
                    print(bdia1[num], end="")
                    num += 1
                num += 1
                print("")
            # print("col:", col)
            # print("dia1:", dia1)
            # print("dia2:", dia2)
            # print("bdia1:", bdia1)
            # print("bdia2:", bdia2)

        sum = 0
        for i in range(len(s)):
            if s[i] == '#':
                continue
            sub_s1 = s[i : i + 5]
            sub_s2 = s[i : i + 6]
            if sub_s1 in self.evals:
                sum += self.evals[sub_s1]
            if sub_s2 in self.evals:
                sum += self.evals[sub_s2]

        return sum

    def alphaBeta(self, player, depth, pos, alpha, beta):

        if pos != (0, 0) and self.is_someone_win(pos[0], pos[1]):
            if player == self.color:
                return -1000000
            else:
                return 1000000

        if depth == 0:
            self.fuck += 1
            sum1 = self.evaluate(self.color, 0)
            sum2 = self.evaluate(self.color ^ 1, 0)
            #print("SUM1:", sum1)
            #print("SUM2", sum2)
            return sum1 - sum2

        saved_legal_pos = copy.deepcopy(self.legal_pos)
        if player == self.color:
            for ((x, y), z) in saved_legal_pos.items():
                self.board[x][y] = player
                # self.legal_pos.remove((x, y))
                #print(f"depth: {depth}, before add, len(legal_pos): {len(self.legal_pos.items())}")
                #print(self.legal_pos.items())
                self.add_legal_pos((x, y))
                val = self.alphaBeta(player ^ 1, depth - 1, (x, y), alpha, beta)
                self.board[x][y] = -1
                # self.legal_pos.add((x, y))
                self.remove_legal_pos((x, y))
                #print(f"depth: {depth}, after removed, len(legal_pos): {len(self.legal_pos.items())}")
                #print(self.legal_pos.items())
                if val > alpha:
                    alpha = val
                    if depth == self.depth:
                        self.moveTo = [x, y]
                if alpha >= beta:
                    return alpha
            return alpha
        else:
            for ((x, y), z) in saved_legal_pos.items():
                self.board[x][y] = player
                # self.legal_pos.remove((x, y))
                #print(f"depth: {depth}, before add, len(legal_pos): {len(self.legal_pos)}")
                self.add_legal_pos((x, y))
                val = self.alphaBeta(player ^ 1, depth - 1, (x, y), alpha, beta)
                self.board[x][y] = -1
                # self.legal_pos.add((x, y))
                self.remove_legal_pos((x, y))
                #print(f"depth: {depth}, after removed, len(legal_pos): {len(self.legal_pos)}")
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return beta
            return beta
            
