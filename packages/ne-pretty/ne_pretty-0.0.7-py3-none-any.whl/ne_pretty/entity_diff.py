# @Time    : 2022/3/26 0:19
# @Author  : tk
# @FileName: entity_diff.py

import json

def e_diff(filename1,filename2,label_name):
    with open(filename1,mode='r',encoding='utf-8',newline='\n') as f:
        lines1= f.readlines()
    with open(filename2,mode='r',encoding='utf-8',newline='\n') as f:
        lines2 = f.readlines()
    id = 0
    all_lines = []
    for i,(line1,line2) in enumerate(zip(lines1,lines2)):
        jd1 = json.loads(line1)
        jd2 = json.loads(line2)
        if not jd1 or not jd2:
            continue

        #text = jd1["text"]
        entities1 = jd1['entities']
        entities2 = jd2['entities']
        t = label_name
        e1 = entities1.get(t, {})
        e2 = entities2.get(t, {})
        if not e1 and not e2:
            continue
        for k in e1:
            e1[k] = sorted(e1[k])
        for k in e2:
            e2[k] = sorted(e2[k])
        e1 = dict(sorted(e1.items(),key=lambda x:x[1]))
        e2 = dict(sorted(e2.items(),key=lambda x:x[1]))
        if e1 == e2:
            continue
        all_lines.append( i + 1)
        id += 1
        print(i + 1,"    ", id)
        print("true",e1)
        print("pred",e2)
        print()