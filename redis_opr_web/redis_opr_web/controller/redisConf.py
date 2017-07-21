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
from ..service import redisCommonOpr
from ..service import dataDictionaryOpr

# ajax 返回值
from ..core.Common import AjaxResponse
import sys
import json
from django.http import Http404


class AppRoute:  # 定义控制类  方法名对应请求的 最后 uri
    def index(self ,request ):
        context = {}
        dataDictionaryList = dataDictionaryOpr.getDataDictionaryKeywordList();
        print('dataDictionaryList : ' , dataDictionaryList)
        context['dataDictionaryList'] = dataDictionaryList;
        return render(request, 'redis/redisConf/keywordConf.html', context)
    def toRedisConf(self ,request ):
        context = {}
        dataDictionaryList = dataDictionaryOpr.getDataDictionaryRedisConfList();
        print('dataDictionaryList : ' , dataDictionaryList)
        context['dataDictionaryList'] = dataDictionaryList;
        return render(request, 'redis/redisConf/redisConf.html', context)

    def toKeywordConfForm(self ,request ):
        reqParams = Router.getPostReqParams(request.GET);
        context = {}
        if reqParams and  not  utils.containsKey(reqParams , 'i_id'):
            i_id = reqParams['i_id'];
            dataDictionary = dataDictionaryOpr.getDataDictionaryById(i_id);
            context['dataDictionary'] = dataDictionary;
        return render(request, 'redis/redisConf/keywordConfForm.html', context)


    def toRedisConfForm(self ,request ):
        reqParams = Router.getPostReqParams(request.GET);
        context = {}
        if reqParams and not utils.containsKey(reqParams , 'i_id'):
            i_id = reqParams['i_id'];
            dataDictionary = dataDictionaryOpr.getDataDictionaryById(i_id);
            context['dataDictionary'] = dataDictionary;
        return render(request, 'redis/redisConf/redisConfForm.html', context)

    # 添加应用入口
    def saveAppRedis(self ,request ):
        # 获取post 请求参数
        reqParams = Router.getPostReqParams(request.POST);
        if reqParams and  not utils.containsKey(reqParams , 'app_name') :
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = '请填写应用名';
            return Router.endAjaxHttpResponse(ajaxResp);


        app_name = reqParams['app_name'];
        app_redis_db = redisCommonOpr.getAppRedisIdByName(app_name);
        if app_redis_db:
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = '应用名重复';
            return Router.endAjaxHttpResponse(ajaxResp);

        # 解析 redis 节点
        serverParseResult = redisCommonOpr.parseRedisNode2ServerList(reqParams['redispass'] , reqParams['redis_node_info'] )
        if serverParseResult.success :
            print('解析成功 .')
        else:
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = serverParseResult.msg;
            return Router.endAjaxHttpResponse(ajaxResp);

        # 获取服务列表
        server_list = serverParseResult.result['server_list'];
        # print(" server_list : " , serverParseResult.result['server_list'])

        app_type = reqParams['app_type'];
        print(" app_type : " , app_type)

        # 单机模式
        if app_type == 'standalone':
            # 检测 standalone 状态
            testRes = redisCommonOpr.testStandaloneServerList(server_list);
            print(" testRes : ", testRes.toDict())
            if testRes.success:
                print(' testStandaloneServerList 成功 .')
            else:
                ajaxResp = AjaxResponse();
                ajaxResp.success = False;
                ajaxResp.msg = testRes.msg;
                return Router.endAjaxHttpResponse(ajaxResp);


            # 成功 继续加载
            # 插入 app_redis 表
            app_redis = reqParams;
            # 获取id 插入执行的时候获取不到 id 所以重新查了一次
            app_id = redisCommonOpr.saveAppRedisAndGetId(app_redis);
            print('app_id : ' ,app_id );
            # redis_client_list = testRes.result['redis_client_list'];
            # 插入 app_server 表
            if server_list and len(server_list) > 0 :
                for server_item in server_list :
                    print('server_item : ' , server_item['name'])
                    redisCommonOpr.saveAppServer(app_id, server_item);
                    continue;


        # sentinel 模式
        elif app_type == 'sentinel':
            print()
        # cluster 集群模式
        elif app_type == 'cluster':
            # 检测集群状态
            testResult = redisCommonOpr.testClusterServerList(server_list);
            print(" testResult : ", testResult.toDict())
            if testResult.success:
                print(' testStandaloneServerList 成功 .')
            else:
                ajaxResp = AjaxResponse();
                ajaxResp.success = False;
                ajaxResp.msg = testResult.msg;
                return Router.endAjaxHttpResponse(ajaxResp);

            # 成功 继续加载
            # 插入 app_redis 表
            app_redis = reqParams;
            # 获取id 插入执行的时候获取不到 id 所以重新查了一次
            app_id = redisCommonOpr.saveAppRedisAndGetId(app_redis);
            # 插入 app_server 表
            if server_list and len(server_list) > 0 :
                for server_item in server_list :
                    print('server_item : ' , server_item['name'])
                    redisCommonOpr.saveAppServer(app_id, server_item);
                    continue;
            print(' 检测成功 ！！！')




        print(" reqParams : " , reqParams)
        print("我是index ...方法")
        context = {}
        context['hello'] = 'Hello World!'
        myarr = ['jason', 'tom', 'ketty'];
        context['arrayNodes'] = myarr;

        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        ajaxResp.result = {};
        ajaxResp.result['name'] = '庄杰森'
        ajaxResp.result['age'] = 23

        return Router.endAjaxHttpResponse(ajaxResp);
        # return render(request, 'redis/common/redis-app-form.html', context)


    def toAppServerDetail(self ,request ):
        print("我是index ...方法")
        context = {}
        getParams = Router.getPostReqParams(request.GET);
        print(' request.postParams : ' , getParams );
        app_id = None;
        if not utils.containsKey(getParams , 'app_id') :
            raise Http404("请输入app_id")
        app_id = getParams['app_id'];
        print('app_id : ' , app_id)

        app_redis = redisCommonOpr.getAppRedisByAppid(app_id);
        app_type = None;
        if app_redis :
            app_type = app_redis['app_type']
        else:
            raise Http404("找不到该应用")
        context['app_redis'] = app_redis;
        # 获取服务列表
        app_servers = redisCommonOpr.getAppServerListByAppid(app_id);
        print('app_servers : ' , app_servers)
        context['app_servers'] = app_servers;
        if app_type == 'standalone' :

            return render(request, 'redis/common/app-standaralone.html', context)
        elif app_type == 'sentinel' :
            return render(request, 'redis/common/app-sentinel.html', context)
        elif app_type == 'cluster':
            return render(request, 'redis/common/app-cluser.html', context)
        else:
            raise Http404("找不到该应用")

    # 获取应用列表 待分页
    def getAppRedisList(self ,request):
        app_redis_list = redisCommonOpr.getAppRedisList();
        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        ajaxResp.result = {};
        ajaxResp.result['app_redis_list'] = app_redis_list;
        return Router.endAjaxHttpResponse(ajaxResp);









# 初始化 路由类
appRouteInst  = AppRoute();

'''
处理请求转发， 通过 Router.route 方法 将请求映射到 AppRoute 的实例 （appRouteInst） 方法中处理
'''
@csrf_exempt
def route(request):
    return Router.route(request , utils.getThisPythonFileName(sys._getframe()) , AppRoute ,route , appRouteInst );