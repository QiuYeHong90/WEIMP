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
from django.shortcuts import render_to_response
from django.forms.models import model_to_dict
import models
import time
from django import forms

from WeiMpian import view_1


def index(request):
    return HttpResponse('hello,world!')


# 登陆
def login(request):
    code = request.GET.get('code'),
    # https: // api.weixin.qq.com / sns / jscode2session?appid =APPID & secret =SECRET & js_code =JSCODE & grant_type =authorization_code
    params = {'appid': 'wx9e6461eebe763b73',
              'secret': '182d62ba11eb23125f413626aebe8422',
              'js_code': code,
              'grant_type': 'authorization_code'
              }
    response = requests.get("https://api.weixin.qq.com/sns/jscode2session", params=params)
    python_obj = json.loads(response.text)
    if python_obj.has_key('openid') == False:
        return HttpResponse('登陆失败')

    openID = python_obj['openid']
    print  openID
    userIfor = models.userInfor.objects.filter(openID=openID)
    # 用户信息
    userDict = {'userID': 0}
    if len(userIfor) > 0:

        # userIfor =serializers.serialize("json",userIfor)
        userDict['userID'] = userIfor[0].pk
        return HttpResponse(json.dumps(userDict))
    else:
        # 如果没有先添加后获取
        dic = {'openID': openID}
        models.userInfor.objects.create(**dic)
        userIfor = models.userInfor.objects.filter(openID=openID)
        # userIfor =serializers.serialize("json",userIfor)
        userDict['userID'] = userIfor[0].pk
        return HttpResponse(json.dumps(userDict))


# 获取卡片cardType==1我创建的2我接收的
def getMyCardList(request):
    searchName = request.GET.get('searchName')
    if len(searchName) == 0:
        myCard = models.MyCard.objects.filter(userID=request.GET.get('userID'), cardType=request.GET.get('cardType'))
        myCard = serializers.serialize("json", myCard)
        return HttpResponse(myCard)
    else:
        # articlelist =models.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
        myCard = models.MyCard.objects.filter(userID=request.GET.get('userID'), cardType=request.GET.get('cardType')). \
            filter(Q(peopleName__icontains=searchName) | Q(phoneNum__icontains=searchName) | Q(
            companyName__icontains=searchName)
                   | Q(positionName__icontains=searchName) | Q(QQ__icontains=searchName) | Q(
            Email__icontains=searchName)
                   | Q(address__icontains=searchName))
        myCard = serializers.serialize("json", myCard)
        return HttpResponse(myCard)


# 获取卡片分享的卡片userID=1&myQrcodeID=cf5c613dfaf789c5db7fa93a04ebd66b 分享自己的还有二维码都是一样的
def getShareCard(request):
    userID = request.GET.get('userID')
    myQrcodeID = request.GET.get('myQrcodeID')
    myCardList = models.MyCard.objects.filter(userID=userID, qrcodeID=myQrcodeID, cardType=1)
    dict = {
    }
    if len(myCardList) > 0:
        dict['isExist'] = 1
        myCard = serializers.serialize("json", myCardList)
        dict['myCard'] = myCard
        return HttpResponse(json.dumps(dict))
    else:
        dict['isExist'] = 0
        return HttpResponse(json.dumps(dict))


def notypeTostr(noType, str1):
    tempfinal = []
    tempfinal.append(noType)
    tempfinal.append(str1)
    if None in tempfinal:
        tempfinal.remove(None)

    finaltext = ''.join(tempfinal)
    return finaltext


# 添加卡片
def addMyCard(request):
    m5 = hashlib.md5()
    fileTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    m5.update(notypeTostr(request.GET.get('userID'),fileTime))
    cardID = m5.hexdigest()
    # path = 'pages/acceptCard/acceptCard?userID=' + notypeTostr(request.GET.get('userID'), '') + '&myQrcodeID=1212'
    # return HttpResponse(path)
    qrModel = createQRcode(request.GET.get('userID'))
    dic = {
        'EnglishName': request.GET.get('EnglishName'),
        'cardID': cardID,
        'cardModelType': request.GET.get('cardModelType'),
        'createTime': time.strftime('%Y-%m-%d', time.localtime(time.time())),
        'cardType': request.GET.get('cardType'),
        'userID': request.GET.get('userID'),
        'createrID': request.GET.get('createrID'),
        'peopleName': request.GET.get('peopleName'),  # 默认微信昵称
        'phoneNum': request.GET.get('phoneNum'),
        'bgImgUrl': request.GET.get('bgImgUrl'),
        'logoImgUrl': request.GET.get('logoImgUrl'),  # 默认微信头像
        'companyName': request.GET.get('companyName'),
        'QQ': request.GET.get('QQ'),
        'Email': request.GET.get('Email'),
        'positionName': request.GET.get('positionName'),
        'address': request.GET.get('address'),
        'sharePeople': request.GET.get('sharePeople'),
        'qrcodeID': qrModel.myQrcodeID,
        'qrcodeimage': qrModel.qrcodeimage,
        'tagID': request.GET.get('tagID'),
        'Latitude': request.GET.get('Latitude'),
        'longitude': request.GET.get('longitude')
    }
    model = models.MyCard.objects.create(**dic)
    qrModel.isUsing = '1'
    qrModel.save()
    model.qrcodeModel = qrModel.toJSON()
    model.save()
    return HttpResponse('创建成功')


# 创建二维码
def createQRcode(userID):
    qrModel = models.qrcodeTable.objects.filter(userID=userID,isUsing='0')
    if len(qrModel) > 0:
        path = qrModel[0].path
        if path == 'myQrcodeID':
            qrModel.delete()
            createQRcode(userID)
        else:
            view_1.getQRCode(qrModel[0].path)
            return qrModel[0]

    else:
        m5 = hashlib.md5()
        fileTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        m5.update(notypeTostr(userID,'myQrcodeID' + fileTime))
        myQrcodeID = m5.hexdigest()
        path = 'pages/acceptCard/acceptCard?userID=' + notypeTostr(userID,'')+ '&myQrcodeID=' + myQrcodeID
        qrcodeimage = view_1.getQRCode(path)
        dic = {
            'path': path,
            'myQrcodeID': myQrcodeID,
            'userID': userID,
            'isUsing': '0',
            'qrcodeimage': qrcodeimage,
        }
        qrModel = models.qrcodeTable.objects.create(**dic)
        return qrModel


# 判断是否存在id
def ExistCard(request):
    cardID = request.GET.get('cardID'),
    userID = request.GET.get('userID')
    myCard = models.MyCard.objects.filter(userID=userID, cardID=cardID)
    dict = {
        'isExist': 0
    }
    if len(myCard) > 0:
        dict['isExist'] = 1
    else:
        dict['isExist'] = 0
    return HttpResponse(json.dumps(dict))  # 删除卡片pk userID


# 接收卡片
def acceptMyCard(request):
    userID = request.GET.get('userID')
    sharePeople = request.GET.get('sharePeople')
    pk = request.GET.get('pk')
    modelCard = models.MyCard.objects.filter(pk=pk)
    cardID = ''
    if len(modelCard) > 0:
        cardID = modelCard[0].cardID
    else:
        return HttpResponse('卡片不存在')
    myCard = models.MyCard.objects.filter(userID=userID, cardID=cardID)
    if len(myCard) > 0:

        return HttpResponse('已经存在')
    else:
        dic = model_to_dict(modelCard[0])
        del dic['id']
        dic['userID'] = userID
        dic['sharePeople'] = sharePeople
        dic['cardType'] = 2
        models.MyCard.objects.create(**dic)
        return HttpResponse('成功')  # 接收卡片pk userID


def deleteCard(request):
    myCard = models.MyCard.objects.filter(userID=request.GET.get('userID'), pk=request.GET.get('pk'))
    myQRcodeID = myCard[0].qrcodeID
    if len(myCard) > 0:
        QRCodeModelList = models.qrcodeTable.objects.filter(userID=request.GET.get('userID'), myQrcodeID=myQRcodeID)
        if len(QRCodeModelList) > 0:
            QRCodeModelList[0].isUsing = '0'
            QRCodeModelList[0].save()
        myCard.delete()
        return HttpResponse('删除成功')
    else:
        return HttpResponse('卡片不存在')


# 修改
def updateCard(request):
    m5 = hashlib.md5()
    fileTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    m5.update(request.GET.get('userID') + fileTime)
    cardID = m5.hexdigest()
    myCard = models.MyCard.objects.filter(userID=request.GET.get('userID'), pk=request.GET.get('pk'))
    if len(myCard) > 0:
        myCard[0].EnglishName = request.GET.get('EnglishName')
        myCard[0].cardID = cardID
        myCard[0].cardModelType = request.GET.get('cardModelType')
        myCard[0].peopleName = request.GET.get('peopleName')
        myCard[0].phoneNum = request.GET.get('phoneNum')
        myCard[0].bgImgUrl = request.GET.get('bgImgUrl')
        myCard[0].logoImgUrl = request.GET.get('logoImgUrl')
        myCard[0].companyName = request.GET.get('companyName')
        myCard[0].QQ = request.GET.get('QQ')
        myCard[0].Email = request.GET.get('Email')
        myCard[0].positionName = request.GET.get('positionName')
        myCard[0].address = request.GET.get('address')
        myCard[0].tagID = request.GET.get('tagID')
        myCard[0].Latitude = request.GET.get('Latitude')
        myCard[0].longitude = request.GET.get('longitude')
        myCard[0].save()
        myCard = models.MyCard.objects.filter(userID=request.GET.get('userID'), pk=request.GET.get('pk'))
        myCard = serializers.serialize("json", myCard)
        return HttpResponse(myCard)
    else:
        return HttpResponse('卡片不存在')


# 获取分享卡片
def getCard(request):
    myCard = models.MyCard.objects.filter(pk=request.GET.get('pk'))
    myCard = serializers.serialize("json", myCard)
    return HttpResponse(myCard)


# 添加卡片
def addSystemBgImage(request):
    dic = {
        'modelType': request.GET.get('modelType'),
        'modelPic': request.GET.get('modelPic'),
        'name': request.GET.get('name')
    }

    models.bgImgList.objects.create(**dic)
    return HttpResponse('成功')  # 删除卡片pk userID


def getSystemBgImage(request):
    modelType = request.GET.get('modelType')
    if len(modelType) > 0:
        myCard = models.bgImgList.objects.filter(modelType=request.GET.get('modelType'))
        myCard = serializers.serialize("json", myCard)
        return HttpResponse(myCard)
    else:
        myCard = models.bgImgList.objects.filter().all()
        myCard = serializers.serialize("json", myCard)
        return HttpResponse(myCard)


# 删除背景图
def deleteSystemBgImage(request):
    # myCard =models.MyCard.objects.filter(userID=request.GET.get('userID'),pk=request.GET.get('pk'))
    myCard = models.bgImgList.objects.filter(pk=request.GET.get('pk'))
    if len(myCard) > 0:
        myCard.delete()
        return HttpResponse('删除成功')
    else:
        return HttpResponse('卡片不存在')


# Create your views here.
class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
# 用户上传图片
def uploadImage(request):
    """
        method: POST
        api: /upload/
        """
    fp = request.FILES.get('file')
    userID = request.POST.get('userID')
    compress = request.POST.get('compress')
    response = {}
    if fp:
        src_fn = save_original_image(fp, userID, settings.UPLOAD_ROOT)
        # settings.HOST_NAME请根据自己的要求设置
        response['url'] = src_fn
    return JsonResponse(response)


UPLOAD_DIR_FORMAT = '%Y%m%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
UPLOAD_DIR_FORMAT = '%Y%m%d'
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'

from WEIMP import settings


def datetime_to_str(x=None, fmt=DATETIME_FORMAT):
    x = x if x else datetime.datetime.now()
    return x.strftime(fmt)


def date_to_str(x=None, fmt=DATE_FORMAT):
    return datetime_to_str(x, fmt)


def save_original_image(fp, userID, path):
    # subdir =datetime_to_str(datetime.date.today(),UPLOAD_DIR_FORMAT)
    # settings.UPLOAD_ROOT设置为UPLOAD_ROOT =os.path.join(BASE_DIR,'images')

    m5 = hashlib.md5()
    fileTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    m5.update(userID + fileTime)
    filename = m5.hexdigest()
    # path =os.path.join(settings.UPLOAD_ROOT,subdir)

    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, filename + '.jpg'), 'wb') as dst_fp:
        for chunk in fp.chunks():
            dst_fp.write(chunk)
    return filename + '.jpg'




#
# def compress_image(filename):
#     rear =filename[filename.rfind('.'):]
#     thumbnail_fn =filename.replace(rear,'-thumbnail' + rear)
#     image =Image.open(os.path.join(settings.BASE_DIR,filename))
#     image.thumbnail((128,128))
#     image.save(os.path.join(settings.BASE_DIR,thumbnail_fn),'JPEG')
#     return thumbnail_fn

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
# 上传系统背景
def upSystemBgImg(request):
    """
        method: POST
        api: /upload/
        """
    fp = request.FILES.get('file')
    userID = request.POST.get('userID')
    response = {}
    if fp:
        src_fn = save_original_image(fp, userID, settings.UPLOAD_SYSTEM_ROOT)
        # settings.HOST_NAME请根据自己的要求设置
        response['url'] = '%s' % (src_fn)

    return JsonResponse(response)
