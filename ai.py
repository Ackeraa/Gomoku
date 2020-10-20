from alphaBeta import AlphaBeta

class Acker(object):
    def __init__(self, color):
        self.color = color
        self.alphaBeta = AlphaBeta(self.color, 2)
    
    def move(self, pos):
        return self.alphaBeta.move(pos)

   

        

