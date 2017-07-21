"""redis_opr_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from .controller import view
from .controller import index
from .controller import user
from .controller import redis
from .controller import redisStandaralone
from .controller import redisCluster
from .controller import redisConf
from .controller import dataDictionary
from .controller import test
urlpatterns = [
    url(r'^index/', index.route),
    url(r'^user/', user.route),
    url(r'^redis/', redis.route),
    url(r'^redisStandaralone/', redisStandaralone.route),
    url(r'^redisCluster/', redisCluster.route),
    url(r'^redisConf/', redisConf.route),
    url(r'^dataDictionary/', dataDictionary.route),
    url(r'^test/', test.route),
]
