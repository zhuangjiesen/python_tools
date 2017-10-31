from django.http import HttpResponse
from django.shortcuts import render
from types import FunctionType
from django.views.decorators.csrf import csrf_exempt
from ..core import RouteConfig
from ..core import Router
from ..core import utils
from ..core import Common
from ..core.my_redis import RedisClient
from ..core.my_redis import RedisCluster
from redis.exceptions import ResponseError



from ..service import redisCommonOpr



# ajax 返回值
from ..core.Common import AjaxResponse
import sys
import json



# redis 操作类请求
# ajax 返回值
from ..core.Common import AjaxResponse
import sys
import json
from django.http import Http404

class AppRoute:  # 定义控制类  方法名对应请求的 最后 uri
    def index(self ,request ):
        print("我是index ...方法")
        context = {}
        context['hello'] = 'Hello World!'
        myarr = ['jason', 'tom', 'ketty'];
        context['arrayNodes'] = myarr;
        return render(request, 'redis/index.html', context)
    def toClusterIndex(self ,request ):
        print("我是index ...方法")
        context = {}
        context['hello'] = 'Hello World!'
        myarr = ['jason', 'tom', 'ketty'];
        context['arrayNodes'] = myarr;
        return render(request, 'oprpage/html/redisCluster/redis-cluster-opr.html', context)

    def toClusterForm(self ,request ):
        print("我是index ...方法")
        context = {}
        context['hello'] = 'Hello World!'
        myarr = ['jason', 'tom', 'ketty'];
        context['arrayNodes'] = myarr;
        return render(request, 'oprpage/html/redisCluster/redisClusterForm.html', context)

    # redis 集群检测
    def testRedisCluster(self ,request):
        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        ajaxResp.result = {};


        host = '';
        reqParams = Router.getPostReqParams(request.POST);
        requirepass = None ;
        if utils.containsKey(reqParams , 'requirepass') :
            requirepass = reqParams['requirepass'];

        print(' request.postParams : ' , reqParams );
        # if not utils.containsKey(reqParams , 'app_id') :
        #     ajaxResp = AjaxResponse();
        #     ajaxResp.success = False;
        #     ajaxResp.msg = '参数错误';
        #     return Router.endAjaxHttpResponse(ajaxResp);
        server_item = reqParams;
        server_list = [];
        server_list.append(server_item);
        # 检测连接
        testResult = redisCommonOpr.testRedisClientListConn(server_list);
        print(" testResult : ", testResult.toDict())
        if not testResult.success:
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = testResult.msg;
            return Router.endAjaxHttpResponse(ajaxResp);
        else:
            # 成功连接
            print(' testConnection 成功 .')
            redis_client_list = testResult.result['redis_client_list'];
            redis_client = redis_client_list[0];

            # 检测 info cluster
            isClusterEnabled = RedisCluster.isClusterEnabled(redis_client);
            if not isClusterEnabled :
                ajaxResp = AjaxResponse();
                ajaxResp.success = False;
                ajaxResp.msg = 'info cluster 结果是 0 该实例不是集群状态!';
                return Router.endAjaxHttpResponse(ajaxResp);

            clusterNodes = RedisCluster.getClusterNodes(redis_client);
            # 还未添加集群
            redis_client_list = [];
            if clusterNodes and len(clusterNodes) > 1 :
                server_list = [];
                for clusterNodeItem in clusterNodes:
                    newClient = {};
                    host = clusterNodeItem['host'];
                    if host == '127.0.0.1':
                        host = reqParams['host'];
                        clusterNodeItem['host'] = host;
                    elif host == '' :
                        host = reqParams['host'];
                        clusterNodeItem['host'] = host;

                    newClient['host'] = host;
                    # 172.16.236.163
                    newClient['port'] = clusterNodeItem['port'];
                    newClient['requirepass'] = requirepass;
                    server_list.append(newClient);

                # 检测连接
                testResult = redisCommonOpr.testRedisClientListConn(server_list);
                print(" testResult : ", testResult.toDict())

                if not testResult.success:
                    ajaxResp = AjaxResponse();
                    ajaxResp.success = False;
                    ajaxResp.msg = testResult.msg;
                    return Router.endAjaxHttpResponse(ajaxResp);
                else:
                    # 成功连接
                    print(' testConnection 成功 .')
                    mredis_client_list = testResult.result['redis_client_list'];
                    redis_client_list = mredis_client_list;
            else:
                redis_client_list.append(redis_client);

            # 槽位信息统计 pie 表单统计
            cluster_slots = RedisCluster.getClusterSlots(redis_client);
            cluster_slots_count = RedisCluster.getSlotsCountInfo(redis_client , cluster_slots , host);
            print('cluster_slots : ' , cluster_slots);
            print('cluster_slots_count : ' , cluster_slots_count);


            # instances 实例统计信息
            nodes_info = [];
            # 遍历客户端连接
            for redis_client_item in redis_client_list :
                node_item_info = {};
                address = redis_client_item.name;
                address = address.replace("127.0.0.1", host);
                address = str(address);

                clusterNodeInfo = None;
                # 集群节点
                for clusterNodeItem in clusterNodes:
                    mName = '';
                    mName = clusterNodeItem['name'];
                    mHost = clusterNodeItem['host'];
                    mPort = clusterNodeItem['port'];
                    if mHost == '' :
                        host = reqParams['host'];
                        mHost = host;
                        mName = mHost + ':' + str(mPort);
                    clusterNodeItem['host'] = mHost;

                    mName = mName.replace("127.0.0.1", host);
                    mName = str(mName);
                    if address == mName:
                        clusterNodeInfo = clusterNodeItem;
                    else :
                        continue;




                # 槽位信息
                cluster_slot_count = None;
                print('cluster_slots_count : ' , cluster_slots_count)
                if not cluster_slots_count == None:
                    for cluster_slot_count_item in cluster_slots_count :
                        mName = cluster_slot_count_item['nodeName'];
                        mName = mName.replace("127.0.0.1", host);
                        if address == mName:
                            cluster_slot_count = cluster_slot_count_item;
                            break;


                if not clusterNodeInfo == None :
                    node_item_info['address'] = address;
                    node_item_info['name'] = address;
                    node_item_info['requirepass'] = requirepass;

                    node_item_info['nodeId'] = clusterNodeInfo['node_id'];

                    replication = RedisClient.getReplication(redis_client_item);
                    server = RedisClient.getServer(redis_client_item)
                    memory = RedisClient.getMemory(redis_client_item)

                    slowLogLength = RedisClient.getSlowLogLen(redis_client_item)
                    cpu = RedisClient.getCPU(redis_client_item);

                    print('replication : ' , replication)
                    node_item_info['role'] = replication['role'];
                    node_item_info['version'] = server['redis_version'];
                    memUsed = '';
                    memUsed = str(memory['used_memory_human']) + '/' + str(memory['total_system_memory_human'])
                    node_item_info['memUsed'] = memUsed;
                    dbsize = redis_client_item.redisClient.execute_command('dbsize');
                    node_item_info['dbsize'] = dbsize;

                    # 槽位信息
                    slotsInfo = '';
                    if cluster_slot_count :
                        slotsInfo = cluster_slot_count['slotsInfo'];

                    cpuInfo = str(cpu['used_cpu_user']) + '/' + str(cpu['used_cpu_sys'])
                    node_item_info['cpuInfo'] = cpuInfo;

                    node_item_info['slotsInfo'] = slotsInfo;
                    node_item_info['slowLogLength'] = slowLogLength;

                    nodes_info.append(node_item_info);

            print('clusterNodes : ' , clusterNodes);

            clusterStatusInfo = None;
            if redis_client_list and len(redis_client_list) > 0 :
                redis_client_item = redis_client_list[0];
                clusterStatusInfo = RedisCluster.getClusterInfo(redis_client_item);




            # ajaxResp.result = {};

            # 集群状态
            clusterStatus = {};
            clusterStatus['clusterStatusInfo'] = clusterStatusInfo;

            # 实例信息
            instancesStatus = {};
            instancesStatus['instancesInfo'] = nodes_info;

            # 槽位信息
            slotsInfo = {};
            slotsInfo['cluster_slots_count'] = cluster_slots_count;

            ajaxResp.result['clusterStatus'] = clusterStatus;
            ajaxResp.result['instancesStatus'] = instancesStatus;
            ajaxResp.result['slotsInfo'] = slotsInfo;

            # spareRandomSlotsToEmptyClusterNodes
            # ajaxResp.result['']


        return Router.endAjaxHttpResponse(ajaxResp);

    # 获取相应的详情
    def getRedisInstanceDetail(self, request):
        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        ajaxResp.result = {};


        host = '';
        reqParams = Router.getPostReqParams(request.POST);



        name = None ;
        if not utils.containsKey(reqParams , 'name'):
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = '节点 name 为空';
            return Router.endAjaxHttpResponse(ajaxResp);

        name = reqParams['name'];
        dataType = reqParams['dataType'];

        # detail
        # replicationDetail
        # memDetail
        # cpuDetail
        # slowLogDetail
        # slosInfoDetail
        requirepass = None;
        if utils.containsKey(reqParams, 'requirepass') or reqParams['requirepass'] != '':
             requirepass = reqParams['requirepass'];
        params = name.split(':');
        redis_client = RedisClient.createRedisConn(params[0] , params[1] , requirepass);


        info = None;
        if dataType == 'detail' :
            serverInfo = RedisClient.getServer(redis_client);

            info = serverInfo;
        elif dataType == 'replicationDetail' :
            replication = RedisClient.getReplication(redis_client);

            info = replication;
        elif dataType == 'memDetail' :
            memory = RedisClient.getMemory(redis_client);

            info = memory;
        elif dataType == 'cpuDetail' :
            cpu = RedisClient.getCPU(redis_client);

            info = cpu;
        elif dataType == 'slowLogDetail' :
            slowLogList = RedisClient.getSlowLogList(redis_client , 30);

            info = slowLogList;
        elif dataType == 'slosInfoDetail' :
            slotsInfo = RedisCluster.getClusterSlots(redis_client);
            curSlotInfo = None;

            slotsCountInfo = '';
            if slotsInfo and len(slotsInfo) > 0 :
                for slotInfoItem in slotsInfo :
                    node_name = slotInfoItem['node_name'];
                    if node_name == name :
                        new_from_slot = slotInfoItem['from_slots']
                        new_to_slot = slotInfoItem['to_slots'];
                        new_slotsCountInfo = str(new_from_slot) + '-' + str(new_to_slot);
                        # 已经存在
                        if curSlotInfo :
                            old_slotsCountInfo = curSlotInfo['slotsInfo'];
                            slotsCountInfo = old_slotsCountInfo + ' | ' + new_slotsCountInfo
                            curSlotInfo['slotsInfo'] = slotsCountInfo;
                        else:
                            curSlotInfo = slotInfoItem;
                            slotsCountInfo = new_slotsCountInfo;
                            curSlotInfo['slotsInfo'] = slotsCountInfo;
                            continue





            if curSlotInfo :
                del curSlotInfo['from_slots']
                del curSlotInfo['to_slots']
                info = curSlotInfo;

        else:
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = 'not dataType found !';
            return Router.endAjaxHttpResponse(ajaxResp);


        ajaxResp.result['info'] = info;
        return Router.endAjaxHttpResponse(ajaxResp);



    # 获取相应的详情
    def migrateClusterSlots(self, request):
        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        ajaxResp.result = {};



        host = '';
        reqParams = Router.getPostReqParams(request.POST);

        requirepass = None;
        if utils.containsKey(reqParams, 'requirepass') and not reqParams['requirepass'] == '':
             requirepass = reqParams['requirepass'];

        migrateSlotFrom = reqParams['migrateSlotFrom']
        migrateSlotTo = reqParams['migrateSlotTo']
        migrateToNodeName = reqParams['migrateToNodeName']
        # migratetoKeyDelay = reqParams['migratetoKeyDelay']
        migrateFromNodeId = reqParams['migrateFromNodeId']
        migrateFromNodeName = reqParams['migrateFromNodeName']

        migrateSlotFrom = int(migrateSlotFrom);
        migrateSlotTo = int(migrateSlotTo);
        if migrateSlotFrom > migrateSlotTo :
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = 'migrateSlotFrom 大于 migrateSlotTo ';
            return Router.endAjaxHttpResponse(ajaxResp);

        migrateFromNodeHost = migrateFromNodeName.split(':')[0]
        migrateFromNodePort = migrateFromNodeName.split(':')[1]
        from_redis_client = RedisClient.createRedisConn(migrateFromNodeHost , migrateFromNodePort , requirepass);

        migrateToNodeHost = migrateToNodeName.split(':')[0]
        migrateToNodePort = migrateToNodeName.split(':')[1]
        to_redis_client = RedisClient.createRedisConn(migrateToNodeHost , migrateToNodePort , requirepass);

        # 只 转移一个槽位
        slotsInfo = None;
        if migrateSlotFrom == migrateSlotTo :
            slotsInfo = RedisCluster.migrate_slots_to_new_node(from_redis_client, to_redis_client, migrateSlotFrom);
            if not slotsInfo['success'] :
                ajaxResp = AjaxResponse();
                ajaxResp.success = False;
                ajaxResp.msg = slotsInfo['msg'];
                return Router.endAjaxHttpResponse(ajaxResp);
        else:
            for slot in range(migrateSlotFrom , migrateSlotTo + 1) :
                slotsInfo = RedisCluster.migrate_slots_to_new_node(from_redis_client ,to_redis_client , slot );

        ajaxResp.msg = slotsInfo['msg'];
        return Router.endAjaxHttpResponse(ajaxResp);





    # 集群重置
    def resetAllClusterNode(self, request):
        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        ajaxResp.result = {};


        return Router.endAjaxHttpResponse(ajaxResp);


    # 添加槽位
    def addSlotsToClusterNode(self, request):
        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        ajaxResp.result = {};

        reqParams = Router.getPostReqParams(request.POST);
        requirepass = None ;
        if utils.containsKey(reqParams , 'requirepass') :
            requirepass = reqParams['requirepass'];

        allocNodeName = reqParams['allocNodeName'];

        allocSlotFrom = reqParams['allocSlotFrom'];
        allocSlotFrom = int(allocSlotFrom);
        allocSlotTo = reqParams['allocSlotTo'];
        allocSlotTo = int(allocSlotTo);
        if allocSlotFrom > allocSlotTo:
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = 'Slot From 大于 Slot To ！！';
            return Router.endAjaxHttpResponse(ajaxResp);

        host = allocNodeName.split(':')[0]
        port = allocNodeName.split(':')[1]

        server_list = [];
        server_item = {};
        server_item['host'] = host;
        server_item['port'] = port;
        server_item['requirepass'] = requirepass;
        server_list.append(server_item);
        # 检测连接
        testResult = redisCommonOpr.testRedisClientListConn(server_list);
        print(" testResult : ", testResult.toDict())
        if not testResult.success:
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = testResult.msg;
            return Router.endAjaxHttpResponse(ajaxResp);
        else:
            # 成功连接
            print(' testConnection 成功 .')
            redis_client_list = testResult.result['redis_client_list'];
            redis_client = redis_client_list[0];
            addSlotsResult = None;
            if allocSlotFrom == allocSlotTo :
                try:
                    addSlotsResult = RedisCluster.addSlots(redis_client, allocSlotFrom)
                except ResponseError as e:
                    exception = str(e);
                    ajaxResp = AjaxResponse();
                    ajaxResp.success = False;
                    ajaxResp.msg = exception;
                    return Router.endAjaxHttpResponse(ajaxResp);

                if not addSlotsResult == True:
                    ajaxResp = AjaxResponse();
                    ajaxResp.success = False;
                    ajaxResp.msg = addSlotsResult;
                    return Router.endAjaxHttpResponse(ajaxResp);
            else:
                # 分配槽位
                for slot in  range(allocSlotFrom , (allocSlotTo + 1)) :
                    try:
                        addSlotsResult = RedisCluster.addSlots(redis_client, slot)
                    except ResponseError as e:
                        exception = str(e);
                        ajaxResp = AjaxResponse();
                        ajaxResp.success = False;
                        ajaxResp.msg = exception;
                        return Router.endAjaxHttpResponse(ajaxResp);

                    if not addSlotsResult == True :
                        ajaxResp = AjaxResponse();
                        ajaxResp.success = False;
                        ajaxResp.msg = addSlotsResult;
                        return Router.endAjaxHttpResponse(ajaxResp);



        return Router.endAjaxHttpResponse(ajaxResp);


    # 删除节点
    def forgetClusterNode(self, request):
        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        ajaxResp.result = {};

        reqParams = Router.getPostReqParams(request.POST);
        requirepass = None ;
        if utils.containsKey(reqParams , 'requirepass') :
            requirepass = reqParams['requirepass'];

        nodeId = reqParams['nodeId'];
        name = reqParams['name'];

        host = name.split(':')[0]
        port = name.split(':')[1]

        clusterNodesClientsResult = RedisCluster.getRedisClientListByOneNode(host , port , requirepass);
        if clusterNodesClientsResult.success :
            redis_client_list = clusterNodesClientsResult.result['redis_client_list'];
            forget_node_rs = RedisClient.createRedisConn(host , port , requirepass);
            RedisCluster.forget_node(redis_client_list ,forget_node_rs );

        return Router.endAjaxHttpResponse(ajaxResp);

    # 自动分配节点
    def autoAllocClusterSlots(self, request):
        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        ajaxResp.result = {};

        reqParams = Router.getPostReqParams(request.POST);
        requirepass = None ;
        if utils.containsKey(reqParams , 'requirepass') :
            requirepass = reqParams['requirepass'];

        nodeNames = reqParams['nodeNames'];
        nodeNameArr = nodeNames.split(',');


        # 删除所有已经分配槽位
        for nodeNameItem in nodeNameArr:
            redisCommonOpr.delAllClusterNodeSlots(nodeNameItem  , requirepass);
            print()


        server_list = [];
        for nodeNameItem in nodeNameArr:
            host = nodeNameItem.split(':')[0]
            port = nodeNameItem.split(':')[1]
            new_server_item = {};
            new_server_item['host'] = host;
            new_server_item['port'] = port;
            new_server_item['requirepass'] = requirepass;
            server_list.append(new_server_item);


        testResult = redisCommonOpr.testRedisClientListConn(server_list);
        if not testResult.success:
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = testResult.msg;
            return Router.endAjaxHttpResponse(ajaxResp);


        redis_client_list = testResult.result['redis_client_list'];
        clusterSlots = RedisCluster.getClusterSlots(redis_client_list[0]);
        if len(clusterSlots) > 0:
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = '槽位清除出错';
            return Router.endAjaxHttpResponse(ajaxResp);

        slotsAllocResult = RedisCluster.spareRandomSlotsToEmptyClusterNodes(redis_client_list);



        return Router.endAjaxHttpResponse(ajaxResp);

    # 自动分配节点
    def deleteAllSlots(self, request):
        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        ajaxResp.result = {};

        reqParams = Router.getPostReqParams(request.POST);
        requirepass = None ;
        if utils.containsKey(reqParams , 'requirepass') :
            requirepass = reqParams['requirepass'];

        name = reqParams['name'];

        result = redisCommonOpr.delAllClusterNodeSlots(name , requirepass);
        if result == True:
            return Router.endAjaxHttpResponse(ajaxResp);
        else:
            return Router.endAjaxHttpResponse(result);



    # 分配从节点
    def addClusterSlaveNode(self, request):
        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        ajaxResp.result = {};

        reqParams = Router.getPostReqParams(request.POST);
        requirepass = None ;
        if utils.containsKey(reqParams , 'requirepass') :
            requirepass = reqParams['requirepass'];

        slaveNodeName = reqParams['newClusterSlaveNodeNameValue'];
        masterNodeName = reqParams['newClusterMasterNodeName'];

        slaveHost = slaveNodeName.split(':')[0]
        slavePort = slaveNodeName.split(':')[1]

        masterHost = masterNodeName.split(':')[0]
        masterPort = masterNodeName.split(':')[1]

        slave_redis_client = RedisClient.createRedisConn(slaveHost, slavePort, requirepass);
        if not slave_redis_client.success:
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = slave_redis_client.msg;
            return Router.endAjaxHttpResponse(ajaxResp);
        else:
            master_redis_client = RedisClient.createRedisConn(masterHost, masterPort, requirepass);
            if not master_redis_client.success:
                ajaxResp = AjaxResponse();
                ajaxResp.success = False;
                ajaxResp.msg = master_redis_client.msg;
                return Router.endAjaxHttpResponse(ajaxResp);



        slaveNodes = RedisCluster.getClusterNodesOfMyself(slave_redis_client)
        masterNodes = RedisCluster.getClusterNodesOfMyself(master_redis_client)
        result = slave_redis_client.redisClient.cluster('replicate', masterNodes['node_id'] );
        if not result :
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = '操作失败';
            return Router.endAjaxHttpResponse(ajaxResp);

        return Router.endAjaxHttpResponse(ajaxResp);

    # redis 集群 新节点添加
    def testRedisClusterNewNode(self ,request):
        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        ajaxResp.result = {};


        host = '';
        reqParams = Router.getPostReqParams(request.POST);
        requirepass = None ;
        if utils.containsKey(reqParams , 'requirepass') :
            requirepass = reqParams['requirepass'];

        print(' request.postParams : ' , reqParams );
        originNodeId = reqParams['originNodeId'];
        originName = reqParams['originName'];

        # if not utils.containsKey(reqParams , 'app_id') :
        #     ajaxResp = AjaxResponse();
        #     ajaxResp.success = False;
        #     ajaxResp.msg = '参数错误';
        #     return Router.endAjaxHttpResponse(ajaxResp);
        server_item = reqParams;
        server_list = [];
        server_list.append(server_item);
        # 检测连接
        testResult = redisCommonOpr.testRedisClientListConn(server_list);
        print(" testResult : ", testResult.toDict())
        if not testResult.success:
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = testResult.msg;
            return Router.endAjaxHttpResponse(ajaxResp);
        else:
            # 成功连接
            print(' testConnection 成功 .')
            redis_client_list = testResult.result['redis_client_list'];
            redis_client = redis_client_list[0];

            # 检测 info cluster
            isClusterEnabled = RedisCluster.isClusterEnabled(redis_client);
            if not isClusterEnabled :
                ajaxResp = AjaxResponse();
                ajaxResp.success = False;
                ajaxResp.msg = 'info cluster 结果是 0 该实例不是集群状态!';
                return Router.endAjaxHttpResponse(ajaxResp);

            clusterNodes = RedisCluster.getClusterNodes(redis_client);
            if clusterNodes :
                if len(clusterNodes) > 1 :
                    inOtherCluster = False;
                    for clusterNodeItem in clusterNodes:
                        node_id = clusterNodeItem['node_id'];
                        if originNodeId == node_id :
                            inOtherCluster = True;
                            ajaxResp = AjaxResponse();
                            ajaxResp.success = False;
                            ajaxResp.msg = '节点已经在集群中，无需添加';
                            return Router.endAjaxHttpResponse(ajaxResp);
                    # 不在集群中 且长度大于1 等于是别的集群的节点
                    if not inOtherCluster :
                        ajaxResp = AjaxResponse();
                        ajaxResp.success = False;
                        ajaxResp.msg = '节点已经在别的集群中！';
                        return Router.endAjaxHttpResponse(ajaxResp);

        # redis_client

        originHost = originName.split(':')[0]
        originPort = originName.split(':')[1]

        to_redis_client = RedisClient.createRedisConn(originHost , originPort , requirepass);
        if not to_redis_client.success :
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = to_redis_client.msg;
            return Router.endAjaxHttpResponse(ajaxResp);
        RedisCluster.meet_node_to_cluster(redis_client , to_redis_client );
        return Router.endAjaxHttpResponse(ajaxResp);



    # 实例操作
    def toInstanceOprIndex(self ,request ):
        print("我是index ...方法")
        context = {}
        context['hello'] = 'Hello World!'
        myarr = ['jason', 'tom', 'ketty'];
        context['arrayNodes'] = myarr;
        return render(request, 'oprpage/html/redisInstance/redis-instance-opr.html', context)


    # 性能页面
    def toInstanceOprIndex(self ,request ):
        print("我是index ...方法")
        context = {}
        context['hello'] = 'Hello World!'
        myarr = ['jason', 'tom', 'ketty'];
        context['arrayNodes'] = myarr;
        return render(request, 'oprpage/html/redisPerformance/redis-performance-opr.html', context)





# 初始化 路由类
appRouteInst  = AppRoute();

'''
处理请求转发， 通过 Router.route 方法 将请求映射到 AppRoute 的实例 （appRouteInst） 方法中处理
'''
@csrf_exempt
def route(request):
    return Router.route(request , utils.getThisPythonFileName(sys._getframe()) , AppRoute ,route , appRouteInst );