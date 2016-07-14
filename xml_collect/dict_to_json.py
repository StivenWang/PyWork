# -*- coding:utf-8 -*-
# @auther:wangxiang
# date:2016/07/11

'''
# dict转json格式，并写入文件
'''

import json
from  xml_to_dict import Export_dict


class Export_json():
    def __init__(self, json_name):
        self.json_name = json_name

    def List_json(self):
        ret = Export_dict('video.xml')   # 文件名待处理
        ret = ret.xml_dict_merge()
        with open(self.json_name, 'w') as f:
            f.write(json.dumps(ret))

