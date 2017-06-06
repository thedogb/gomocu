#!/usr/bin/env python
# encoding: utf-8

from table import black, white,space, dead

huo_score = [0,1,10,100,1000,10000]
tiao_score= [0, 0, 6, 60, 800, 900]
mian_score = [0, 0, 3, 40, 800, 10000]
mian_tiao_score = [0,0,2,35,700,800]
dead_tiao_score = [0,0,0,0,600,600]
dead_score = [0,0,0,0,0,10000]
punish_score = 450

def evaluate_line(line):
    # 1. 统计连续相同的子数
    item =[[line[0], 1,False]]
    index = 0
    for i in xrange(1, len(line)):
        if line[i] == item[index][0]:
            item[index][1] += 1
        else:
            index += 1
            item.append([line[i], 1, False])
    merge_item = [item[0]]

    # 2. 对‘嵌’这个情况进行合并
    i = 1
    while i < len(item)-1:
        color, color_num, _= item[i]
        last_color, last_color_num, _ = item[i-1]
        after_color, after_color_num, _ = item[i+1]
        if color == space and color_num == 1 and last_color == after_color and last_color != space and last_color_num < 4 and after_color_num <4:
            # 有嵌存在,并且合并方不超过4*，进行合并
            it = (last_color, last_color_num +  after_color_num, True)
            if merge_item[-1][2] == False:
                # 不是连跳
                merge_item.pop()
            else:
                #print '连跳，中间加个空格'
                merge_item.append((space,1,False))
            merge_item.append(it)
            i+=2
        else:
            # 无嵌存在
            merge_item.append(item[i])
            i+=1
    if i < len(item):
        #不是以嵌结束的，要补上最后一项
        merge_item.append(item[-1])

    # 3. 给首尾加上两个禁手，方便之后的判别
    merge_item = [(dead, 1, False)] + merge_item + [(dead, 1, False)]
    #print merge_item

    # 4. 统计分数
    score = {
            black:[0,0],
            white:[0,0]
            }

    for i in xrange(1, len(merge_item)-1):
        color, color_num, flag = merge_item[i]
        last_color, last_color_num, last_flag = merge_item[i-1]
        after_color, after_color_num, after_flag = merge_item[i+1]

        if color == space:
            continue

        color_num = 5 if color_num >=5 else color_num
        if flag==False and color_num >= 5:
            # 已连成5星
            score[color][0] += huo_score[color_num]
        elif last_color == after_color == space:
            if flag == False:
                #print color, '活', color_num
                # 活
                score[color][0] += huo_score[color_num]
                if color_num >= 4:
                    score[color][1] += punish_score
            else:
                #print '跳'
                # 跳
                score[color][0] += tiao_score[color_num]
                if color_num >= 4:
                    score[color][1] += punish_score
        elif ((last_color == space  and after_color != color) or (last_color != color and after_color == space )):
            if flag == False:
                #print '眠'
                # 眠
                score[color][0] += mian_score[color_num]
                if color_num >= 4:
                    score[color][1] += punish_score
            else:
                #print '眠跳'
                # 眠跳
                score[color][0] += mian_tiao_score[color_num]
                if color_num >= 4:
                    score[color][1] += punish_score
        else:
            if flag == False:
                #print '死'
                # 死
                score[color][0] += dead_score[color_num]
            else:
                # 死跳
                #print '死跳'
                score[color][0] += dead_tiao_score[color_num]
                if color_num >= 4:
                    score[color][1] += punish_score
    #if score[black][0] > 0 or score[white][0] > 0:
    #    print score
    #    print line
    #    raw_input()
    return score


if __name__ == '__main__':
    line = [1, 1, 1, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    print line
    score = evaluate_line(line)
    print 'black:', score[black]
    print 'white:', score[white]
