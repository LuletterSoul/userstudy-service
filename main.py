#!/usr/bin/env python
# encoding: utf-8
"""
@author: Shanda Lau 刘祥德
@license: (C) Copyright 2019-now, Node Supply Chain Manager Corporation Limited.
@contact: shandalaulv@gmail.com
@software: 
@file: http.py
@time: 2/7/20 11:43 AM
@version 1.0
@desc:
"""
import argparse
import os
import re
import yaml
from multiprocessing import Process

import shutil
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from pathlib import Path
import json
from random import shuffle, sample

app = Flask(__name__)
cors = CORS(app)


class VideoType:
    ORIGIN = 'original-streams'
    RENDER = 'render-streams'


def query_directory(dir_name):
    """
    return a directory folder tree recursively, exit if meet a file endpoint.
    :param dir_name:
    :return:
    """
    sun_dir_names = [l for l in os.listdir(dir_name) if not l.startswith('.')]
    if not len(sun_dir_names):
        return []

    return [{'value': d, 'label': d, 'children': query_directory(os.path.join(dir_name, d))} for d in sun_dir_names if
            os.path.isdir(os.path.join(dir_name, d))]


def query_directory_child_list(dir_name):
    """
    return a directory folder tree recursively, exit if meet a file endpoint.
    :param dir_name:
    :return:
    """
    sun_dir_names = [l for l in sample(os.listdir(dir_name), 100) if not l.startswith('.')]
    # print(len(sun_dir_names))
    if not len(sun_dir_names):
        return []
    # sun_dir_names = sort_humanly(sun_dir_names)
    shuffle(sun_dir_names)
    li = []
    for d in sun_dir_names:
        filelist, indexlist = sort_humanly([ls for ls in os.listdir(os.path.join(dir_name, d))])
        li.append({'content': d, 'filenames': filelist, 'index': indexlist})
    return li
    # return [{'content': d, 'filenames': sort_humanly([ls for ls in os.listdir(os.path.join(dir_name, d))])}
    #         for d in
    #         sun_dir_names]


def tryint(s):  # 将元素中的数字转换为int后再排序
    try:
        return int(s)
    except ValueError:
        return s


def str2int(v_str):  # 将元素中的字符串和数字分割开
    return [tryint(sub_str) for sub_str in re.split('([0-9]+)', v_str)]


def sort_humanly(v_list):  # 以分割后的list为单位进行排序
    """
    sort list strings according string and number
    :param v_list:
    :return:
    """
    list = []
    list.append(v_list[4])
    index = [0, 1, 2, 3, 5]
    shuffle(index)
    for i in index:
        list.append(v_list[i])
    print(list)
    print(index)
    # print(sorted(v_list, key=str2int))
    return list, index


config = None


class HttpServer(object):

    def __init__(self, host_ip="127.0.0.1", host_port="8080", env='dev', root=".",
                 config_path='config/base_caricature.yaml'):
        self.host_ip = host_ip
        self.host_port = host_port
        self.env = env
        self.set_root(root)

        with open(config_path, encoding='UTF-8') as f:
            global config
            config = yaml.load(f)
            os.makedirs(config['data_path'], exist_ok=True)
            os.makedirs(config['scores_path'], exist_ok=True)

    @staticmethod
    @app.route('/photos/<content>/<filename>', methods=['GET'])
    def photos_by_content(content, filename):
        # url = f"{config['data_path']}/{content}/{filename}"
        url = os.path.join(config['data_path'], content, filename)
        url = url.replace('\\', '/')
        # print(url)
        return app.send_static_file(url)

    @staticmethod
    @app.route('/user_study', methods=['GET'])
    def user_study():
        data = query_directory_child_list(config['data_path'])
        # print(data)
        return jsonify(data)

    @staticmethod
    @app.route('/scores', methods=['POST'])
    def scores():
        json_data = json.loads(request.get_data().decode('utf-8'))
        scores_res = json_data['scores']
        user_id = json_data['user_id']
        for task, scores in scores_res.items():
            score_path = f'scores/{user_id}_{task}.json'
            # if os.path.exists(score_path):
            #     order = len(list(Path('scores').glob(f'{user_id}*')))
            #     score_path = f'scores/{user_id}_{order}.json'
            with open(score_path, 'w') as fw:
                fw.write(json.dumps(scores, indent=4))
                fw.close()
        return 'success'

    @staticmethod
    @app.route('/score_types', methods=['GET'])
    def scores_types():
        return jsonify(config['score_types'])

    @staticmethod
    def set_root(root):
        app.static_folder = root

    def run(self):
        Process(target=app.run, args=(self.host_ip, self.host_port, False,), daemon=True).start()

    def run_front(self):
        app.run(self.host_ip, self.host_port, False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default='prod',
                        help='System environment.')
    # parser.add_argument('--http_ip', type=str, default="10.196.122.94", help='Http server ip address')
    parser.add_argument('--http_ip', type=str, default="127.0.0.1", help='Http server ip address')
    parser.add_argument('--http_port', type=int, default=8080, help='Http server listen port')
    parser.add_argument('--root', type=str, default=".", help='Http server listen port')
    parser.add_argument('--config', type=str, default="config/base_caricature.yaml", help='Http server configuration')
    args = parser.parse_args()
    http = HttpServer(args.http_ip, args.http_port, root=args.root, config_path=args.config)
    http.run_front()
    # print(query_directory_child_list('user_study'))
