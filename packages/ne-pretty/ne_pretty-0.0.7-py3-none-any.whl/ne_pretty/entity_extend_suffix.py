# @Time    : 2022/2/25 19:38
# @Author  : tk
# @FileName: entity_extend_suffix.py
import json
import copy
from ne_pretty.utils import get_file_context
# 实体后面扩充
def e_extend_suffix(filename, outfile,label_name,suffix):
    lines = get_file_context(filename)

    # label_name = '作案手段'
    # #待增加内容
    # suffix='逃离了现场'
    suffix_len = len(suffix)
    f_out =  open(outfile,mode='w',encoding='utf-8',newline='\n')
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

        text_Len = len(text)
        flag = False

        if label_name in entities_new:
            o = entities_new.pop(label_name)
            o_new = {}
            for sub_text in o:
                pt_list = o[sub_text]
                pt_list = sorted(pt_list)

                for pt in pt_list:
                    if pt[1] + suffix_len < text_Len and text[pt[1] + 1:pt[1] + suffix_len + 1] == suffix:
                        flag = True
                        pt_d = pt[1]+suffix_len
                        sub_text_new = text[pt[0]: pt_d + 1]
                        if sub_text_new not in o_new:
                            o_new[sub_text_new] = [[pt[0],pt_d]]
                        else:
                            o_new[sub_text_new].append([pt[0],pt_d])
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

