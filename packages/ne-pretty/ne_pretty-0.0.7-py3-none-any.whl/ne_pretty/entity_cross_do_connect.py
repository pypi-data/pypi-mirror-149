# @Time    : 2022/3/5 20:34
# @Author  : tk

import copy
import json
from ne_pretty.utils import get_file_context

#同标签交叉实体连接完整实体

def has_cross(pts):
    tmp_pts = sorted(pts, key=lambda x: (x[0],x[1]), reverse=False)
    length = len(tmp_pts)
    i = 0
    while i < length - 1:
        s_pt = tmp_pts[i]
        for j in range(i + 1, length):
            d_pt = tmp_pts[j]
            if s_pt[0]  <= d_pt[0] and s_pt[1] >=  d_pt[0] :
                return True
        i = i+1
    return False

def get_connect_cross_pts(pts):
    tmp_pts = sorted(pts, key=lambda x: (x[0],x[1]), reverse=False)

    pts_new = []
    i = 0

    while i <= len(tmp_pts)-1:
        s_pt = tmp_pts[i]
        flag = False
        for j in range(i+ 1,len(tmp_pts)):
            d_pt = tmp_pts[j]
            if s_pt[0]  <= d_pt[0] and s_pt[1] >=  d_pt[0] :
                flag = True

                new_pt = [s_pt[0],max(s_pt[1],d_pt[1])]
                pts_new.append(new_pt)
                tmp_pts[i] = new_pt
                tmp_pts.__delitem__(j)
                break

        if not flag:
            new_pt = [s_pt[0], s_pt[1]]
            if new_pt not in pts_new:
                pts_new.append(new_pt)
            i = i + 1
    return pts_new

def do_get_cross_connect_pts(pts):
    pts_tmp = pts
    while 1:
        if has_cross(pts_tmp):
            pts_tmp = get_connect_cross_pts(pts_tmp)
        else:
            break
    return pts_tmp



def e_cross_do_connect(filename,outfile,label_name):
    lines = get_file_context(filename)


    all_count = 0
    id = 0
    f_out = open(outfile,mode='w',encoding='utf-8')
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

        # 连接交叉实体
        for label_key in entities_new:
            if label_key != label_name:
                continue
            o = entities_new[label_key]
            pts = []
            for sub_text in o:
                pt_list = o[sub_text]
                pts.extend(pt_list)


            pts = do_get_cross_connect_pts(pts)


            o_new = {}
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
                entities_new[label_key] = o_new

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

        all_count += 1
        if flag:
            id += 1
            print(i + 1, id)
            print(entities.get(label_name, {}))
            print(entities_new.get(label_name, {}))
            print()

        out = {
            'id':  i+1,
            'text': text,
            'entities': entities_new
        }

        f_out.write(json.dumps(out,ensure_ascii=False) + '\n')
    f_out.close()
    print('all_count', all_count)

