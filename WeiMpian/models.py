# coding=utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.




class userInfor(models.Model):
    openID = models.CharField(max_length=100, default='openID')


class MyCard(models.Model):
    cardID = models.CharField(max_length=100, default='cardID')
    cardType = models.CharField(max_length=100, default='cardType')
    userID = models.CharField(max_length=100, default='userID')
    createrID = models.CharField(max_length=100, default='createrID')
    peopleName = models.CharField(max_length=100, default='peopleName')
    phoneNum = models.CharField(max_length=100, default='phoneNum')
    createTime = models.CharField(max_length=100, default='createTime')
    cardModelType = models.CharField(max_length=100, default='cardModelType')
    bgImgUrl = models.CharField(max_length=100, default='bgImgUrl')
    logoImgUrl = models.CharField(max_length=1000, default='logoImgUrl')
    companyName = models.CharField(max_length=32, default='companyName')
    QQ = models.CharField(max_length=100, default='QQ')
    Email = models.CharField(max_length=100, default='Email')
    positionName = models.CharField(max_length=100, default='positionName')
    address = models.CharField(max_length=100, default='positionName')
    sharePeople = models.CharField(max_length=100, default='sharePeople')
    EnglishName = models.CharField(max_length=100, default='EnglishName')

    qrcodeID = models.CharField(max_length=100, default='qrcodeID')
    qrcodeimage = models.CharField(max_length=100, default='qrcodeimage')
    qrcodeModel = models.CharField(max_length=1000, default='qrcodeModel', null=True)

    # 经纬度
    Latitude = models.CharField(max_length=1000, default='Latitude', null=True)
    longitude = models.CharField(max_length=1000, default='longitude', null=True)

    tagID = models.CharField(max_length=1000, default='', null=True)

    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))


class bgImgList(models.Model):
    modelType = models.CharField(max_length=100, default='modelType')
    modelPic = models.CharField(max_length=100, default='modelPic')
    name = models.CharField(max_length=1000, default='', null=True)

class qrcodeTable(models.Model):
    path = models.CharField(max_length=100, default='myQrcodeID')
    myQrcodeID = models.CharField(max_length=100, default='myQrcodeID')
    userID = models.CharField(max_length=100, default='userID')
    isUsing = models.CharField(max_length=100, default='isUsing')
    qrcodeimage = models.CharField(max_length=100, default='qrcodeimage')
    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))



class tagTable(models.Model):
    value = models.CharField(max_length=1000, default='', null=True)
    tagID = models.CharField(max_length=1000, default='', null=True)
    price = models.CharField(max_length=1000, default='0', null=True)