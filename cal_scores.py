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

with open('config/base.yaml', 'r') as f:
    score_types = yaml.load(f)['score_types']

total_content = 47

warp_gan_shape_score = 0
cast_shape_score = 0
hand_shape_score = 0

warp_gan_visual_score = 0
cast_visual_score = 0
hand_visual_score = 0

score_filenames = os.listdir('scores')
num_file = len(score_filenames)
if not num_file:
    raise Exception('Empty score files to be calculation.')

for filename in score_filenames:
    with open(os.path.join('scores', filename)) as f:
        score = json.load(f)
        cnt = 0
        for s in score:
            if s['content'].endswith('WarpGAN'):
                warp_gan_shape_score += s['shape_score']
                warp_gan_visual_score += s['visual_score']
            elif s['content'].endswith('CAST'):
                cast_shape_score += s['shape_score']
                cast_visual_score += s['visual_score']
            elif s['content'].endswith('hand'):
                cnt += 1
                hand_shape_score += s['shape_score']
                hand_visual_score += s['visual_score']
        print(cnt)

print(f'\nHand-sketched Exaggeration Quality: {round(hand_shape_score / (num_file * total_content), 2)}')
print(f'Hand-sketched Visual Quality: {round(hand_visual_score / (num_file * total_content), 2)}')

print(f'\nCAST Exaggeration Quality: {round(cast_shape_score / (num_file * total_content), 2)}')
print(f'CAST Visual Quality: {round(cast_visual_score / (num_file * total_content), 2)}')

print(f'\nWarpGAN Exaggeration Quality: {round(warp_gan_shape_score / (num_file * total_content), 2)}')
print(f'WarpGAN Visual Quality: {round(warp_gan_visual_score / (num_file * total_content), 2)}')
