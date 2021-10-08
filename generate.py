#!/usr/bin/env python
# encoding: utf-8
"""
@author: Shanda Lau 刘祥德
@license: (C) Copyright 2019-now, Node Supply Chain Manager Corporation Limited.
@contact: shandalaulv@gmail.com
@software: 
@file: user_study.py
@time: 5/20/20 10:47 AM
@version 1.0
@desc:
"""
from pathlib import Path
from posixpath import join
import cv2
import os
from random import sample
from multiprocessing import Process
import shutil
import time


def select_samples(data_dir, person_name, output_path, prefix, num_samples=1):
    filenames = os.listdir(os.path.join(data_dir, person_name))
    selected_filenames = sample(filenames, num_samples)
    return [[
        os.path.join(data_dir, person_name, filename),
        os.path.join(output_path, f'{prefix}_{idx}{filename[-4:]}')
    ] for idx, filename in enumerate(selected_filenames)]


def select_handcraft(data_dir,
                     person_name,
                     output_path,
                     prefix,
                     nums_samples=1):
    filenames = [
        filename
        for filename in os.listdir(os.path.join(data_dir, person_name))
        if filename[0] == 'C'
    ]
    selected_filenames = sample(filenames, nums_samples)
    return [[
        os.path.join(data_dir, person_name, filename),
        os.path.join(output_path, f'{prefix}_{idx}{filename[-4:]}')
    ] for idx, filename in enumerate(selected_filenames)]


def parse_original_photo_info(person_name):
    person_name, extention = person_name[:-4], person_name[-4:]
    person_name = person_name.replace(' ', '_')
    person_name = person_name.replace('_', ' ')
    pns = person_name.split(' ')
    original_pn = ''
    original_photo_id = f'{pns[-1]}'
    for idx, pn in enumerate(pns[:-1]):
        if idx == 0:
            original_pn += pn
        else:
            original_pn += f' {pn}'
    return original_pn, original_photo_id


def compose(
    testset_dir,
    photo_dir,
    CAST_dir,
    WarpGAN_dir,
    CariGAN_dir,
    output_dir,
):

    filenames = os.listdir(testset_dir)
    for filename in filenames:
        # CAST
        person_name, photo_id = parse_original_photo_info(filename)
        person_output_dir = os.path.join(output_dir, person_name)
        os.makedirs(person_output_dir, exist_ok=True)
        real_samples = [[
            os.path.join(testset_dir, filename),
            os.path.join(person_output_dir, f'0_Person_0.{filename[-4:]}'),
        ]]
        cast_samples = select_samples(CAST_dir,
                                      filename[:-4].replace(' ', '_'),
                                      person_output_dir,
                                      prefix='1_CAST')
        warpgan_samples = select_samples(WarpGAN_dir,
                                         person_name,
                                         person_output_dir,
                                         prefix='2_WarpGAN')
        carigan_samples = select_samples(CariGAN_dir,
                                         person_name,
                                         person_output_dir,
                                         prefix='3_CariGAN')
        handcraft_samples = select_handcraft(photo_dir,
         person_name,
         person_output_dir,
         prefix='4_HandCraft')
        samples = real_samples + cast_samples + warpgan_samples + carigan_samples + handcraft_samples
        # samples = real_samples + cast_samples + warpgan_samples + carigan_samples
        for idx, (src_path, output_path) in enumerate(samples):
            print(f'Processing {src_path} to {output_path}')
            shutil.copy(src_path, output_path)


if __name__ == '__main__':

    datatime = time.strftime("%Y-%m-%d-%H%M%S", time.localtime())
    testset_dir = '/data/lxd/datasets/contents_original'
    photo_dir = '/data/lxd/datasets/WebCari_512/img'
    CAST_dir = '/data/lxd/datasets/UserStudy/2021-05-16-CAST'
    WarpGAN_dir = '/data/lxd/datasets/UserStudy/2021-10-04-WarpGAN'
    CariGAN_dir = '/data/lxd/datasets/UserStudy/2021-10-04-CariGAN'
    output_dir = f'data/{datatime}-data'
    compose(testset_dir, photo_dir, CAST_dir, WarpGAN_dir, CariGAN_dir,
            output_dir)
