# @Time    : 2022/2/25 19:38
# @Author  : tk
# @FileName: entity_remove_prefix.py

import json
import copy
from ne_pretty.utils import get_file_context

# 从实体前面删除
def e_remove_prefix(filename, outfile,label_name,remove_suffix):

    assert remove_suffix != ''
    lines = get_file_context(filename)

    prefix=remove_suffix
    prefix_len = len(prefix)

    all_count = 0
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
        if label_name in entities:
            o = entities_new.pop(label_name)
            o_new = {}
            for sub_text in o:
                pt_list = o[sub_text]
                pt_list = sorted(pt_list)
                if not sub_text.startswith(prefix):
                    for pt in pt_list:
                        s = pt[0]
                        e = pt[1]
                        sub_text_new = text[s:e + 1]
                        if sub_text_new not in o_new:
                            o_new[sub_text_new] = [[s, e]]
                        else:
                            new_point = [s, e]
                            if new_point not in o_new[sub_text_new]:
                                o_new[sub_text_new].append([s, e])
                else:
                    flag = True
                    for pt in pt_list:
                        s = pt[0] + prefix_len
                        e = pt[1]
                        if e < s:
                            continue
                        sub_text_new = text[s:e + 1]
                        if sub_text_new not in o_new:
                            o_new[sub_text_new] = [[s, e]]
                        else:
                            new_point = [s, e]
                            if new_point not in o_new[sub_text_new]:
                                o_new[sub_text_new].append([s, e])

            entities_new[label_name] = o_new


        if label_name in entities_new and not entities_new[label_name]:
            entities_new.pop(label_name)

        entities = dict(sorted(entities.items(),key=lambda x:x[0]))
        entities_new = dict(sorted(entities_new.items(), key=lambda x: x[0]))

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
        all_count += 1
        if flag:
            id += 1
            print(i + 1, id)
            print(entities.get(label_name, {}))
            print(entities_new.get(label_name, {}))
            print()

    f_out.close()
    print('all_count',all_count )


