# -*- coding: utf-8 -*-
# @Time    : 2022/3/17 14:56
# @Author  : wyw

import pickle

def get_file_context(file):
    with open(file, mode='r', encoding='utf-8', newline='\n') as f:
        lines = f.readlines()
    if lines:
        with open(file + '.pkl', mode='wb') as f:
            pickle.dump(lines, f)
    return lines