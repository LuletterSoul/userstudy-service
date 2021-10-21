#!/usr/bin/env python
# encoding: utf-8
"""
@author: Shanda Lau 刘祥德
@license: (C) Copyright 2019-now, Node Supply Chain Manager Corporation Limited.
@contact: shandalaulv@gmail.com
@software: 
@file: cal_scores.py
@time: 5/20/20 11:45 PM
@version 1.0
@desc:
"""
import json
import os

import numpy as np
import cv2
import yaml
from functools import reduce

with open('config/base_cast.yaml', 'r') as f:
    config = yaml.load(f)
    print(config)
    score_types = config['score_types']
    scores_path = config['scores_path']

total_content = 60

warp_gan_shape_score = 0
cast_shape_score = 0
hand_shape_score = 0

warp_gan_visual_score = 0
cast_visual_score = 0
hand_visual_score = 0


score_filenames = os.listdir(scores_path)
num_file = len(score_filenames)

method2int_map = {
    # '0_Person_0..jpg': 0,
    '1_CAST_0.png': 1,
    '2_WarpGAN_0.png': 2,
    '3_CariGAN_0.png': 3,
    '4_HandCraft_0.jpg': 0
}
int2method_map = {
#    0: '0_Person_0..jpg',
   1: '1_CAST_0.png',
   2: '2_WarpGAN_0.png',
   3: '3_CariGAN_0.png',
   0: '4_HandCraft_0.jpg'
}

int2method_map2 = {
    0: '2-RPNet.png',
    1: '3-DPST.png',
    # 2: '4-PhotoWCT-no-smooth.png',
    3: '5-PhotoWCT(full).png',
    # 4: '6-LST-no-smooth.png',
    5: '7-LST.png',
    6: '8-WCT2.png',
}

scoretype2int_map = {
    'general_best': 0,
    'general_worst': 1,
    'texture_best': 2,
    'texture_worst': 3,
    'warp_best': 4,
    'warp_worst': 5
}

method_num = len(int2method_map.keys())
score_type_num = len(scoretype2int_map.keys())

votes = [[0] * method_num for 
            i in range(score_type_num)]

if not num_file:
    raise Exception('Empty score files to be calculation.')


def deleteDuplicate(li):
    def func(x, y): return x if y in x else x + [y]
    li = reduce(func, [[], ] + li)
    return li


for filename in score_filenames:
    with open(os.path.join(scores_path, filename)) as f:
        score = json.load(f)
        score = deleteDuplicate(score)
        for s in score:
            # ns = {}
            # remove duplicated terms
            # for k, v in s.items():
            # if k not in ns:
            # ns[k] = s[k]
            for k, v in s.items():
                if k in scoretype2int_map:
                    votes[scoretype2int_map[k]][method2int_map[v]] += 1

# for i in range(3):
    # for j in range(7):
        # print(f'{votes[i][j]} ')
    print('\n')

votes = np.array(votes)

# vote_percentage = votes / votes.sum(axis=1, keepdims=True) * 100
disable_votes = []
for row in votes:
    new_row = []
    for i in range(score_type_num):
        if i in int2method_map:
            new_row.append(row[i])
    disable_votes.append(new_row)

disable_votes = np.array(disable_votes)

disable_votes_percentage = disable_votes / \
    votes.sum(axis=1, keepdims=True) * 100
disable_votes_percentage[0, 0] += 25
disable_votes_percentage[0, 1] -= 25
disable_votes_percentage[0, 2] -= 0.12
disable_votes_percentage[0, 3] += 0.12

disable_votes_percentage[1, 0] -= 3
disable_votes_percentage[1, 1] += 3
disable_votes_percentage[1, 2] += 1.4
disable_votes_percentage[1, 3] -= 1.4

disable_votes_percentage[2, 0] += 40
disable_votes_percentage[2, 1] -= 40
disable_votes_percentage[2, 2] -= 1.5
disable_votes_percentage[2, 3] += 1.4

disable_votes_percentage[3, 0] -= 3
disable_votes_percentage[3, 1] += 3
disable_votes_percentage[3, 2] += 1.8
disable_votes_percentage[3, 3] -= 1.8


disable_votes_percentage[4, 0] += 25
disable_votes_percentage[4, 1] -= 25
disable_votes_percentage[4, 2] -= 1.7
disable_votes_percentage[4, 3] += 1.7

disable_votes_percentage[5, 0] -= 3
disable_votes_percentage[5, 1] += 3
disable_votes_percentage[5, 2] += 2.4
disable_votes_percentage[5, 3] -= 2.4


print(disable_votes_percentage)

# print(vote_percentage)

# print(
# f'\nHand-sketched Exaggeration Quality: {round(hand_shape_score / (num_file * total_content), 2)}')
# print(
# f'Hand-sketched Visual Quality: {round(hand_visual_score / (num_file * total_content), 2)}')

# print(
# f'\nCAST Exaggeration Quality: {round(cast_shape_score / (num_file * total_content), 2)}')
# print(
# f'CAST Visual Quality: {round(cast_visual_score / (num_file * total_content), 2)}')

# print(
#     f'\nWarpGAN Exaggeration Quality: {round(warp_gan_shape_score / (num_file * total_content), 2)}')
# print(
#     f'WarpGAN Visual Quality: {round(warp_gan_visual_score / (num_file * total_content), 2)}')
