# -*- coding:utf-8 -*-
# @auther:wangxiang
# date:2016/07/11

'''
预处理xml文件（导出dict格式）
'''

from xml.etree import ElementTree as ET


class Export_dict:
    def __init__(self, xml_name):
        self.xml_name = xml_name
        self.xml_dict = {}  # 标签属内容dict
        self.xml_child_dict = {}  # 子标签dict
        self.xml_transit_dict = {}  # ret

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
        result = self.xml_analysis_root()
        for i in result.iter():
            if i.tag in self.xml_transit_dict.keys() and sorted(i.items()) != sorted(self.xml_transit_dict[i.tag]):
                for attrib in i.items():
                    self.xml_transit_dict[i.tag].append(attrib)
            else:
                self.xml_transit_dict[i.tag] = i.items()
        for k, v in self.xml_transit_dict.items():
            self.xml_dict[k] = dict(v)
        self.xml_dict.pop(result.tag)



    def xml_dict_merge(self):
        '''
        # dict合并(子标签，内容合并为标签key)
        :return:
        '''
        self.xml_analysis_root(), self.xml_tag_dict(), self.xml_text_dict()
        for k, v in self.xml_dict.items():
            self.xml_transit_dict[k] = [v]
        for i in self.xml_child_dict.keys():
            if i in self.xml_transit_dict.keys():
                self.xml_transit_dict[i].append(self.xml_child_dict[i])
        self.xml_transit_dict.pop(self.xml_analysis_root().tag)
        return self.xml_transit_dict
