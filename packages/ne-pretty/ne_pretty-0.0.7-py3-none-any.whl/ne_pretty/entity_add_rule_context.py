# -*- coding: utf-8 -*-
# @Time    : 2022/3/16 10:18
# @Author  : wyw

import re
import json
import copy
from ne_pretty.utils import get_file_context

def rule_finder(text_,pattern ):
    pat = re.compile(pattern, re.I)
    pos = {}
    s_pos = 0
    while True:
        ret = pat.search(text_, s_pos)
        if ret is None:
            break
        s = ret.span()
        text = text_[s[0]:s[1]]
        if text not in pos:
            pos[text] = [[s[0], s[1] - 1]]
        else:
            pos[text].append([s[0], s[1] - 1])
        s_pos = s[1]
    return pos



#添加指定内容实体
def e_add_rule_context(filename, outfile,label_name,rule_text):
    lines = get_file_context(filename)


    f_out = open(outfile,mode='w',encoding='utf-8',newline='\n')
    id = 0
    for i,line in enumerate(lines):
        try:
            jd = json.loads(line)
            text = jd["text"]
            entities = jd.get('entities', {})
        except Exception as e:
            text = line
            entities = {}
        entities_new = copy.deepcopy(entities)

        rules = rule_finder(text,rule_text)

        flag = False
        if len(rules) > 0:
            if label_name not in entities_new:
                entities_new[label_name] = {}
            objects = entities_new[label_name]

            for sub_text in rules:
                pt_list_add = rules[sub_text]
                if sub_text not in objects:
                    objects[sub_text] = []
                o = objects[sub_text]
                for one_pt in pt_list_add:
                    if one_pt not in o:
                        o.append(one_pt)
                        flag = True


        entities = dict(sorted(entities.items(), key=lambda x: x[0]))
        entities_new = dict(sorted(entities_new.items(),key=lambda x:x[0]))
        #排序
        for label_key in entities:
            o = entities[label_key]
            for sub_text in o:
                o[sub_text] = sorted(o[sub_text])

        for label_key in entities_new:
            o = entities_new[label_key]
            for sub_text in o:
                o[sub_text] = sorted(o[sub_text])


        out = {
            'id' : i+1,
            "text":text,
            "entities": entities_new
        }
        f_out.write(
            json.dumps(out,ensure_ascii=False) + '\n'
        )

        if flag:
            id += 1
            print(i + 1, id)
            print(entities.get(label_name, {}))
            print(entities_new.get(label_name, {}))
            print()
    f_out.close()


