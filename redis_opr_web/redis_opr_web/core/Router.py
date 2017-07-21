from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from types import FunctionType
from ..core import RouteConfig
import json


'''
用来路由请求，请求分发
'''


'''
参数说明
prefix 请求过滤 处理请求的 py 文件名 
AppRoute 每个请求的类
route 每个处理请求 py 中的 route 方法 
appRouteInst AppRoute类的实例
'''
def route(request , prefix , AppRoute ,route , appRouteInst ):
    attr_dict = AppRoute.__dict__;
    method_name = route.__name__;
    url_path = request.path;
    uri_path = '';
    http_method = request.method;
    # print('url_path : ' , url_path);
    # print('method_name : ' , method_name);
    if http_method.lower() == 'get' :
        # 无参数
        if url_path.find('?') > -1 :
            end_index = url_path.find('?');
            uri_path = url_path[len(prefix) + 2 , end_index ];
        else :
            uri_path = url_path[len(prefix) + 2:];

    if http_method.lower() == 'post' :
        uri_path = url_path[len(prefix) + 2:];

    # 匹配后缀
    suffix_index = uri_path.find(RouteConfig.URI_SUFFIX);
    if uri_path.find(RouteConfig.URI_SUFFIX) > -1 :
        uri_path = uri_path[ 0 : suffix_index ];
    else:
        print('后缀不匹配 ')
        # return render(request, '404.html', None)
        raise Http404("非法请求")

    # print('uri_path : ' , uri_path)
    # 判断url是否在处理类的方法列表中 没有就404
    if uri_path in attr_dict.keys():
        # print('有方法....')
        # 映射到对应方法
        func = attr_dict[uri_path];
        return func(appRouteInst , request);
    else:
        print('uri_path : ' , uri_path)
        raise Http404("找不到请求")
        # return render(request, '404.html', None)






'''
返回 ajax 返回值 json 结果
'''
def endAjaxHttpResponse(ajaxResponse):
    print(' endJsonHttpResponse ....')
    return HttpResponse(json.dumps(ajaxResponse.toDict() , ensure_ascii=False ) ,content_type="application/json;charset=utf-8");



def getPostReqParams(postReq ):
    res = None;
    if postReq :
        res = {};
        for key in postReq :
            res[key] = postReq[key];
    return res;


def getGetReqParams(getReq ):
    res = None;
    if getReq :
        res = {};
        for key in getReq :
            res[key] = getReq[key];
    return res