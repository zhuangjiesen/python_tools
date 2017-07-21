from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from types import FunctionType
#要想在settings文件中取到变量就要先导入模块
from django.conf import settings

# 项目 zqxt 文件名 zqxt/middleware.py

class BlockedMiddleware(object):
    def process_request(self, request):
        print(' i am process_request ')
