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
from django.http import Http404


from ..service import redisCommonOpr



# ajax 返回值
from ..core.Common import AjaxResponse
import sys
import json
from ..service import dataDictionaryOpr


class AppRoute:  # 定义控制类  方法名对应请求的 最后 uri
    def index(self ,request ):
        print("我是index ...方法")
        context = {}
        context['hello'] = 'Hello World!'
        myarr = ['jason', 'tom', 'ketty'];
        context['arrayNodes'] = myarr;
        return render(request, 'redis/index.html', context)

    # 获取单机服务详情信息
    def toStandaraloneServerDetail(self ,request ):
        context = {}
        getParams = Router.getPostReqParams(request.GET);
        print(' request.postParams : ' , getParams );
        server_id = None;
        if not utils.containsKey(getParams , 'server_id') :
            raise Http404("请输入app_id")
        server_id = getParams['server_id'];
        print('server_id : ' , server_id)
        # 获取服务列表
        redis_client = redisCommonOpr.getRedisConnectionByServerId(server_id);
        print('redis_client : ' , redis_client)
        if redis_client :
            if redis_client.success :
                infoList = [];
                # plainInfo = {};
                # plainInfo['host'] = redis_client.host;
                # plainInfo['port'] = redis_client.port;
                # context['info'] = plainInfo;
                serverInfo = RedisClient.getServer(redis_client);
                print('serverInfo : ' , serverInfo)
                serverInfo['name'] = '服务器配置';
                # context['serverInfo'] = serverInfo;
                infoList.append(serverInfo)

                memoryInfo = RedisClient.getMemory(redis_client)
                memoryInfo['name'] = '内存配置';
                # context['memoryInfo'] = memoryInfo;
                infoList.append(memoryInfo)

                replicationInfo = RedisClient.getReplication(redis_client)
                replicationInfo['name'] = '主从信息';
                # context['replicationInfo'] = replicationInfo;
                infoList.append(replicationInfo)

                # print('replicationInfo : ' , replicationInfo)
                cpuInfo = RedisClient.getCPU(redis_client)
                cpuInfo['name'] = 'cpu情况';
                # context['cpuInfo'] = cpuInfo;
                infoList.append(cpuInfo)

                clusterInfo = {};
                if not RedisCluster.isClusterEnabled(redis_client):
                    clusterInfo['enable'] = 'True'
                else:
                    clusterInfo = RedisCluster.getClusterInfo(redis_client)
                clusterInfo['name'] = '集群配置';
                # context['clusterInfo'] = clusterInfo;
                infoList.append(clusterInfo)

                keyspaceInfo = RedisClient.getKeySpace(redis_client);
                keyspaceInfo['name'] = '键空间';
                # context['keyspaceInfo'] = keyspaceInfo;
                infoList.append(keyspaceInfo)

                persistenceInfo = RedisClient.getPersistence(redis_client)
                persistenceInfo['name'] = '持久化信息';
                context['persistenceInfo'] = persistenceInfo;
                # infoList.append(persistenceInfo)

                clientsInfo = RedisClient.getClients(redis_client)
                clientsInfo['name'] = '客户端信息';
                # context['clientsInfo'] = clientsInfo;
                infoList.append(clientsInfo)
                context['infoList'] = infoList;

                for i in range(0,len(infoList)) :
                    infoItem = infoList[i];
                    infoItem['index'] = i;
                return render(request, 'redis/standaralone/server-standaralone.html', context)
            else:
                raise Http404(redis_client.msg)
        else:
            raise Http404("服务未启动，请重试")







# 初始化 路由类
appRouteInst  = AppRoute();

'''
处理请求转发， 通过 Router.route 方法 将请求映射到 AppRoute 的实例 （appRouteInst） 方法中处理
'''
@csrf_exempt
def route(request):
    return Router.route(request , utils.getThisPythonFileName(sys._getframe()) , AppRoute ,route , appRouteInst );