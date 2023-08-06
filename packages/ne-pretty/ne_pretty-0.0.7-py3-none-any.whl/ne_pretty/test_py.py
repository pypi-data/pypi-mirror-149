# -*- coding: utf-8 -*-
# @Time    : 2022/3/17 14:39
# @Author  : wyw

#增加实体
from ne_pretty import e_add_context
#正则添加实体
from ne_pretty import e_add_rule_context
#连接相邻实体
from ne_pretty import e_do_connect
#连接交叉实体，保留最大
from ne_pretty import e_cross_do_connect
#扩展前缀
from ne_pretty import e_extend_prefix
#扩展后缀
from ne_pretty import e_extend_suffix
#删除前缀
from ne_pretty import e_remove_prefix
#删除后缀
from ne_pretty import e_remove_suffix

#删除实体包含
from ne_pretty import e_remove_contain
#删除指定实体
from ne_pretty import e_remove_eq
#去重
from ne_pretty import e_remove_dup
#比较不同
from ne_pretty import entity_diff


filename = r'C:\Users\acer\Desktop\demo\text.txt'

e_add_rule_context(filename,filename,'地点','(北京)')

#e_add_context(filename,filename,'地点','北京')


#e_remove_eq(filename,filename,'地点','北京')


#e_remove_suffix(filename,filename,'地点','北京')

#e_remove_prefix(filename,filename,'地点','北京')


#e_remove_contain(filename,filename,'作案手段')

#e_remove_dup(filename,filename)
