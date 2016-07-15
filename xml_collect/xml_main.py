# -*- coding:utf-8 -*-
# @auther:wangxiang
# date:2016/07/11

'''
由xml产生各种格式文件
'''
import os, time, re
import sys
from  xml_to_dict import Export_dict


class File_handle(Export_dict):

    def __init__(self):
        pass


    def xml_to_as(self):
        '''
        # 产生as文件
        :return:
        '''
        val = Export_dict(self.xml_name)
        val = val.xml_dict_merge()
        for k, v in val.items():
            as_text_list = ['package client.config_data.{}.data'.format(re.split('\W',self.xml_name)[-2]), '{', '\tpublic class TextVO', '\t{', '\t}', '}']
            for i in v:
                if isinstance(i, list):
                    for s in i:
                        # ===== 定义子标签格式begin =====
                        # as_text_list.insert(-2, '\t\tpublic var {}:{}VO;'.format(s, k.capitalize()))  # 子标签一行一行写入
                        if len(i) > 1 and i.index(s) == 0:  # 子标签写成一行
                            as_text_list.insert(-2, '\t\tpublic var {}:{}VO;'.format(s, k.capitalize()))
                        elif len(i) > 1:
                            rets = '{},{}:{}'.format(as_text_list[-3].split(':')[0], s, as_text_list[-3].split(':')[1])
                            as_text_list[-3] = rets
                else:
                    for key, value in i.items():
                        result = re.findall(r'^[+-]?\d+\d*$', value)
                        if len(result) > 0:
                            var_type = 'int'
                        else:
                            var_type = 'string'
                        as_text_list.insert(-2, '\t\tpublic var {}:{};'.format(key, var_type))

            # ===== 根据标签名产生文件 =====
            with open('{}VO.as'.format(k.capitalize()), 'w+') as f:
                for s, i in enumerate(as_text_list):
                    if s == 0:
                        f.write(i)
                    elif s == 2:
                        f.write('\n%s' % i.replace('Text', k.capitalize()))
                    else:
                        f.write('\n%s' % i)


if __name__ == '__main__':
    try:
        ret = File_handle()
        ret.xml_name = sys.argv[1]
        ret.xml_to_as()
    except IndexError as e:
        print(u'缺少xml文件，程序已退出'.encode('utf-8'))
