import pymysql
from DBUtils.PooledDB import PooledDB
from db_tools.mysql import MysqlConn
from db_tools.mysql import Mysql_Conf  as Config;
from types import FunctionType
import datetime

'''
@功能：获取PT数据库连接
'''
mysql_connection = MysqlConn.PTConnectionPool();

def getCursor():
    return mysql_connection.getCursor();

'''
获取数据库表的列信息
'''
def getTableCols(tableName):
    sql = " SELECT column_name from information_schema.`COLUMNS` where TABLE_SCHEMA = '"+ Config.DB_TEST_DBNAME +"' and TABLE_NAME = '"+ tableName +"' "
    print(' sql : ' , sql);
    return queryBySql(sql);

'''
检查字典类型数据的字段数据库中是否存在字段
'''
def checkTableCols(tableName , entity):
    if not entity :
        return None;
    col_list = [];
    cols = getTableCols(tableName);
    # print(' checkTableCols tableName : ' , tableName);
    for key in entity :
        is_exist = False;
        for i in range(0 , len(cols) ):
            col_item = cols[i];
            column_name = col_item['column_name']
            # print('column_name : ', column_name)
            if column_name and column_name == key :
                is_exist = True;
                break;
        if not is_exist :
            #不存在这个字段
            col_list.append(key);
    if len(col_list) == 0:
        return None;
    return col_list;



def alter_add_new_col(tableName , colName , length ):
    sql = " alter table " + tableName + " add " + colName + " varchar(" + str(length) + ")" ;
    print(' sql : ' , sql);
    return queryBySql(sql)



def insert(tableName , data ):
    if data :
        sql = " insert into ${tableName} ( ${columnName} ) values ( ${values} )";
        columnNameStr = '';
        valuesStr = '';
        params_list = [];
        for key in data :
            columnNameStr += " `"+ key + "` ";
            columnNameStr += " ,";
            valuesStr += " %s "
            valuesStr += " ,";
            if type(data[key]) == dict :
                params_list.append(str(data[key]))
            else:
                # print('params type : ' , type(data[key]))
                params_list.append(data[key])

        if len(columnNameStr) > 0 :
            columnNameStr = columnNameStr[0 : len(columnNameStr) - 1];
        if len(valuesStr) > 0 :
            valuesStr = valuesStr[0 : len(valuesStr) - 1];

        sql = sql.replace('${tableName}', tableName)
        sql = sql.replace('${columnName}', columnNameStr)
        sql = sql.replace('${values}', valuesStr)
        # print('params_list : ' , tuple(params_list) )
        print('sql : ', sql, '   params : ', params_list);
        conn = mysql_connection.getConn();
        cursor = conn.cursor()
        res = cursor.execute(sql , tuple(params_list)  );
        conn.commit();

        if res > 0 :
            return True
        return None;
    else:
        return None


def update( tableName , id_col_name , id ,  new_data ):
    # 改进应该防注入
    sql = ' update ${tableName} ${set}  where ${idColName} = ${id} ';
    setStr = ' set ';
    params_list = [];
    if new_data :
        for key in new_data :
            setStr += " " + key + " ";
            setStr += " = %s "
            setStr += " ,"
            params_list.append(new_data[key]);

    if len(setStr) > 1 :
        setStr = setStr[0 : len(setStr) - 1];
    else:
        return None;
    sql = sql.replace('${tableName}', tableName)
    sql = sql.replace('${set}', setStr)
    sql = sql.replace('${idColName}', id_col_name)
    sql = sql.replace('${id}', str(id));

    print('sql : ', sql , '   params : ' , params_list);
    conn = mysql_connection.getConn();
    cursor = conn.cursor()
    res = cursor.execute(sql , tuple(params_list));
    conn.commit();
    return True;



def updateByParams(tableName , whereParams , new_data ):
    if not whereParams :
        return None;
    sql = ' update ${tableName} ${set}  ${whereParams} ';
    setStr = ' set ';
    whereParamsStr = ' where 1 = 1 ';
    params_list = [];
    if new_data :
        for key in new_data :
            setStr += " " + key + " ";
            setStr += " = %s "
            setStr += " ,"
            params_list.append(new_data[key]);

    hasWhereParams = False;
    for key in whereParamsStr :
        hasWhereParams = True;
        whereParamsStr += " and " + key + " ";
        whereParamsStr += " = %s "
        params_list.append(whereParamsStr[key]);

    if not hasWhereParams :
        return None;
        setStr = reduceLastChar(setStr);
    else:
        return None;
    sql = sql.replace('${tableName}', tableName)
    sql = sql.replace('${whereParams}', whereParamsStr)
    sql = sql.replace('${set}', setStr)

    print('sql : ', sql , '   params : ' , params_list);
    conn = mysql_connection.getConn();
    cursor = conn.cursor()
    res = cursor.execute(sql , tuple(params_list));
    conn.commit();
    return True;




def queryBySql(sql):
    conn = mysql_connection.getConn();
    cursor = conn.cursor()
    cursor.execute(sql);
    conn.commit();
    return getCursorResult(cursor);


'''
注释
tableName 表名
selectArray 选择字段 None 默认* 
whereParams 字典对象 { 字段 : 值 }
orderBy { 字段 : 排序 }
limit 数组 [ 1 , 2 ]

'''

def query(tableName , selectArray  , whereParams , orderBy , limit   ):
    sql = ' select ${selectArray} from ${tableName} ${whereParams} ${orderBy} ${limit} ';
    selectArrayStr = '';
    tableNameStr = tableName;
    whereParamsStr = ' where 1 = 1';
    orderByStr = '';
    limitStr = '';
    params_list = [];
    # 空 数组空 有* 默认查所有字段
    if not selectArray or len(selectArray) == 0:
        print()
        selectArrayStr = '*'
    else:
        for item in selectArray:
            if item.find('*') > 0:
                selectArrayStr = '*'
                break;
            selectArrayStr += item + ' ';
            selectArrayStr += ' ,'
        if len(selectArrayStr) > 1 :
            selectArrayStr = selectArrayStr[0 : len(selectArrayStr) - 1];

    if whereParams :
        for key in whereParams :
            whereItem = ' and ';
            whereItem += "`"+ key + "` = %s ";
            # print('whereParams[key] : ' , whereParams);
            params_list.append(whereParams[key])
            whereParamsStr = whereParamsStr +  whereItem

    if orderBy :
        orderByStr = ' order by '
        # print(' orderBy ' , orderBy)
        for key in orderBy :
            orderByStr += key + '  ';
            orderByStr += str(orderBy[key]) ;
            break

    if limit :
        if len(limit) == 1 :
            limitStr += ' limit ' + str(limit[0]);
        elif len(limit) == 2:
            limitStr += ' limit ' + str(limit[0]) + ' , ' + str(limit[1]);
    # print('selectArrayStr : ' , selectArrayStr)
    sql = sql.replace('${selectArray}' , selectArrayStr )
    sql = sql.replace('${tableName}', tableNameStr)
    sql = sql.replace('${whereParams}', whereParamsStr)
    sql = sql.replace('${orderBy}', orderByStr)
    sql = sql.replace('${limit}', limitStr)
    print('sql : ', sql , '   params : ' , params_list);
    conn = mysql_connection.getConn();
    cursor = conn.cursor()
    res = cursor.execute(sql , tuple(params_list));
    conn.commit();
    return getCursorResult(cursor);


def executeSql(sql , params_list):
    print('sql : ', sql , '   params : ' , params_list);
    conn = mysql_connection.getConn();
    cursor = conn.cursor()
    res = cursor.execute(sql , tuple(params_list));
    conn.commit();
    return getCursorResult(cursor);



def reduceLastChar(str):
    if str :
        if len(str) > 1:
            str = str[0: len(str) - 1];

        return str;
    else:
        return None


# app_redis = cursor.fetchall()
# print(' app_redis : ' , list(app_redis))
# app_redis = cursor.fetchall()
# print(' app_redis : ' , list(app_redis))
# print(' app_redis : ' , app_redis)
# app_redis_list = list(app_redis);
# print(' app_redis : ' , type(app_redis_list))

# 封装结果集
def getCursorResult(cursor) :
    cursor_data = cursor.fetchall();
    if cursor_data and len(cursor_data) > 0 :
        cursor_data_list = list(cursor_data);
        # 字段描述 获取字段结果集
        desc_list = list(cursor.description)
        col_list = [];
        for i in range(0, len(desc_list)):
            desc_item = desc_list[i];
            # print(' desc_item : ' , list(desc_item))
            col_name = list(desc_item)[0];
            # print(' col_name : ' , col_name)
            col_list.append(col_name);
        # print(col_list)
        # 将结果集封装成 字段 : 查询结果 的样式
        result_list = [];
        for i in range(0, len(cursor_data_list)):
            app_redis_item = cursor_data_list[i];
            # print('item : ' , i ,' app_redis_item : ' , app_redis_item )
            result_item = {};
            app_redis_item_list = list(app_redis_item);
            now = datetime.datetime.now();
            for j in range(0, len(app_redis_item_list)):
                res_item = app_redis_item_list[j];
                col_item = col_list[j];
                if res_item:
                    # 时间类型判断
                    if type(res_item) == type(now):
                        result_item[col_item] = res_item.strftime("%Y-%m-%d %H:%M:%S");
                    else:
                        result_item[col_item] = res_item;
                else:
                    continue
            result_list.append(result_item);
            # print('create_time : ', result_item['create_time'])
            # print(' result_item : ', result_item)
    else :
        return None
    return result_list

