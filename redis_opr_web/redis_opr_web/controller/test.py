from django.http import HttpResponse
from django.shortcuts import render
from types import FunctionType
from django.views.decorators.csrf import csrf_exempt
from ..core import RouteConfig
from ..core import Router
from ..core import utils
import sys



class AppRoute:  # 定义控制类  方法名对应请求的 最后 uri
    def index(self ,request ):
        print("我是index ...方法")
        context = {}
        context['hello'] = 'Hello World!'
        myarr = ['jason', 'tom', 'ketty'];
        context['arrayNodes'] = myarr;
        return render(request, 'index.html', context)

    def toModalContent(self ,request ):
        print("我是index ...方法")
        context = {}
        context['hello'] = 'Hello World!'
        myarr = ['jason', 'tom', 'ketty'];
        context['arrayNodes'] = myarr;
        return render(request, 'modalContent.html', context)




# 初始化 路由类
appRouteInst  = AppRoute();

'''
处理请求转发， 通过 Router.route 方法 将请求映射到 AppRoute 的实例 （appRouteInst） 方法中处理
'''
@csrf_exempt
def route(request):
    return Router.route(request , utils.getThisPythonFileName(sys._getframe()) , AppRoute ,route , appRouteInst );