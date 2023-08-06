# -*- coding: utf-8 -*-
# @Time    : 2022/5/9 9:46
# @Author  : tk


def has_connected(pts):
    tmp_pts = sorted(pts, key=lambda x: (x[0],x[1]), reverse=False)
    length = len(tmp_pts)
    i = 0
    while i < length - 1:
        s_pt = tmp_pts[i]
        for j in range(i+1, length):
            d_pt = tmp_pts[j]
            if s_pt[1] + 1 == d_pt[0]:
                return True
        i = i+1
    return False

def get_connect_pts(pts):
    tmp_pts = sorted(pts, key=lambda x: (x[0],x[1]), reverse=False)
    print('sorted',tmp_pts)
    pts_new = []
    i = 0
    while i <= len(tmp_pts)-1:
        s_pt = tmp_pts[i]
        flag = False
        for j in range(i+1,len(tmp_pts)):
            d_pt = tmp_pts[j]
            if s_pt[1] + 1 == d_pt[0]:
                flag = True
                new_pt = [s_pt[0],d_pt[1]]
                tmp_pts[i] = new_pt
                tmp_pts.__delitem__(j)
                break
        if not flag:
            pts_new.append([s_pt[0], s_pt[1]])
            i = i + 1
    return pts_new


pts = [
	[0,9],[10,20],[20,50],[0,5]
]

print('inital...')
print(pts)
print()


while has_connected(pts):
    pts = get_connect_pts(pts)
    print(pts)

print('final....')
print(pts)

