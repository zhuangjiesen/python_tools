from django.http import HttpResponse
from django.shortcuts import render
from types import FunctionType
from django.views.decorators.csrf import csrf_exempt
from ..core import RouteConfig
from ..core import Router
from ..core import utils
from ..core.Common import AjaxResponse
import sys


class AppRoute:  # 定义控制类  方法名对应请求的 最后 uri
    def index(self ,request ):
        context = {}
        context['hello'] = 'Hello World! miniprogram ...'
        myarr = ['jason', 'tom', 'ketty'];
        context['arrayNodes'] = myarr;
        return render(request, 'miniprogram/index.html', context)

    def indexContent(self ,request ):
        context = {}

        ajaxResp = AjaxResponse();
        ajaxResp.success = False;
        ajaxResp.msg = "操作成功";
        return Router.endAjaxHttpResponse(ajaxResp);


# 初始化 路由类
appRouteInst  = AppRoute();

'''
处理请求转发， 通过 Router.route 方法 将请求映射到 AppRoute 的实例 （appRouteInst） 方法中处理
'''
@csrf_exempt
def route(request):
    return Router.route(request , utils.getThisPythonFileName(sys._getframe()) , AppRoute ,route , appRouteInst );


