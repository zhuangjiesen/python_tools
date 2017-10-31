'''
通用 redis操作

'''
import redis
# 链接redis 并存入数据库
from ..core.my_redis import RedisCluster
from ..core.my_redis import RedisClient
from ..core.mysql import MysqlClient

# redis_opr 数据库的操作
from ..core.mysql import RedisDbOpr

# 工具类
from ..core import utils
from ..core.Common import AjaxResponse
# 普通方法返回值
from ..core.Common import CommonMethodResult



def saveServerInfo(redis_client , app_server_id ):
    serverInfo = RedisClient.getServer(redis_client);
    tableName = 'instance_server';
    serverInfo['app_server_id'] = app_server_id;
    return RedisDbOpr.saveInfo(tableName, serverInfo);

def saveClientsInfo(redis_client , app_server_id):
    tableName = 'instance_clients';
    serverInfo = RedisClient.getClients(redis_client);
    serverInfo['app_server_id'] = app_server_id;
    return RedisDbOpr.saveInfo(tableName, serverInfo);

def saveCPUInfo(redis_client , app_server_id):
    serverInfo = RedisClient.getCPU(redis_client);
    tableName = 'instance_cpus';
    serverInfo['app_server_id'] = app_server_id;
    return RedisDbOpr.saveInfo(tableName, serverInfo);

def saveKeyspacesInfo(redis_client , app_server_id):
    serverInfo = RedisClient.getKeySpace(redis_client);
    tableName = 'instance_keyspaces';
    serverInfo['app_server_id'] = app_server_id;
    return RedisDbOpr.saveInfo(tableName, serverInfo);

def saveMemoriesInfo(redis_client , app_server_id):
    serverInfo = RedisClient.getMemory(redis_client);
    tableName = 'instance_memories';
    serverInfo['app_server_id'] = app_server_id;
    return RedisDbOpr.saveInfo(tableName, serverInfo);

def savePersistencesInfo(redis_client , app_server_id):
    serverInfo = RedisClient.getPersistence(redis_client);
    tableName = 'instance_persistences';
    serverInfo['app_server_id'] = app_server_id;
    return RedisDbOpr.saveInfo(tableName, serverInfo);

def saveReplicationsInfo(redis_client , app_server_id):
    serverInfo = RedisClient.getReplication(redis_client);
    tableName = 'instance_replications' , app_server_id;
    serverInfo['app_server_id'] = app_server_id;
    return RedisDbOpr.saveInfo(tableName, serverInfo);

def saveStatsesInfo(redis_client , app_server_id):
    serverInfo = RedisClient.getStats(redis_client);
    tableName = 'instance_statses';
    serverInfo['app_server_id'] = app_server_id;
    return RedisDbOpr.saveInfo(tableName, serverInfo);



# 获取集群信息
def saveClustersInfo(redis_client  , app_server_id):
    serverInfo = None;
    # 是否集群模式
    if RedisCluster.isClusterEnabled(redis_client) :
        RedisCluster.getClusterInfo()
        serverInfo = RedisClient.getClients(redis_client);
    if not serverInfo :
        return None
    tableName = 'instance_clusters';
    serverInfo['app_server_id'] = app_server_id;
    return RedisDbOpr.saveInfo(tableName, serverInfo);



# 慢查询日志
def saveSlowLogInfo(redis_client , app_server_id):
    tableName = 'instance_slow_log';

    serverInfo = None;
    # 获取日志长度
    logLen = RedisClient.getSlowLogLen(redis_client);
    # 获取日志列表
    slow_log_list = RedisClient.getSlowLog(redis_client, logLen);
    if slow_log_list and len(slow_log_list) > 0 :
        for log_item in slow_log_list :
            # 获取慢查询日志
            serverInfo['app_server_id'] = app_server_id;
    # 批量添加数据
    RedisDbOpr.saveInfoByBatch(tableName, slow_log_list) ;
    return True;




# 从数据库中获取redis server 数据 并获取redis连接
def getRedisConnectionByHostPort(host , port ):
    server = RedisDbOpr.getServerByHostAndPort(host, port);
    if server :
        print('server : ' ,server );
        pwd = None
        if utils.containsKey(server ,'requirepass' ):
            pwd = server['requirepass'];
        # 获取客户端连接
        redis_client = RedisClient.createRedisConn(host,port , pwd);
        return redis_client;
    else:
        return None;



# 从数据库中获取redis server 数据 并获取redis连接
def getRedisConnectionByServerId(server_id):
    server = RedisDbOpr.getServerByServerId(server_id);
    if server :
        print('server : ' ,server );
        pwd = None
        if utils.containsKey(server ,'requirepass' ):
            pwd = server['requirepass'];
        host = server['host']
        port = str (server['port']);
        # 获取客户端连接
        redis_client = RedisClient.createRedisConn(host,port , pwd);
        return redis_client;
    else:
        return None;


def getAppRedisIdByName(app_name):
    results = MysqlClient.query('app_redis', ['i_id'], {'app_name' : app_name}, None, [0 , 1]);
    if not results:
        return None;
    elif len(results) == 0 :
        return None;
    # print('results : ', results);
    return results[0];

# 获取服务列表
def getAppServerListByAppid(app_id):
    return RedisDbOpr.getServersByAppId(app_id);

# 获取app_redis列表
def getAppRedisList():
    return RedisDbOpr.getAppRedisList();



def getAppRedisByAppid(app_id):
    app_redis = RedisDbOpr.getAppRedisByAppId(app_id);
    if app_redis and len(app_redis) > 0 :
        return app_redis[0];
    return None;


# 添加应用
def saveAppRedis(app_redis):
    RedisDbOpr.saveInfo('app_redis', app_redis);
    return True;

# 插入服务表
def saveAppServer(app_id , app_server):
    app_server['app_id'] = app_id;
    RedisDbOpr.saveInfo('app_server', app_server);
    return True;



# 检测redis连接
def testRedisClientListConn(redis_server_list):
    commonMethodResult = CommonMethodResult();
    # res = {};

    redis_client_list = [];
    if redis_server_list and len(redis_server_list) > 0 :
        for app_server_item in redis_server_list :
            host = app_server_item['host'];
            port = app_server_item['port'];
            pwd = None;
            if utils.containsKey(app_server_item , 'requirepass' ) :
                pwd = app_server_item['requirepass'];
            redis_client = RedisClient.createRedisConn(host , port , pwd);
            if redis_client.success :
                print(' 服务 ' , host , ':' , str(port) , ' msg : ' , redis_client.msg)
                redis_client_list.append(redis_client);
                continue;
            else :
                commonMethodResult.success = False;
                msg = ' 服务 ' + host + ':' + str(port) + ' msg : ' + redis_client.msg ;
                commonMethodResult.msg = msg;
                print(msg)

                return commonMethodResult;
    else:
        commonMethodResult.success = False;
        commonMethodResult.msg = '请输入应用'
        return commonMethodResult;

    commonMethodResult.result = {};
    commonMethodResult.result['redis_client_list'] = redis_client_list;
    commonMethodResult.success = True;
    commonMethodResult.msg = '成功连接'
    return commonMethodResult;


def isRedisClusterEnabled(redis_client):
    return RedisCluster.isClusterEnabled(redis_client);


def isRedisClusterListEnabled(redis_client_list):
    res = {};
    if redis_client_list and len(redis_client_list) > 0 :
        for redis_client in redis_client_list :
            if not isRedisClusterEnabled(redis_client) :
                res['result'] = False;
                res['msg'] = redis_client.host + ':' + redis_client.port + ' 实例未设置 cluster enable '
                return res;
        return True;
    else:
        return None


# 检测主从 单机状态下的状态
def testStandaloneServerList(server_list):
    commonMethodResult = CommonMethodResult();

    # res = {};
    master_list = [];
    slave_list = [];

    redis_client_list = [];
    conn_res = testRedisClientListConn(server_list);
    # 获取连接
    if conn_res.success == True :
        # 获取客户端连接对象
        redis_list = conn_res.result['redis_client_list'];
        if redis_list and len(redis_list) > 0 :
            for redis_client_item in redis_list :
                redis_client = RedisClient.createRedisConn(redis_client_item.host , redis_client_item.port , redis_client_item.pwd);
                replication = RedisClient.getReplication(redis_client);
                if replication :
                    role = replication['role'];
                    print(' name  : ' , redis_client.name)
                    print('role : ' , role)
                    # master
                    if role == 'master':
                        new_master = {};
                        new_master['redis_client'] = redis_client;
                        new_master['replication'] = replication;

                        master_list.append(new_master);
                        # 多个 master 不属于单机
                        if len(master_list) > 1 :
                            commonMethodResult.success = False;
                            msg = ''
                            for master_item in master_list :
                                msg += ' ' + master_item['redis_client'].host + ':' + str(
                                    master_item['redis_client'].port) +' 是 master ; ';
                            commonMethodResult.msg = msg;
                            return commonMethodResult;
                    else:
                        # slave
                        print()
                        new_slave = {};
                        new_slave['redis_client'] = redis_client;
                        new_slave['replication'] = replication;
                        slave_list.append(new_slave);
                else:
                    commonMethodResult.success = False;
                    msg = '无法确定 ' + redis_client_item.host + ':' + str(redis_client_item.port) + ' 的角色类型 '
                    print(msg)
                    commonMethodResult.msg = msg;
                    return commonMethodResult;
                print('replication : ' , replication)


        # 结果...
        if len(master_list) == 0 :
            commonMethodResult.success = False;
            msg = '没有 master 节点 '
            commonMethodResult.msg = msg;
            print(msg)
            return commonMethodResult;

        master = master_list[0];
        redis_client_list.append( master['redis_client']);
        # print('redis_client_list : ' , len(redis_client_list))
        # print('slave_list : ' , len(slave_list))
        if len(slave_list) > 0 :
            for slave_item in slave_list:
                redis_client = slave_item['redis_client'] ;
                replication = slave_item['replication'] ;
                master_host = replication['master_host']
                master_port = replication['master_port'];
                # 从节点 replication 的master 信息
                rep_master_name = master_host + ':' + str(master_port);
                print('rep_master_name : ', rep_master_name)
                master_redis_client = master['redis_client'];
                # 主节点信息
                master_name = master_redis_client.host + ':' +str(master_redis_client.port);
                print('master_name : ', master_name)
                if master_name == rep_master_name :
                    print(' 主从一致 ')
                    redis_client_list.append(redis_client);
                    continue;
                else:
                    commonMethodResult.success = False;
                    msg = ' 从节点 ' + redis_client.name + ' 的 master 不是 ' + master_name;
                    print(msg)
                    commonMethodResult.msg = msg;
                    return commonMethodResult;

        commonMethodResult.success = True;
        msg = '检测成功';
        print(msg)
        commonMethodResult.msg = msg;
        commonMethodResult.result = {};
        commonMethodResult.result['redis_client_list'] = redis_client_list;
        '''
        redis_client_list 
        格式 ：
        RedisClient.py中的 Redis_client 类
        
        '''
        # print('redis_client_list : ' , len(redis_client_list))
        return commonMethodResult;

    else:
        return conn_res;



# 检测 sentinel 模式
def testSentinelServerList(server_list):
    print()
    return None;

# 检测 集群 模式
def testClusterServerList(server_list):
    commonMethodResult = CommonMethodResult();
    # res = {};

    # 检测连接状态
    conn_res = testRedisClientListConn(server_list);
    # 获取连接
    if conn_res.success == True :
        # 获取客户端连接对象 列表
        redis_list = conn_res.result['redis_client_list'];
        if redis_list and len(redis_list) > 0 :
            # 获取连接 访问集群状态
            node_client_list = [];
            for redis_client_item in redis_list :
                redis_client = RedisClient.createRedisConn(redis_client_item.host , redis_client_item.port , redis_client_item.pwd);
                # TODO 获取集群信息作判断
                # cluster_nodes = RedisCluster.getClusterNodes(redis_client);
                # print('cluster_nodes : ' , cluster_nodes);
                node_client_list.append(redis_client);

            result = RedisCluster.isNodesInCluster(node_client_list);
            if not result.success :
                commonMethodResult.success = False;
                msg = result.msg;
                print(msg)
                commonMethodResult.msg = msg;
                return commonMethodResult;
            # print('isNodesInCluster : ' , result.toDict() );

            '''
                    返回值格式
                    res['success'] = False;
                    msg = '无法确定 ' + redis_client_item.host + ':' + str(redis_client_item.port) + ' 的角色类型 '
                    print(msg)
                    res['msg'] = msg;
                    return res;
                '''

        commonMethodResult.success = True;
        msg = '检测成功';
        print(msg)
        commonMethodResult.msg = msg;
        commonMethodResult.result = {};
        commonMethodResult.result['redis_client_list'] = conn_res.result['redis_client_list'];
        # print('redis_client_list : ' , len(redis_client_list))
        return commonMethodResult;
    else:
        return conn_res;




# app_redis 表单结果的解析
def parseRedisNode2ServerList (redispass ,redis_node_info ):
    commonMethodResult = CommonMethodResult();

    if not (redis_node_info and len(redis_node_info) > 0) :
        commonMethodResult.success = False;
        commonMethodResult.msg = '请输入 redis 实例列表'
        return commonMethodResult.toDict();
    if not (redispass and len(redispass) > 0) :
        redispass = None;


    server_list = [];
    splitStr = "\r\n";
    maohao = ":";

    redis_node_info_arr = redis_node_info.split(splitStr);
    if len(redis_node_info_arr) > 0:
        for redis_node_info_item in redis_node_info_arr :
            # 有端口号
            maohaoIndex = redis_node_info_item.find(maohao) ;
            if maohaoIndex > -1 :
                server_item = {};
                host = redis_node_info_item[0 : maohaoIndex];
                port = redis_node_info_item[maohaoIndex + 1 : len(redis_node_info_item)];
                name = host + ':' +str(port)
                print(' server name : ' , name)
                server_item['name'] = name
                server_item['host'] = host
                server_item['port'] = port
                server_item['requirepass'] = redispass


                server_list.append(server_item);
            else:
                commonMethodResult.success = False;
                commonMethodResult.msg = redis_node_info_item + ' 实例没配置端口号 '
                print(commonMethodResult.msg);
                return commonMethodResult.toDict();
            print('redis_node_info_item : ' , redis_node_info_item);

    if len(server_list) > 0 :
        commonMethodResult.success = True;
        commonMethodResult.msg = '操作成功'
        commonMethodResult.result = {};
        commonMethodResult.result['server_list'] = server_list;
    else :
        commonMethodResult.success = False;
        commonMethodResult.msg = '未解析成功请检查格式'


    return commonMethodResult;



# 插入 app_redis 表并获取app_id
def saveAppRedisAndGetId(app_redis):
    saveAppRedis(app_redis);
    # 获取id 插入执行的时候获取不到 id 所以重新查了一次
    app_id = getAppRedisIdByName(app_redis['app_name'])['i_id'];
    print('app_id : ', app_id);
    return app_id;




# 删除节点所有的槽位
def delAllClusterNodeSlots(name , requirepass):
    host = name.split(':')[0]
    port = name.split(':')[1]

    server_item = {};
    server_item['host'] = host;
    server_item['port'] = port;
    server_item['requirepass'] = requirepass;

    server_list = [];
    server_list.append(server_item);
    # 检测连接
    testResult = testRedisClientListConn(server_list);
    print(" testResult : ", testResult.toDict())
    if not testResult.success:
        ajaxResp = AjaxResponse();
        ajaxResp.success = False;
        ajaxResp.msg = testResult.msg;
        return ajaxResp;
    else:
        # 成功连接
        print(' testConnection 成功 .')
        redis_client_list = testResult.result['redis_client_list'];
        redis_client = redis_client_list[0];
        clusterSlots = RedisCluster.getClusterSlots(redis_client);
        if clusterSlots and len(clusterSlots) > 0:
            for clusterSlotItem in clusterSlots:
                node_name = clusterSlotItem['node_name'];
                if name == node_name:
                    from_slots = int(clusterSlotItem['from_slots']);
                    to_slots = int(clusterSlotItem['to_slots']);
                    if from_slots == to_slots:
                        RedisCluster.delSlots(redis_client, from_slots);
                    else:
                        for slot in range(from_slots, to_slots + 1):
                            result = RedisCluster.delSlots(redis_client, slot);
                            if not result:
                                ajaxResp = AjaxResponse();
                                ajaxResp.success = False;
                                ajaxResp.msg = '删除失败';
                                return ajaxResp;
    return True;




