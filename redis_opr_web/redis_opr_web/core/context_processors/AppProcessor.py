'''
应用全局 context 属性 用来配置 contextPath

'''
from ...core import RouteConfig


def loadContext(request):
    context = {};
    context['contextPath'] = RouteConfig.APP_URL;
    return context