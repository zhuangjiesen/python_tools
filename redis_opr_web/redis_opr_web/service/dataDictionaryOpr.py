from ..core.mysql import MysqlClient

# 工具类
from ..core import utils
from ..core.Common import AjaxResponse
# 普通方法返回值
from ..core.Common import CommonMethodResult
import datetime



def saveDataDictionary(dictionary):
    commonRes = CommonMethodResult();
    # print()
    dictionary['create_time'] = datetime.datetime.now();
    if MysqlClient.insert('data_dictionary', dictionary) :
        return True
    else:
        return None


def getDataDictionaryByKey(key ):
    dataDictionary = MysqlClient.query('data_dictionary', None, {'key' : key}, None, None);
    if dataDictionary and len(dataDictionary) == 1 :
        return dataDictionary[0];
    return None;


def getDataDictionaryListByValue():
    print()


def getDataDictionaryList():
    dataDictionary = MysqlClient.query('data_dictionary', None, None, None, None);
    return dataDictionary;



def getDataDictionaryKeywordList():
    dataDictionary = MysqlClient.query('data_dictionary', None, {'type' : 9 }, None, None);
    return dataDictionary;

def getDataDictionaryRedisConfList():
    dataDictionary = MysqlClient.query('data_dictionary', None, {'type' : 8 }, None, None);
    return dataDictionary;


def getDataDictionaryById(id):
    dataDictionary = MysqlClient.query('data_dictionary', None, {'i_id' : id }, None, None);
    if dataDictionary and len(dataDictionary) > 0 :
        return dataDictionary[0];
    return None;

def deteleDataDictionaryById(id):
    MysqlClient.executeSql(' delete from data_dictionary where i_id = %s ', [ id ]);

