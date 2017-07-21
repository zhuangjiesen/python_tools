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
        dataDictionaryList = dataDictionaryOpr.getDataDictionaryList();
        print('dataDictionaryList : ' , dataDictionaryList)
        context['dataDictionaryList'] = dataDictionaryList;
        return render(request, 'redis/redisConf/keywordConf.html', context)



    # 添加字典
    def saveDataDictionary(self ,request ):
        # 获取post 请求参数
        reqParams = Router.getPostReqParams(request.POST);
        print('reqParams : ' , reqParams)
        if not utils.containsKey(reqParams , 'key') or len(reqParams['key']) == 0 :
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = '请输入名称';
            return Router.endAjaxHttpResponse(ajaxResp);
        if not utils.containsKey(reqParams , 'value') or len(reqParams['value']) == 0 :
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = '请输入值';
            return Router.endAjaxHttpResponse(ajaxResp);

        dataDictionary = dataDictionaryOpr.getDataDictionaryByKey(reqParams['key']);
        if dataDictionary :
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = 'key值重复';
            return Router.endAjaxHttpResponse(ajaxResp);

        # print('dataDictionary : ' , dataDictionary)
        comRes = dataDictionaryOpr.saveDataDictionary(reqParams);
        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        ajaxResp.result = {};
        return Router.endAjaxHttpResponse(ajaxResp);
        # return render(request, 'redis/common/redis-app-form.html', context)


    def deleteDataDictionaryById(self ,request):
        reqParams = Router.getPostReqParams(request.POST);
        if not utils.containsKey(reqParams , 'ids') or len(reqParams['ids']) == 0 :
            ajaxResp = AjaxResponse();
            ajaxResp.success = False;
            ajaxResp.msg = '请选择至少一项';
            return Router.endAjaxHttpResponse(ajaxResp);
        ids = reqParams['ids'];
        idArr = ids.split(',');
        for idItem in idArr:
            dataDictionaryOpr.deteleDataDictionaryById(idItem);

        ajaxResp = AjaxResponse();
        ajaxResp.success = True;
        ajaxResp.msg = '操作成功';
        return Router.endAjaxHttpResponse(ajaxResp);


    # 获取应用列表 待分页
    def getDataDictionaryByKey(self ,request):
        reqParams = Router.getPostReqParams(request.GET);
        dataDictionary = dataDictionaryOpr.getDataDictionaryByKey(reqParams['key']);
        ajaxResp = AjaxResponse();
        if dataDictionary :
            ajaxResp = AjaxResponse();
            ajaxResp.success = True;
            ajaxResp.msg = '操作成功';
            ajaxResp.result = {};
            ajaxResp.result['dataDictionary'] = dataDictionary;
            return Router.endAjaxHttpResponse(ajaxResp);
        else:
            ajaxResp.success = False;
            ajaxResp.msg = '找不到关键词';
        return Router.endAjaxHttpResponse(ajaxResp);









# 初始化 路由类
appRouteInst  = AppRoute();

'''
处理请求转发， 通过 Router.route 方法 将请求映射到 AppRoute 的实例 （appRouteInst） 方法中处理
'''
@csrf_exempt
def route(request):
    return Router.route(request , utils.getThisPythonFileName(sys._getframe()) , AppRoute ,route , appRouteInst );