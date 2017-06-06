#!/usr/bin/env python
# encoding: utf-8

from table import TABLE,row,col, black, white,space
from evaluate import evaluate_line
from copy import deepcopy

class NODE():
    def __init__(self, table,deep,  status):
        self.table = table
        self.status = status
        self.deep = deep
        self.pos_i = -1
        self.pos_j = -1

    def move(self, i, j, status):
        self.table.move(i, j, status)

    def traverse(self):
        for i in xrange(0, row):
            for j in xrange(0, col):
                if self.table.table[i][j] != space:
                    continue
                #如果一个棋两步以内都没有棋，那么就跳过
                next_status = black ^ self.status ^white
                new_node = NODE(deepcopy(self.table), self.deep-1, next_status)
                new_node.move(i, j, self.status)

                yield new_node, i, j

    def evaluateNega(self):
        return - self.evaluate()


    def evaluate(self):
        # 用遍历法获取当前四个方向的棋子情况，这里可以用启发式来做，先用遍历，再简化

        # 1. 获得72个向量
        vecs = []
        # 1.1 '---' *15
        for i in xrange(0, row):
            vecs.append(self.table.table[i])
        # 1.2 '|' * 15
        for j in xrange(0, col):
            vecs.append([self.table.table[i][j] for i in range(0, row)])

        # 1.3 '\' *21
        vecs.append([self.table.table[x][x] for x in range(0,row)])
        for i in xrange(1, row-4):
            vec = [self.table.table[x][x-i] for x in range(i, row)]
            vecs.append(vec)
            vec = [self.table.table[y-i][y] for y in range(i, col)]
            vecs.append(vec)
            #print [(y-i,y) for y in range(i, col)]

        # 1.4 '/'*21
        #vecs.append([self.table.table[x][row-x-1] for x in range(0, row)])
        #print [(x, row-x-1) for x in xrange(0, row)]
        for i in xrange(4, row-1):
            vec = [self.table.table[x][i-x] for x in xrange(i, -1, -1)]
            vecs.append(vec)
            vec = [self.table.table[x][col-x+row-i-2] for x in xrange(row-i-1, row)]
            vecs.append(vec)
            #print [(x,i-x) for x in xrange(i,-1,-1)]
            #print [(x,col-x+row-i-2) for x in xrange(row-i-1, row)]

        # 2. 对每个向量进行算分，获取总分
        table_score = 0
        for vec in vecs:
            score = evaluate_line(vec)
            if self.status == black:
                #上一手是白棋，计算对白棋的分数
                table_score += score[white][0]-score[black][0] - score[black][1]
            else:
                #上一手是黑棋, 计算对黑棋的分数
                table_score += score[black][0]-score[white][0] - score[white][1]

        return table_score

def miniMax(node):
    if node.deep <= 0:
        score = node.evaluateNega()
        return score
    score = -10000000
    for new_node, i, j in  node.traverse():
        new_score = -miniMax(new_node)
        if new_score > score:
            score = new_score
            node.pos_i, node.pos_j = i, j
    return score

def alphaBeta(node, alpha=-1000000, beta=1000000):
    if node.deep <= 0:
        score = node.evaluateNega()
        return score
    for new_node, i, j in node.traverse():
        new_score = -alphaBeta(new_node, -beta, -alpha)
        if new_score > beta:
            return beta
        if new_score > alpha:
            alpha = new_score
            node.pos_i, node.pos_j = i, j
    return alpha




if __name__=='__main__':
    table = TABLE()
    node = NODE(table, 10, black)

    alphaBeta(node)





