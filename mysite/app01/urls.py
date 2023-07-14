from django.contrib import admin
from django.urls import path, include
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 主页
    path('index/', views.index),
    # 商户入驻
    path('merchant/entry/', views.merchant_entry),
    # 商户注册
    path('merchant/register/', views.merchant_register),
    # 商户注册邮箱验证
    path('merchant/register/check/', views.merchant_register_check),
    # 商户登录
    path('merchant/login/', views.merchant_login),
    # 商户登录验证
    path('merchant/login/check/', views.merchant_login_check),
    # 商户信息
    path('merchant/info/', views.merchant_info),
    # 商户信息编辑
    path('merchant/info/edit/', views.merchant_info_edit),
    # 收藏商家
    path('merchant/collect/', views.merchant_collect),
    # 取消收藏
    path('cancel/collect/', views.cancel_collect),
    # 收藏记录
    path('user/collections/', views.personal_collections),





    # todo 插入
    path('insert/', views.insert),
    path('all/collections/', views.all_collections),




]
