#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Nine Six """
""" grid.py """
""" Copyright 2019, Jogle Lew """

import os
import random as rnd
import codecs
import more_itertools
import numpy as np
from sklearn.model_selection import ParameterGrid
import six
import shutil
import subprocess
import sys
import argparse
import json
rnd.seed(123)

class GridSearch():
    def __init__(self):
        self.cmd_env = ""
        self.cmd_template = "" 
        self.gpus = [0]
        self.param_grid = {}

    def generate_grid_search(self):
        cmd_env = self.cmd_env
        cmd_template = self.cmd_template 
        gpus = self.gpus
        param_grid = self.param_grid
        if os.path.exists('grid'):
            shutil.rmtree('grid')
        os.mkdir('grid')
        cmd_list = []
        for setting in ParameterGrid(param_grid):
            cmd_list.append("NINESIX_CONFIG='" + json.dumps(setting) + "' " + cmd_template)
        print('#cmd:', len(cmd_list))

        # shuffle and divide cmds to different gpus
        rnd.shuffle(cmd_list)
        cmd_bucket_list = more_itertools.divide(len(gpus), cmd_list)
        for i, gpu_id in enumerate(gpus):
            with codecs.open('grid/grid.%s.sh' % (gpu_id,), 'w', 'utf-8') as f_out:
                f_out.write(cmd_env)
                f_out.write('\n'.join(map(lambda x: 'CUDA_VISIBLE_DEVICES=%d %s' % (gpu_id, x), cmd_bucket_list[i])) + '\n')

    def execute_script(self):
        grid_scripts = os.listdir('grid')
        sub_processes = []
        for grid_script in grid_scripts:
            child = subprocess.Popen(['bash', os.path.join('grid', grid_script)])
            sub_processes.append(child)
        for proc in sub_processes:
            proc.wait()


def main():
    parser = argparse.ArgumentParser(description="Nine Six Grid Search Planner")
    parser.add_argument('--param', '-p', action='append', nargs='+', help='assign hyperparameter and its values. Example 1: -p lr 0.1 0.01 0.001; Example 2: -p epoch 100 to 200 jump 10')
    parser.add_argument('--gpu', '-g', action='store', nargs='+', type=int, default=[0], help='assign graphic cards. Example: -g 1 3 5')
    parser.add_argument('--cmd', '-c', action='store', nargs="+", required=True, help='assign default command to start program')
    args = parser.parse_args()
    gs = GridSearch()
    gs.cmd_template = ' '.join(args.cmd)
    gs.gpus = args.gpu
    param_grid = {}
    for item in args.param:
        param_name = item[0]
        if len(item) == 4 and item[2] == "to":
            from_val = eval(item[1])
            to_val = eval(item[3])
            value = list(range(from_val, to_val))
        elif len(item) == 6 and item[2] == "to" and item[4] == "jump":
            from_val = eval(item[1])
            to_val = eval(item[3])
            jump_val = eval(item[5])
            value = list(range(from_val, to_val, jump_val))
        else:
            value = list(map(eval, item[1:]))
        param_grid[param_name] = value
    gs.param_grid = param_grid
    gs.generate_grid_search()
    gs.execute_script()


if __name__ == "__main__":
    main()
