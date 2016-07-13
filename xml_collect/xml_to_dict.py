# -*- coding:utf-8 -*-
'''
预处理xml文件（导出json格式）
'''
from xml.etree import ElementTree as ET
import sys, re


class Export_dict:
    def __init__(self, xml_name, xml_dict, xml_child_dict):
        self.xml_name = xml_name
        self.xml_dict = xml_dict  # 标签属内容dict
        self.xml_child_dict = xml_child_dict  # 子标签dict

    def xml_analysis_root(self):
        '''
        # 获取xml根节点
        :return:None
        '''
        tree = ET.parse(self.xml_name)
        root = tree.getroot()
        return root

    def xml_tag_dict(self):
        '''
         # 获取标签子标签dict
        :return:节点:子节点dict
        '''
        result = self.xml_analysis_root()
        for s in result.iter():
            for i in s.getchildren():
                if len(s.getchildren()) != 0:
                    if s.tag in self.xml_child_dict and i.tag not in self.xml_child_dict[s.tag]:
                        self.xml_child_dict[s.tag].append(i.tag)
                    else:
                        self.xml_child_dict[s.tag] = i.tag.split()
        self.xml_child_dict.pop(result.tag)


    def xml_text_dict(self):
        '''
        # 获取标签:标签内容dict
        :return: 获取标签:标签内容dict
        '''
        xml_transit_dict = {}
        result = self.xml_analysis_root()
        for i in result.iter():
            if i.tag in xml_transit_dict.keys() and sorted(i.items()) != sorted(xml_transit_dict[i.tag]):
                for attrib in i.items():
                    xml_transit_dict[i.tag].append(attrib)
            else:
                xml_transit_dict[i.tag] = i.items()
        for k, v in xml_transit_dict.items():
            self.xml_dict[k] = dict(v)
        self.xml_dict.pop(result.tag)
        # return self.xml_dict


    def xml_dict_merge(self):
        merge_v = []
        for k in self.xml_child_dict.keys():
            if self.xml_dict.has_key(k):
                merge_v.append(self.xml_dict[k])
                merge_v.append(self.xml_child_dict[k])
                self.xml_dict[k] = merge_v
        return self.xml_dict



if __name__ == '__main__':
    ret = {}
    val = {}
    xml_export_dict = Export_dict('video.xml', ret, val)
    xml_export_dict.xml_text_dict()
    xml_export_dict.xml_tag_dict()
    r = xml_export_dict.xml_dict_merge()
    for k,v in r.items():
        print k,v


