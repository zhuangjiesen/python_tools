# 见外文档翻译统计

from  db_tools.mysql import  MysqlClient
from  db_tools.mysql import  MysqlStatusCheck
import codecs
from commons import utils
import json

'''
计算翻译信息
'''
fd = codecs.open('trans_text.txt')
text = fd.read();

jsonDict = {};
jsonDict['content'] = text;
jsonDict['lang'] = 'zh'

json_str = json.dumps(jsonDict,ensure_ascii=False,indent=2)
print ("JSON 对象：", json_str)


