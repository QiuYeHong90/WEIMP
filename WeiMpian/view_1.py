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
from django.shortcuts import render_to_response, render

import models
import time
from django import forms
from WEIMP import settings




def index(request):
    return HttpResponse('您好!欢饮')


import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# 获取二维码接口
def getQRCode(path):
    local_filename = getQRCodeName(path)
    judgeExists = judgeExistslocal_filename(local_filename)
    if judgeExists == True:
        return local_filename
    access_token = getAccess_token()
    if len(access_token) > 0:
        url = 'https://api.weixin.qq.com/cgi-bin/wxaapp/createwxaqrcode?access_token=' + access_token
        params = {"path": path,"width": 430}
        params = json.dumps(params).encode('utf-8')
        response = requests.post(url,params)
        local_filename = downloadImageFile(response,local_filename)
        return local_filename
    else:
        return ''


def getAccess_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx936fb333f8d8b718&secret=fdf14e625a1e63cf96250a90fc1ae17f'

    response = requests.get(url)
    python_obj = json.loads(response.text)

    return python_obj['access_token']

# 获取名字
def getQRCodeName(path):
    m5 = hashlib.md5()
    m5.update(path)
    filename = m5.hexdigest()
    local_filename = filename + '.png'
    return  local_filename
# 判断是否存在
def judgeExistslocal_filename(local_filename):
    if not os.path.exists(settings.QRCODE_PATH):
        os.mkdir(settings.QRCODE_PATH)
        return False
    if not os.path.exists(settings.QRCODE_PATH + local_filename):
        return False
    else:
        return True
# 图片读取放在本地
def downloadImageFile(r, local_filename):
    with open(settings.QRCODE_PATH + local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    return local_filename


def getMPKcondition(request):
    request.encoding = 'utf-8'
    userInforNum = models.userInfor.objects.all().count()
    MyCardNumAll = models.MyCard.objects.filter(cardType=1).count()
    data = {
        'COUNT':{
            'usedNumber':userInforNum,
            'MyCardNumAll':MyCardNumAll,
        },
    }
    return render(request, "weiCard.html", {'data': data})





