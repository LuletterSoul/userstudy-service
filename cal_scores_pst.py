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

with open('config/base_pst.yaml', 'r') as f:
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
votes = [[0] * 7 for i in range(3)]

method2int_map = {
    '2-RPNet.png': 0,
    '3-DPST.png': 1,
    '4-PhotoWCT-no-smooth.png': 2,
    '5-PhotoWCT(full).png': 3,
    '6-LST-no-smooth.png': 4,
    '7-LST.png': 5,
    '8-WCT2.png': 6
}
int2method_map = {
    0: '2-RPNet.png',
    1: '3-DPST.png',
    2: '4-PhotoWCT-no-smooth.png',
    3: '5-PhotoWCT(full).png',
    4: '6-LST-no-smooth.png',
    5: '7-LST.png',
    6: '8-WCT2.png',
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
    'structural_best': 0,
    'stylization_best': 1,
    'photolism_best': 2
}

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
    for i in range(7):
        if i in int2method_map2:
            new_row.append(row[i])
    disable_votes.append(new_row)

disable_votes = np.array(disable_votes)

disable_votes_percentage = disable_votes / \
    votes.sum(axis=1, keepdims=True) * 100

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
