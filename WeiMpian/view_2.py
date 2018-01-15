# coding=utf-8
# Create your views here.
import json
import os
import sys
import datetime
from PIL import Image
from django.core.files.base import ContentFile
from django.db.models import Q
from  django.http import HttpResponse
from django.core import serializers
import requests
import hashlib
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from multiprocessing.connection import Client
from unittest import TestCase
import urllib
# from django.core.serializers import json
from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response

import models
import time
from django import forms
from WEIMP import settings

from django.shortcuts import render



def addTag(request):
    request.encoding = 'utf-8'
    value = request.GET.get('value')
    price = request.GET.get('price')
    tagModel = models.tagTable.objects.filter(value=value)
    if len(tagModel) > 0:
        return HttpResponse('标签名字重复')
    else:
        m5 = hashlib.md5()
        m5.update(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        tagID = m5.hexdigest()
        dict = {
            'value': value,
            'price': price,
            'tagID': tagID,
        }
        models.tagTable.objects.create(**dict)
        return HttpResponse('创建成功')


# 修改
def updateTag(request):
    request.encoding = 'utf-8'
    pk = request.GET.get('pk'),
    tagModel = models.tagTable.objects.filter(pk=pk)
    if len(tagModel) > 0:
        value = request.GET.get('value'),
        price = request.GET.get('price'),
        tagModel[0].value = value
        tagModel[0].price = price
        tagModel[0].save()
        return HttpResponse('修改成功')
    else:
        return HttpResponse('标签不存在')


# 删除标签
def deleteTag(request):
    pk = request.GET.get('pk')
    tagModel = models.tagTable.objects.filter(pk=pk)
    if len(tagModel) > 0:
        tagModel.delete()
        return HttpResponse('删除成功')
    else:
        return HttpResponse('标签不存在')


# 获取标签
def getTagList(request):
    request.encoding = 'utf-8'
    tagModelList = models.tagTable.objects.all()
    tagModelJson = serializers.serialize("json", tagModelList)
    return HttpResponse(tagModelJson)
