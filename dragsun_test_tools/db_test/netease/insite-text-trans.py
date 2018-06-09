# 见外文档翻译统计

from  db_tools.mysql import  MysqlClient
from  db_tools.mysql import  MysqlStatusCheck
import codecs
from commons import utils


'''
计算翻译信息
'''
def calTransSourceInfo(appKey , startTime , endTime):
    global sourceByteCount;
    global transByteCount;
    global sentenceCount;

    limitCount = 100 ;
    idSqlClause = ' 1=1 ';
    id = None
    hasNextPage = True;
    while hasNextPage :
        fd = codecs.open('insite-text-trans-cal.sql')
        sql = fd.read();
        sql = sql.replace('\n', '  ');
        sql = sql.replace('${appKey}', appKey)
        sql = sql.replace('${idSqlClause}', idSqlClause)
        sql = sql.replace('${startTime}', startTime)
        sql = sql.replace('${endTime}', endTime)
        limit = limitCount + 1;
        sql = sql.replace('${limitCount}', str(limit))
        res = MysqlClient.queryBySql(sql);
        if res and len(res) > 0:
            print('limit : ' , limit)
            if len(res) == limit :
                hasNextPage = True
                lastOne = res[len(res) - 2];
                id = lastOne['id'];
                print('id : ' , id)
                idSqlClause += ' AND t_aeli.id < ' + str(id);
            else:
                hasNextPage = False;

            rangeLimit = limitCount;
            if not hasNextPage :
                rangeLimit = len(res);

            for i in range(0 , rangeLimit):
                sentenceCount = sentenceCount + 1;
                item = res[i];
                source_content = None;
                trans_content = None;
                if utils.containsKey(item , 'source_content' ) :
                    source_content = item['source_content'];
                if utils.containsKey(item , 'trans_content' ) :
                    trans_content = item['trans_content'];


                if source_content :
                    itemSourceByteCount = len(source_content);
                    sourceByteCount = sourceByteCount + itemSourceByteCount;
                if trans_content :
                    itemTransByteCount = len(trans_content);
                    transByteCount = transByteCount + itemTransByteCount;

    return None

'''
获取英文单词数量
'''
def getEnWordCount(enText):
    return 0

'''
获取中文字数
'''
def getZhCount(zhText):
    return 0;



appKey = 'btY2e66W';
startTime = '2018-05-01 00:00:00';
endTime = '2018-12-15 23:59:59';
# 原文字节数
sourceByteCount = 0;
# 译文字节数
transByteCount = 0;
# 句子数
sentenceCount = 0;

calTransSourceInfo(appKey , startTime , endTime)


print('appKey : ' , appKey)
print('起始时间 : ' , startTime)
print('结束时间 : ' , endTime)
print('句子数 : ' , sentenceCount)
# sourceByteCount = sourceByteCount / 1024
# transByteCount = transByteCount / 1024
# 1027662 + 455
print('原文字节数 : ' , sourceByteCount)
print('译文字节数 : ' , transByteCount)
print()

