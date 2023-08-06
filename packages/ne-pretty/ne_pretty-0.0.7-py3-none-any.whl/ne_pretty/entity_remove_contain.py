# @Time    : 2022/2/25 20:13
# @Author  : tk
# @FileName: remove_contain.py


import copy
import json
from ne_pretty.utils import get_file_context
import numpy as np


def get_array_dup_pt(pts):
    pts = sorted(pts,key=lambda x: x[1] -x[0],reverse=False)
    arrs = []
    for i in range(len(pts) - 1):
        s = pts[i]
        for j in range(i + 1, len(pts)):
            d = pts[j]
            if s[0] >= d[0] and s[1] <= d[1]:
                arrs.append(i)
                break
    if arrs:
        pts = np.delete(pts,arrs,axis=0).tolist()
    return pts


def e_remove_contain(filename,outfile,label_name):
    assert label_name is not None

    lines = get_file_context(filename)


    f_out = open(outfile,mode='w',encoding='utf-8')

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


        flag = False
        #去重
        for label_key in entities_new:
            o = entities_new[label_key]
            for sub_text in o:
                pt_list = o[sub_text]
                pt_list = list(set(map(lambda x: (x[0], x[1]), pt_list)))
                o[sub_text] = list(map(lambda x: [x[0], x[1]], pt_list))

        # 去除包含
        if label_name in entities_new:
            o = entities_new[label_name]

            o_new = {}

            pts = []
            for sub_text in o:
                pt_list = o[sub_text]
                pts.extend(pt_list)

            pts = get_array_dup_pt(pts)

            for pt in pts:
                sub_text = text[pt[0]:pt[1] + 1]
                if sub_text not in o_new:
                    o_new[sub_text]=[]
                o_new[sub_text].append(pt)

            o = dict(sorted(o.items(), key=lambda x: x[0]))
            o_new = dict(sorted(o_new.items(), key=lambda x: x[0]))

            for sub_text in o:
                o[sub_text] = sorted(o[sub_text])

            for sub_text in o_new:
                o_new[sub_text] = sorted(o_new[sub_text])

            if o != o_new:
                flag = True
                entities_new[label_name] = o_new

        entities = dict(sorted(entities.items(), key=lambda x: x[0]))
        entities_new = dict(sorted(entities_new.items(), key=lambda x: x[0]))
        # 排序
        for label_key in entities:
            o = entities[label_key]
            for sub_text in o:
                o[sub_text] = sorted(o[sub_text])

        for label_key in entities_new:
            o = entities_new[label_key]
            for sub_text in o:
                o[sub_text] = sorted(o[sub_text])

        if flag:
            id += 1
            print(i + 1, id)
            print(entities.get(label_name, {}))
            print(entities_new.get(label_name, {}))
            print()

        out = {
            'id': i+ 1,
            'text': text,
            'entities': entities_new
        }

        f_out.write(json.dumps(out,ensure_ascii=False) + '\n')
    f_out.close()



