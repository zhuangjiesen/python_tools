'''
线程任务

'''
import threading
import datetime
import time
import threadpool
from ...core.mysql import RedisDbOpr
from ...service import redisCommonOpr
from ...core.my_redis import RedisCluster
from ...core.my_redis import RedisClient

# 定时器开关 是否开启
CONF_ENABLED = False;
# CONF_ENABLED = False;
# 线程池大小
THREAD_SIZE = 20;

# 线程休眠时间 (秒)
SLEEP_TIME_SECONDS = 5;


class Task :
    redisClientServer = None
    taskName = None

    def toDict(self):
        dict = {};
        dict['redisClientServer'] = self.redisClientServer
        dict['taskName'] = self.taskName
        return dict;


# ==============基础   info 命令的信息采集 ==================
def getRedisInfoAndSave(redis_client , serverName , server_id ):
    # 更新 instance_server

    res = RedisClient.getRedisConnection(redis_client);
    if res['success'] == False :
        # 获取连接失败 更新服务状态
        print('获取连接失败 更新服务状态')
        print('==============================')
        RedisDbOpr.updateInfo('app_server' , server_id ,{
            'status' : 2,
            'status_desc' :  res['msg']
        });
    else :
        #
        serverInfo = RedisClient.getServer(redis_client)
        print('serverInfo : ', serverInfo);
        serverInfo['name'] = serverName
        serverInfo['app_server_id'] = server_id
        RedisDbOpr.saveInfo('instance_server', serverInfo);

        # 更新 instance_replications
        replication = RedisClient.getReplication(redis_client)
        print('replication : ', replication);
        replication['app_server_id'] = server_id
        RedisDbOpr.saveInfo('instance_replications', replication);

        # 更新 instance_cpus
        CPU = RedisClient.getCPU(redis_client)
        print('CPU : ', CPU);
        CPU['app_server_id'] = server_id
        RedisDbOpr.saveInfo('instance_cpus', CPU);

        # 更新 instance_keyspaces
        keyspace = RedisClient.getKeySpace(redis_client)
        print('keyspace : ', keyspace);
        keyspace['app_server_id'] = server_id
        RedisDbOpr.saveInfo('instance_keyspaces', keyspace);

        # 更新 instance_statses
        statse = RedisClient.getStats(redis_client)
        print('statse : ', statse);
        statse['app_server_id'] = server_id
        RedisDbOpr.saveInfo('instance_statses', statse);

        # 更新 instance_persistences
        persistence = RedisClient.getPersistence(redis_client)
        print('persistence : ', persistence);
        persistence['app_server_id'] = server_id
        RedisDbOpr.saveInfo('instance_persistences', persistence);

        # 更新 instance_memories
        memoryInfo = RedisClient.getMemory(redis_client)
        print('memoryInfo : ', memoryInfo);
        memoryInfo['app_server_id'] = server_id
        RedisDbOpr.saveInfo('instance_memories', memoryInfo);

        # 更新 instance_slow_log
        slowLogLen = RedisClient.getSlowLogLen(redis_client);
        slowLogList = RedisClient.getSlowLogList(redis_client, slowLogLen);
        print('slowLog : ', slowLogList);
        if slowLogList and len(slowLogList) > 0:
            for slowLogItem in slowLogList:
                slowLogItem['app_server_id'] = server_id
                RedisDbOpr.saveInfo('instance_slow_log', slowLogItem);



# 更新 instance_clusters 集群状态
def getAndSaveClusterInfo(redis_client , server_id ):
    if RedisCluster.isClusterEnabled(redis_client) :
        clusterInfo = RedisCluster.getClusterInfo(redis_client)
        print('clusterInfo : ', clusterInfo);
        clusterInfo['app_server_id'] = server_id
        RedisDbOpr.saveInfo('instance_clusters', clusterInfo );

    else:
        print('clusterInfo : no .');
        print('非集群模式')




# task 是 字典类型  Task.toDict传入的
def scheduledGetRedisInfo(task):
    redisClientServer = task['redisClientServer'];
    server_item = redisClientServer['server'] ;
    server_id = server_item['i_id'];
    print('server_id : ' , server_id);

    redis_client = redisClientServer['redis_client'];
    taskName = task['taskName']
    serverName = server_item['name'];

    # print("taskName : ", taskName , '  nowSecond : scheduledGetRedisInfo : ' + redis_client.name);
    # serverInfo = RedisClient.getServer(redis_client);
    # print('task : ')

    # 更新 app_server
    # 更新 instance_clients
    clientInfo = RedisClient.getClients(redis_client)
    print('clientInfo : ' , clientInfo);
    clientInfo['app_server_id'] = server_id
    RedisDbOpr.saveInfo('instance_clients', clientInfo );

    # ==============基础   info 命令的信息采集 ==================
    getRedisInfoAndSave(redis_client , serverName , server_id );

    # 更新 instance_clusters 集群状态
    getAndSaveClusterInfo(redis_client , server_id);



class ThreadClass(threading.Thread):
    def run(self):
        now = datetime.datetime.now()
        print("%s says Hello World at time: %s" %
        (self.getName(), now))
        pool = threadpool.ThreadPool(THREAD_SIZE)
        while True:
            # 休眠
            time.sleep(SLEEP_TIME_SECONDS)
            # 查询app_server 数据
            server_list = RedisDbOpr.getAppServerList();
            print('查询app_server 数据... server_llist : ' , server_list) ;


            # 获取 redis 客户端 与 server 后续要用到 server_id
            redis_server_client_list = [];
            print(' 获取redis 客户端...')
            # 无服务
            if not (server_list and len(server_list) > 0) :
                continue;
            else:
                for server_item in server_list :
                    host = server_item['host']
                    port = server_item['port']
                    redis_client = redisCommonOpr.getRedisConnectionByHostPort(host , port);
                    redis_server_client = {};
                    redis_server_client['server'] = server_item;
                    redis_server_client['redis_client'] = redis_client;

                    redis_server_client_list.append(redis_server_client)


            # 无服务
            if not ( redis_server_client_list and len(redis_server_client_list) > 0) :
                continue
            else:
                # 封装任务 分发给线程池 查询 redis 信息并放到数据库
                task_list = []
                if redis_server_client_list and len(redis_server_client_list) > 0:
                    for redis_server_client_item in redis_server_client_list:
                        task = Task();
                        task.redisClientServer = redis_server_client_item;
                        Task.taskName = 'task_' + redis_server_client_item['redis_client'].name;
                        task_list.append(task.toDict())

                # 开启线程池定时任务
                # task_list = ['a', 'b', 'c', 'd']
                if task_list and len(task_list) > 0:
                    start_time = time.time()
                    requests = threadpool.makeRequests(scheduledGetRedisInfo, task_list)
                    [pool.putRequest(req) for req in requests]
                    pool.wait()
                else:
                    now = datetime.datetime.now();
                    print('当前无任务 time : ', now)
                    continue;





# 开启定时任务
def startTask():
    # 开启线程
    t = ThreadClass()
    t.setDaemon(True);
    t.start();



