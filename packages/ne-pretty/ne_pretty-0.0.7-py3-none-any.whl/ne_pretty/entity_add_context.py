# @Time    : 2022/2/25 19:38
# @Author  : tk
# @FileName: entity_add_context.py

import json
import copy
from ne_pretty.utils import get_file_context


#添加指定内容实体
def e_add_context(filename, outfile,label_name,context):
    lines = get_file_context(filename)

    context_len = len(context)
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


        start_pos = 0
        add_pt =[]
        while True:
            start_pos_new = text.find(context,start_pos)
            if start_pos_new == -1:
                break
            add_pt.append([start_pos_new,start_pos_new + context_len -1])
            start_pos = start_pos_new + context_len

        flag = False
        if add_pt:
            flag = True
            if label_name not in entities_new:
                entities_new[label_name] = {}
            o = entities_new.get(label_name)
            if context in o:
                for pt in add_pt:
                    if pt not in o[context]:
                        o[context].append(pt)
            else:
                o[context] = add_pt

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

