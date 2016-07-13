#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @auther:wangxiang
# data；2016-07-11
from xml.etree import ElementTree as ET
import sys,re

acc = {}
child_dict = {}
ret_dict = {}
xml_name = sys.argv[1]
tree = ET.parse(xml_name)

# 获取xml文件的根节点
root = tree.getroot()

for i in root.iter():
    rets = i.tag
    # print i.getchildren
    for x in i.getchildren():
        if len(i.getchildren()) != 0:
            if rets in ret_dict.keys() and x.tag not in ret_dict[rets]:
                ret_dict[rets] += ',{}'.format(x.tag)
            else:
                ret_dict[rets] = x.tag

for l in root.iter():
    if l.tag in acc.keys() and sorted(l.items()) != sorted(acc[l.tag]):
         for val  in l.items():
            acc[l.tag].append(val)
    else:
        acc[l.tag] = l.items()
for k,v in acc.items():     # 把标签内容转出dict(同时去除重复key)
    child_dict[k] = dict(v)
child_dict.pop('root'),ret_dict.pop('root')


def create_file(filename,dic,lis):
    '''
    # 根据节点名生成对应as文件
    :param filename:    上下文
    :param dic:         标签名
    :return:
    '''
    ret = {}
    text = filename.split('\n')  # 字符格式化li
    text[0] = 'package client.config_data.{}.data'.format(xml_name.split('.')[0])
    text[2] = 'public class {}VO'.format(dic.capitalize())
    for v in child_dict[dic].items():  # 判断标签属性数据类型
        result = re.findall(r'^[+-]?\d+\d*$', v[1])
        if len(result) > 0:
            var_type = 'int'
            ret[v[0]] = var_type
        else:
            var_type = 'string'
            ret[v[0]] = var_type
    for keys, values in zip(ret.keys(), range(4, 4 + len(ret))):
        text.insert(4, '\tpublic var {}:{};'.format(keys, ret[keys]))  # list插入标签及其数据类型
    for r,t in lis.items():
        for s in t.split(','):
            if r == dic:
                text.insert(-2, '\tpublic var {}:{}VO;'.format(s,dic.capitalize()))
    with open('{}VO.as'.format(dic.capitalize()), 'w') as f:  # 编辑好的list重新写入文件
        for s,i in enumerate(text):
            if s == 0:
                f.write(i)
            else:
                f.write('\n%s'%i)

if __name__ == '__main__':
    temp_Text = '''package client.config_data.shaw.data
{
  public class TextVO
  {
  }
}'''
    for k in child_dict.keys():
            create_file(temp_Text, k,ret_dict)  # 生成文件