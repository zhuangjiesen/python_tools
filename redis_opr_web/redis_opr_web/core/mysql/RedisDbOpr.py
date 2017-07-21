import redis
# 链接redis 并存入数据库
from ..my_redis import RedisCluster
from ..mysql import MysqlClient
import datetime

def getServerByHostAndPort(host , port) :
    server_name = host + ':' + str(port);
    return getServerByServerName(server_name);

def getServerByServerId(server_id):
    server = MysqlClient.query('app_server', None, {'i_id' : server_id}, None, None);
    if server and len(server) > 0 :
        return server[0];
    return None;

def getServerByServerName(server_name):
    server = MysqlClient.query('app_server', None, {'name'  : server_name}, None, [0 , 1]);
    if server and len(server) > 0 :
        return server[0];
    return None;

def getServersByAppId(app_id):
    servers = MysqlClient.query('app_server', None, {'app_id' : app_id}, None, None);
    return servers;



def getAppRedisByAppId(app_id):
    app_redis = MysqlClient.query('app_redis', None, {'i_id' : app_id}, None, None);
    return app_redis;


def getAppRedisList():
    app_redis_list = MysqlClient.query('app_redis', None, None, None, None);
    return app_redis_list;


# 插入
def saveInfo(tableName , info_data ):
    if not info_data :
        return None;

    # 查询字段数据库都有存在
    unknewn_cols = MysqlClient.checkTableCols(tableName, info_data);
    if unknewn_cols :
        for key in unknewn_cols :
            # 新增字段 异常不执行
            try:
                MysqlClient.alter_add_new_col(tableName, key, 255);
            except Exception as e:
                print(Exception, ":", e);

    # 插入数据库
    info_data['create_time'] = datetime.datetime.now();
    MysqlClient.insert(tableName, info_data);
    return True;


def saveInfoByBatch(tableName , info_data_arr ):
    # 查询字段数据库都有存在
    if info_data_arr and len(info_data_arr) > 0:
        for info_data_item in info_data_arr :
            unknewn_cols = MysqlClient.checkTableCols(tableName, info_data_item);
            if unknewn_cols :
                for key in unknewn_cols :
                    # 新增字段
                    MysqlClient.alter_add_new_col(tableName, key, 255);
            # 插入数据库
            MysqlClient.insert(tableName, info_data_item);
    else:
        return False

    return True;




# 更新
def updateInfo(tableName , id , new_info_data ):
    # 查询字段数据库都有存在
    unknewn_cols = MysqlClient.checkTableCols(tableName, new_info_data);
    if unknewn_cols :
        for key in unknewn_cols :
            # 新增字段
            MysqlClient.alter_add_new_col(tableName, key, 255);
    MysqlClient.update(tableName, 'i_id', id, new_info_data);
    return True;


#TODO 拉取 app_server 表中所有数据 后期可能要分页 此处是一次性拉取
def getAppServerList():
    servers = MysqlClient.query('app_server', [
        'i_id' , 'name' , 'host' , 'port' , 'requirepass'
    ] , { 'is_delete' :  '0' } , { 'i_id' : 'asc'}, None);
    return servers;




