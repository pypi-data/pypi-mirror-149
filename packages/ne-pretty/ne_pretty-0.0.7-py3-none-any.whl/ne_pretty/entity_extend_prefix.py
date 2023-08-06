# @Time    : 2022/2/25 19:38
# @Author  : tk
# @FileName: entity_extend_prefix.py

import json
import copy
from ne_pretty.utils import get_file_context
# 实体前面扩充
def e_extend_prefix(filename,outfile,label_name,prefix):
    lines = get_file_context(filename)
            

    prefix_len = len(prefix)

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

        flag = False
        if label_name in entities_new:
            o = entities_new.pop(label_name)
            o_new = {}
            for sub_text in o:
                pt_list = o[sub_text]
                pt_list = sorted(pt_list)
                for pt in pt_list:
                    if pt[0] >= prefix_len and text[pt[0]-prefix_len:pt[0]] == prefix:
                        flag = True
                        pt_s = pt[0]-prefix_len
                        sub_text_new = text[pt_s:pt[1] +1]
                        if sub_text_new not in o_new:
                            o_new[sub_text_new] = [[pt_s,pt[1]]]
                        else:
                            o_new[sub_text_new].append([pt_s,pt[1]])
                    else:
                        if sub_text not in o_new:
                            o_new[sub_text] = [[pt[0], pt[1]]]
                        else:
                            o_new[sub_text].append([pt[0], pt[1]])
            entities_new[label_name] = o_new
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

