from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def hello(request):
    return HttpResponse('Hello World!')


@csrf_exempt
def page_not_found(request):
    print(' iam page_not_found.... ')
    return render_to_response('404.html')