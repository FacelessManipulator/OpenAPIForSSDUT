#coding=utf-8
from django.shortcuts import render
from django.http.response import JsonResponse
from restfulapi import settings
from models import Bkstz
import re
# Create your views here.

response_200 = {'code': 200, 'data':""}
response_201 = {'code': 201, 'message': "The account has been updated."}
response_404 = {'code': 404, "error": "Couldn't found the required resource."}
response_500 = {'code': 500, "error": "Oops, the server crashed."}
response_400 = {'code': 400, "error": "Wrong request. Please check your params."}
response_401 = {'code': 401, "error": "You should login in first.",
                             "url": "".join((settings.SITE_NAME, '/login'))}
response_403 = {'code': 403, "error": "You are forbidden to request this resources"}


def get_bkstz(request, id=None):
    if request.method == 'GET':
        if id is None:
            try:
                page = int(request.GET.get('page', 0))
                limit = int(request.GET.get('limit', 10))
            except ValueError,e:
                return JsonResponse(response_400)
            #有效性检测
            if(page < 0 or limit < 0):
                return JsonResponse(response_400)
            try:
                data = Bkstz.get_bkstz_list(page, limit)
                return JsonResponse({"code": 200, 'type': 'list', 'count': len(data), "data": data})
            except Exception,e:
                return JsonResponse(response_500)
        else:
            #检查id有效性，虽然url部分已经检查过了
            if re.match(r"^[a-f\d]{24}$", id) is None:
                return JsonResponse(response_400)
            else:
                try:
                    data = Bkstz.get_bkstz(id)
                    return JsonResponse({"code": 200, 'type': 'map', "data": data})
                except Exception,e:
                    return JsonResponse(response_500)
    else:
        return JsonResponse(response_400)




