# -*- coding:utf-8 -*-
'''
预处理xml文件（导出json格式）
'''
from xml.etree import ElementTree as ET
import sys, re


class Export_dict:
    def __init__(self, xml_name,xml_dict,xml_child_dict):
        self.xml_name = xml_name
        self.xml_dict = xml_dict    # 标签属内容dict
        self.xml_child_dict = xml_child_dict    # 子标签dict

    def xml_list(self):
        tree = ET.parse(self.xml_name)
        root = tree.getroot()
        for s in root.iter():
            for i in s.getchildren():
                if len(s.getchildren()) != 0:
                    if s.tag in self.xml_child_dict and i.tag not in self.xml_child_dict[s.tag]:
        #如果已存在子标签
                        self.xml_child_dict[s.tag] += ',{}'.format(i.tag)
                    else:
                        self.xml_child_dict[s.tag] = i.tag.split()




class Export_json(Export_dict):
    def List_json(self):
        pass



if __name__ == '__main__':
    xml_export_dict = Export_dict('video.xml')
    xml_export_dict.xml_list()