# coding=utf-8
from django.conf.urls import url


from WeiMpian import views
from WeiMpian import view_1
from WeiMpian import view_2
from  WEIMP import settings

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^login$', views.login),
    url(r'^getMyCardList$', views.getMyCardList),
    url(r'^addMyCard$', views.addMyCard),
    url(r'^deleteCard$', views.deleteCard),
    url(r'^updateCard$', views.updateCard),
    url(r'^getCard$', views.getCard),
    url(r'^acceptMyCard$', views.acceptMyCard),
    url(r'^ExistCard$', views.ExistCard),
    url(r'^uploadImage', views.uploadImage),
    url(r'^addSystemBgImage', views.addSystemBgImage),
    url(r'^getSystemBgImage', views.getSystemBgImage),
    url(r'^deleteSystemBgImage', views.deleteSystemBgImage),
    url(r'^upSystemBgImg', views.upSystemBgImg),
    # 获取二维码
    # url(r'^getQRCode', view_1.getQRCode),getShareCard 获取分享的或者扫描二维码的卡片
    url(r'^getShareCard', views.getShareCard),

    # 标签功能
    url(r'^addTag', view_2.addTag),
    url(r'^updateTag', view_2.updateTag),
    url(r'^deleteTag', view_2.deleteTag),
    url(r'^getTagList', view_2.getTagList),
    url(r'^getMPKcondition', view_1.getMPKcondition),
    # url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root':'/home/anna/Documents/django_py/showImg/static'}),getMPKcondition

    # addMyCardlogin updateCard upload_view upload_file ExistCard uploadImage addSystemBgImage getSystemBgImage deleteSystemBgImage
    #
    # url(r'detail/([0-9]+)$', views.get_xx_tab),
    #
    # url(r'delete/([0-9]+)$', views.delete_xx_tab),
    #
    # url(r'update/([0-9]+)$', views.update_xx_tab),
    #
    # url(r'add/$', views.add_xx_tab),

]
