import redis


'''
作全局 缓存连接
'''


class RedisConnCache:
    cache = {};

    def __init__(self) -> None:
        super().__init__()


    def put(self, name, value):
        self.cache[name] = value;

    def get(self, name):
        if name in self.cache.keys():
            return self.cache[name];
        else:
            return None

    def delete(self, name):
        if name in self.cache.keys():
            del self.cache[name];
            return True;
        else:
            return None


redisConnCache_inst = RedisConnCache();



# 返回false说明redis连接失败
def getRedisConnection(rs):
    result = True;
    res = {};
    try:
        rs.ping()  # getting None returns None or throws an exception
    except (redis.exceptions.ConnectionError,
            redis.exceptions.BusyLoadingError, redis.exceptions.ResponseError) as e:
        print(' ConnectionError  : ', str(e))
        result = False;
        res['success'] = False;
        res['msg'] = str(e);
    if result:
        res['success'] = True;
        res['redis'] = rs;
    return res;



'''
redis 客户端
'''


class Redis_client:
    name = None;
    redisClient = None;
    host = None;
    port = None;
    pwd = None;
    success = False;
    msg = '';
    def __init__(self) -> None:
        super().__init__()


def createRedisConn(host, port, pwd):
    key = host + ':' + str(port);
    rs = redisConnCache_inst.get(key);
    if rs:
        print('获取缓存连接....')
        if getRedisConnection(rs.redisClient):
            # 连接还未中断
            return rs;
        else:
            redisConnCache_inst.delete(key);
            # 重新连接

    rs_client = None;
    if pwd:
        rs_client = redis.Redis(host=host, port=port, password=pwd, socket_timeout=1000,
                                socket_connect_timeout=1500,
                                decode_responses=True);

    else:
        rs_client = redis.Redis(host=host, port=port, socket_timeout=1000,
                                socket_connect_timeout=1500,
                                decode_responses=True);

    conn_res = getRedisConnection(rs_client);
    redis_client = Redis_client();
    redis_client.host = host;
    redis_client.port = port;
    redis_client.name = host + ':' + str(port);
    redis_client.pwd = pwd;
    if conn_res['success'] == False:
        redis_client.success = False;
        redis_client.msg = conn_res['msg'];
        return redis_client;

    redis_client.success = True;
    redis_client.msg = '连接成功';
    redis_client.redisClient = rs_client;

    redisConnCache_inst.put(key, redis_client);
    return redis_client;



# =========== redis 操作  =================

# 是否支持集群
def getServer(rs):
    res = rs.redisClient.info('server');
    return res;
def getClients(rs):
    res = rs.redisClient.info('Clients');
    return res;
def getMemory(rs):
    res = rs.redisClient.info('Memory');
    return res;
def getReplication(rs):
    res = rs.redisClient.info('Replication');
    return res;
def getPersistence(rs):
    res = rs.redisClient.info('Persistence');
    return res;
def getStats(rs):
    res = rs.redisClient.info('Stats');
    return res;
def getCPU(rs):
    res = rs.redisClient.info('CPU');
    return res;
def getKeySpace(rs):
    res = rs.redisClient.info('KeySpace');
    return res;

def getSlowLogList(rs , count ):
    slowlogs = rs.redisClient.execute_command('slowlog get' , count);
    # 解析slowlog 结果
    res = [];
    if slowlogs :
        for log_item in slowlogs :
            '''
            格式
            'id': item[0],
            'start_time': int(item[1]),
            'duration': int(item[2]),
            'command': b(' ').join(item[3])
            '''
            res_item = {};
            if log_item and len(log_item) > 3:
                res_item['id'] = log_item[0];
                res_item['start_time'] = log_item[1];
                res_item['duration'] = log_item[2];
                res_item['command'] = str(log_item[3]);
                print('log_item : ' , res_item);
                res.append(res_item);
    if len(res) == 0 :
        return None;

    return res;
def getSlowLogLen(rs ):
    res = rs.redisClient.slowlog_len();
    return res;




