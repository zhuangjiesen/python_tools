import psycopg2
from ..postgresql import PG_Conf
import datetime

# 数据库连接
class Pg_Conn:

    def getConn(self):
        conn = psycopg2.connect(database=PG_Conf.DATABASE, user=PG_Conf.USER, password=PG_Conf.PASSWORD,
                                host=PG_Conf.HOST, port=PG_Conf.PORT);
        return conn;


pg_Conn = Pg_Conn();


def getConn():
    return pg_Conn.getConn();



def insert(tableName , insertObject ):
    if not insertObject :
        return None;

    sql = ' insert into ${tableName} ( ${colNames})  values (${values})'
    sql = sql.replace('${tableName}', tableName);

    valuesList = [];
    colNames = '';
    values = '';
    for insertCol in insertObject :
        colNames += ' "' + insertCol + '" '
        colNames += ','
        if str(insertObject[insertCol]).find('nextval') == -1 :
            values += ' %s '
            values += ','
            valuesList.append(insertObject[insertCol])
        else:
            values += ' ' + str(insertObject[insertCol]);
            values += ','

    colNames = reduceLastChar(colNames);
    values = reduceLastChar(values);
    sql = sql.replace('${colNames}', colNames);
    sql = sql.replace('${values}', values);
    print('sql : ' , sql);
    # 数据库连接参数
    conn = getConn()
    cur = conn.cursor()
    cur.execute(sql , tuple(valuesList))
    # result_list = getCursorResult(cur);
    # print('result_list : ', result_list)
    conn.commit()
    cur.close()
    conn.close()
    # return result_list;
    return True;




'''
limitArr : [ 0 , 1] 数组
'''
def select(tableName, selectArray, whereParams, orderBy, limitArr):
    print()
    sql = ' select ${selectItem} from ${tableName} ';
    if whereParams:
        sql += ' where 1=1 ${whereParams}';

    sql += ' ${orderBy} ';
    sql += ' ${limit} ';
    sql = sql.replace('${tableName}', tableName);

    selectItemClause = '';
    whereParamsClause = '';

    whereValues = [];
    if selectArray and len(selectArray) > 0:

        for selectItem in selectArray :
            selectItemClause += '"';
            selectItemClause += selectItem
            selectItemClause += '" ,';


    else :
        selectItemClause = ' * ';

    sql = sql.replace('${selectItem}', selectItemClause);

    whereValues = [];
    if whereParams :
        for key in whereParams :
            whereParamsClause += ' AND ("';
            whereParamsClause += key;
            whereParamsClause += '" = %s ';
            whereParamsClause += '),';
            whereValues.append(whereParams[key]);

        whereParamsClause = reduceLastChar(whereParamsClause);


    sql = sql.replace('${whereParams}', whereParamsClause);

    if not orderBy :
        orderBy = '';
    sql = sql.replace('${orderBy}', orderBy);

    limit = '';
    if limitArr and len(limitArr) > 0 :
        if len(limitArr) == 2:
            limit += ' limit '+ str(limitArr[1]) + ' offset ' + str(limitArr[0]);
        elif len(limitArr) == 1:
            limit += ' limit '+ str(limitArr[0]);
        else:
            limit = '';
    else:
        limit = '';

    sql = sql.replace('${limit}', limit);

    print('sql : ' , sql);

    # 数据库连接参数
    conn = getConn()
    cur = conn.cursor()
    cur.execute(sql , tuple(whereValues))
    result_list = getCursorResult(cur);
    # print('result_list : ', result_list)
    conn.commit()
    cur.close()
    conn.close()
    return result_list;


def query(sql , params ):
    print()
    # 数据库连接参数
    conn = getConn()
    cur = conn.cursor()
    tupleParams = None;
    if params :
        tupleParams = tuple(params)
        cur.execute(sql ,tupleParams );
    else:
        cur.execute(sql );
    result_list = getCursorResult(cur);
    # print('result_list : ', result_list)
    conn.commit()
    cur.close()
    conn.close()
    return result_list;

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
    if result_list and len(result_list) == 1 :
        return result_list[0];
    return result_list



def reduceLastChar(str):
    if str and len(str) > 0:
        str = str[0: len(str) - 1];
    return str;


