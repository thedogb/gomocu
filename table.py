#!/usr/bin/env python
# encoding: utf-8

col = 15
row = 15

black = 1
white = -1
space = 0
dead = -2

class MoveERROR(Exception):
    def __init__(self, arg):
        self.args = arg

class TABLE():
    def __init__(self, plane=None):
        if plane == None:
            self.table = [ [0]*col for i in xrange(row)]
        else:
            self.table = plane

    def get(self, i, j):
        if i < 0 or i >= row or j < 0 or j >=col:
            return space
        return self.table[i][j]


    def move(self, x, y, status):
        if status != black and status != white:
            raise MoveERROR(['No such status:' + str(status)])
        if 0 <= x< row and 0<=y<col:
            if self.table[x][y] != space:
                raise MoveERROR(['The Place has been placed'])
            self.table[x][y] = status
        else:
            raise MoveERROR(['move beyond border:(%d,%d)'%(x, y)])

    def judge(self, x, y, status):
        status = self.table[x][y]
        if status == space:
            return False

        # judge '-----'
        for i in xrange(x-4, x+5):
            if self.get(i, y)==status \
                    and self.get(i+1,y) == status \
                    and self.get(i+2,y) == status \
                    and self.get(i+3,y) == status \
                    and self.get(i+4,y) == status :
                return True
        # judge '|'
        for j in xrange(y-4, y+5):
            if self.get(x,j)==status \
                    and self.get(x,j+1) == status \
                    and self.get(x,j+2) == status \
                    and self.get(x,j+3) == status \
                    and self.get(x,j+4) == status :
                return True

        # judge '\'
        j = y-4
        for i in xrange(x-4, x+5):
            if self.get(i, j)==status \
                    and self.get(i+1,j+1) == status \
                    and self.get(i+2,j+2) == status \
                    and self.get(i+3,j+3) == status \
                    and self.get(i+4,j+4) == status :
                return True
            j += 1

        # judge '/'
        i = x+4
        for j in xrange(y-4, y+5):
            if self.get(i,j)==status \
                    and self.get(i-1,j+1) == status \
                    and self.get(i-2,j+2) == status \
                    and self.get(i-3,j+3) == status \
                    and self.get(i-4,j+4) == status :
                return True
            i -=1
        return False


    def is_full(self):
        for i in xrange(0, row):
            for j in xrange(0, col):
                if self.table[i][j] == space:
                    return False
        return True



    def display(self):
        head = map(lambda i: hex(i)[2:].upper(), xrange(col))
        print '  ' + ' '.join(head)
        #print '--'*(col+1)
        for i in xrange(0, row):
            chs=[]
            for j in xrange(0, col):
                if self.table[i][j] == space:
                    ch = ' '
                elif self.table[i][j] == black:
                    ch = 'o'
                else:
                    ch = 'x'
                chs.append(ch)
            line = '%s|%s|'%(head[i], '|'.join(chs))
            print line


if __name__ == '__main__':
    t = TABLE()
    t.display()
#    j=10
#    for i in range(8,8+5):
#        t.move(i, j, black)
#        print t.judge(i, j, black)
#        j-=1
#    #t.move(0,1,white)
#    t.display()
#    import copy
#    b = copy.deepcopy(t)
#    b.display()
#    b.move(10,10,black)
#    b.display()
#    t.display()




