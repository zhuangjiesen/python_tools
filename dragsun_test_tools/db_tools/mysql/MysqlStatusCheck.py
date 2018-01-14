'''
mysql 数据库状态监测

'''
from  db_tools.mysql import  MysqlClient
from commons import utils
from db_tools.mysql import MysqlConf as Config;

# 查看数据库配置

# 查看锁等待






# 慢查询日志
def getSlowLogOfSql(tableName):
    dbName = Config.DB_TEST_DBNAME;
    sql = '';
    sql += " select * from mysql.slow_log "
    sql += " where 1=1  "
    sql += " and db = '%(dbName)s' "
    sql += "and sql_text like '%(tableName)s' "
    sql = sql % {'tableName' : tableName , 'dbName' : dbName}
    print('sql : ' , sql )
    res = MysqlClient.queryBySql(sql);
    return res;




# 执行计划
def getExplainOfSql(sql):
    explainSql = ' EXPLAIN ' + sql ;
    res = MysqlClient.queryBySql(explainSql);
    return res;


# 索引状态


# 索引选择性
'''
算总记录数
算字段group by 分组数量情况

计算区分度 
字段区分度越低（字段值相同的越多），索引的用处越小

'''
def getIndexSelectable(tableName):
    staticsResult = {};
    totalSql = '  select count(1) as total from ' + tableName;
    res = MysqlClient.queryBySql(totalSql );
    total = 0;
    if res :
        total = res[0]['total'];
    # print(' total : ' , total)
    staticsResult['total'] = total;
    staticsResult['cols'] = [];

    # 数据库行数
    if total > 0 :
        tableColumns = MysqlClient.showTableIndexInfo(tableName);
        # print(' 3.query res : ', tableColumns);
        if tableColumns:
            for colItem in tableColumns:
                fieldName = colItem['Column_name'];

                fieldObj = {};
                fieldObj['fieldName'] = fieldName;
                fieldObj['Key_name'] = colItem['Key_name'];
                fieldObj['Cardinality'] = colItem['Cardinality'];
                fieldObj['Index_type'] = colItem['Index_type'];
                if utils.containsKey(colItem, 'Non_unique') and colItem['Non_unique'] == 1:
                    fieldObj['is_unique'] = True;
                else:
                    fieldObj['is_unique'] = False;

                # 排除主键
                if  utils.containsKey(colItem , 'Key_name' ) and not colItem['Key_name'] == 'PRIMARY' :
                    sql = " SELECT COUNT(1) AS total ,  %(fieldName)s  FROM %(tableName)s GROUP BY  %(fieldName)s  HAVING COUNT( %(fieldName)s ) > 1 " % {'fieldName': fieldName, 'tableName': tableName}
                    countSql = 'select count(1) as total from ( ' + sql + ' ) as a';
                    res = MysqlClient.queryBySql(countSql);
                    if res :
                        res = res[0];
                        desc = '字段 %s 的值重复的数量大于 1 的总数 : %s ' % (fieldName ,  str(res['total']))
                        print(desc)
                        # 字段区分度 大于 2000
                        fieldObj['distinctCount'] = res['total'];
                        if res['total'] > 2000 :
                            print()
                        else:
                            print()
                            res = MysqlClient.queryBySql(sql);
                            rows = [];
                            for item in res :
                                rowItem = {};
                                rowItem['fieldValue'] = item[fieldName];
                                rowItem['total'] = str( item['total'] );
                                rows.append(rowItem);
                            fieldObj['distinctRows'] = rows;
                else:
                    fieldObj['is_unique'] = True;
                staticsResult['cols'].append(fieldObj);
    return staticsResult;



# 统计字段区分度 ， 时间字段除外
def getColumnsSelectable(tableName):
    staticsResult = {};
    totalSql = '  select count(1) as total from ' + tableName;
    res = MysqlClient.queryBySql(totalSql );
    total = 0;
    if res :
        total = res[0]['total'];
    # print(' total : ' , total)
    staticsResult['total'] = total;
    staticsResult['cols'] = [];

    # 数据库行数
    if total > 0 :
        tableColumns = MysqlClient.showTableColumns(tableName);
        # print(' 3.query res : ', tableColumns);
        if tableColumns:
            for colItem in tableColumns:
                print(' col : ' , colItem)
                fieldName = colItem['Field'];

                fieldObj = {};
                fieldObj['fieldName'] = fieldName;
                # 时间类型不参与比较
                fieldObj['Type'] = colItem['Type'];
                if  utils.containsKey(colItem , 'Type' ) and colItem['Type'] == 'datetime' :
                    continue
                if  utils.containsKey(colItem , 'Key' ) and colItem['Key'] == 'PRI' :
                    fieldObj['isPRI'] = 1;
                else:
                    fieldObj['isPRI'] = 0;
                    sql = " SELECT COUNT(1) AS total ,  %(fieldName)s  FROM %(tableName)s GROUP BY  %(fieldName)s  HAVING COUNT( %(fieldName)s ) > 1 " % {
                        'fieldName': fieldName, 'tableName': tableName}
                    countSql = 'select count(1) as total from ( ' + sql + ' ) as a';
                    res = MysqlClient.queryBySql(countSql);
                    if res:
                        res = res[0];
                        desc = '字段 %s 的值重复的数量大于 1 的总数 : %s ' % (fieldName, str(res['total']))
                        print(desc)
                        # 字段区分度 大于 2000
                        fieldObj['distinctCount'] = res['total'];
                        if res['total'] > 2000:
                            print()
                        else:
                            print()
                            res = MysqlClient.queryBySql(sql);
                            rows = [];
                            for item in res:
                                rowItem = {};
                                rowItem['fieldValue'] = item[fieldName];
                                rowItem['total'] = str(item['total']);
                                rows.append(rowItem);
                            fieldObj['distinctRows'] = rows;
                    staticsResult['cols'].append(fieldObj);
    return staticsResult;




# 获取表 数据大小 索引大小
def getDataLength(tableName):
    dbName = Config.DB_TEST_DBNAME;
    sql = '';
    sql += " select "
    sql += " concat(round(sum(data_length / 1024 / 1024), 2), 'MB') as data_length_MB, "
    sql += " concat(round(sum(index_length / 1024 / 1024), 2), 'MB') as index_length_MB "
    sql += " from information_schema.tables  where "
    sql += "  table_schema = '%(dbName)s' "
    sql += " and table_name = '%(tableName)s'; "
    sql = sql % {'tableName' : tableName , 'dbName' : dbName}
    # print('sql : ' , sql )
    res = MysqlClient.queryBySql(sql);
    return res;






# 慢查询日志

'''


show status

show PROCESSLIST

show status like '%Slow_queries%'

show global status like 'table_locks%';  


show global status like 'innodb%';  



show status like 'innodb_row_lock%';  


show status like 'innodb_row%';  


show status like '%Last_query_%';  


show VARIABLES like '%slow%';  


set GLOBAL slow_query_log = 'ON'

  
-- 进程使用情况
show global status like 'Thread%'; 

-- 表扫描情况
 show global status like 'handler_read%'; 


-- sql通过hash算法匹配， 有时候开query cache 反而查询效率更慢
show variables like 'query_cache%'; 

set GLOBAL query_cache_size = 4096

set GLOBAL query_cache_type = 1


 show global status like 'qcache%'; 

#获取表所有列
SELECT * from information_schema.`COLUMNS` where TABLE_SCHEMA = 'dragsun_db' and TABLE_NAME = 'm_user'



select 
from 



SELECT * from information_schema.`statistics`  where TABLE_SCHEMA = 'dragsun_db' and TABLE_NAME = 'm_user'



 SELECT THREAD_ID, NUMBER_OF_BYTES
       FROM events_waits_history



       WHERE EVENT_NAME LIKE 'wait/io/file/%'
       AND NUMBER_OF_BYTES IS NOT NULL;


where TABLE_SCHEMA = 'dragsun_db' and TABLE_NAME = 'm_user'

 

SHOW INDEX from m_user

SHOW COLUMNS from m_user





 show status like '%lock%'



show status like '%Innodb_%'




show index from m_user;

show keys from m_user;



# 查看数据库数据大小，索引大小
select concat(round(sum(data_length/1024/1024),2),'MB') as data_length_MB,  
			concat(round(sum(index_length/1024/1024),2),'MB') as index_length_MB  
			from information_schema.tables  where  
			table_schema='dragsun_db'  
			and table_name = 'm_user';  














show VARIABLES like '%log_output%'
# 慢查询记录到表中
 set global log_output='TABLE';


# 没用索引的sql会被记录到慢查询
set global log_queries_not_using_indexes=1;

# 查看慢查询时间设置 秒
show VARIABLES like '%long_query_time%'



 
show global status like '%Slow_queries%';

# 查看慢查询
show variables like 'slow_query%';


# 开启慢查询
set global slow_query_log=1;


# 慢查询表查询
select * from mysql.slow_log
where 1=1 
and db = 'dragsun_db'
and sql_text like '%%'


'''




