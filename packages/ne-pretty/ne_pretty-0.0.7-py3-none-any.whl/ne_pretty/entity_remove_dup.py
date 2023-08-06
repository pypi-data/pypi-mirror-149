# -*- coding: utf-8 -*-
# @Time    : 2022/2/24 12:27
# @Author  : wyw


# -*- coding: utf-8 -*-
# @Time    : 2022/2/21 14:51
# @Author  : wyw
# 除去重复标签
import json
import copy
from ne_pretty.utils import get_file_context

def is_dup(filename):
    with open(filename,mode='r',encoding='utf-8',newline='\n') as f:
        lines = f.readlines()

    id = 0
    for i,line in enumerate(lines):
        jd = json.loads(line)
        text = jd["text"]
        entities = jd['entities']

        flag = False
        for label_key in entities:
            o = entities[label_key]
            for sub_text in o:
                pt_list = o[sub_text]
                pt_list = sorted(pt_list)
                pt_list_tmp = list(set(map(lambda x: (x[0], x[1]), pt_list)))
                pt_list_new = list(map(lambda x: [x[0], x[1]], pt_list_tmp))
                pt_list_new = sorted(pt_list_new)

                if pt_list  != pt_list_new:
                    flag = True

        if flag:
            print(i+1,entities)
            print()

def e_remove_dup(filename,outfile):
    lines = get_file_context(filename)

    f_out = open(outfile,mode='w',encoding='utf-8')

    for i,line in enumerate(lines):
        try:
            jd = json.loads(line)
            text = jd["text"]
            entities = jd.get('entities', {})
        except Exception as e:
            text = line
            entities = {}
        #entities_new = copy.deepcopy(entities)

        for label_key in entities:
            o = entities[label_key]
            for sub_text in o:
                pt_list = o[sub_text]
                pt_list = list(set(map(lambda x: (x[0], x[1]), pt_list)))
                o[sub_text] = list(map(lambda x: [x[0], x[1]], pt_list))

        out = {
            'id': i+1,
            'text': text,
            'entities': entities
        }

        f_out.write(json.dumps(out,ensure_ascii=False) + '\n')
    f_out.close()
