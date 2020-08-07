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

with open('config/base.yaml') as f:
    config = yaml.load(f)
    score_structure = config['score_types']
    cmp_methods = config['cmp_methods']
    study_group_num = config['study_group_num']

warp_gan_shape_score = 0
cast_shape_score = 0
hand_shape_score = 0

warp_gan_visual_score = 0
cast_visual_score = 0
hand_visual_score = 0

score_matrix = [[0] * len(score_structure) for i in range(len(cmp_methods))]

score_filenames = os.listdir('scores')
user_num = len(score_filenames)
if not user_num:
    raise Exception('Empty score files to be calculation.')

for filename in score_filenames:
    with open(os.path.join('scores', filename)) as f:
        score = json.load(f)
        print(len(score))
        for s in score:
            cnt = 0
            for m_id, method in enumerate(cmp_methods):
                for s_id, score_item in enumerate(score_structure):
                    if s['content'].endswith(method):
                        score_matrix[m_id][s_id] += s[score_item['score_type']]

print(score_matrix)
for m_id, method in enumerate(cmp_methods):
    print(f'\n')
    for s_id, score_item in enumerate(score_structure):
        effect = score_item['effect']
        print(f'{method} {effect}: {round(score_matrix[m_id][s_id] / (user_num * study_group_num),2)}')
