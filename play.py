#!/usr/bin/env python
# encoding: utf-8

from table import TABLE,row,col, black, white,space
from miniMax import NODE, miniMax, alphaBeta

def play():
    table = TABLE()
    table.display()

    status = black
    deep = 2
    while True:
        node = NODE(table, deep, status)
        #score = miniMax(node)
        score = alphaBeta(node)
        print score
        x, y = node.pos_i, node.pos_j
        table.move(x, y, status)

        table.display()

        if table.judge(x, y, status):
            if status == black:
                print '黑棋胜利!'
            else:
                print '白棋胜利!'
            break
        elif table.is_full():
            print '棋盘已满， 平局'
        else:
            #交换手
            status = black ^ status ^ white
        raw_input()

if __name__ == '__main__':
    play()
