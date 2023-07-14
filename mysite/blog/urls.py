from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # orm操作表中数据
    path('orm/', views.orm),

    # 用户列表
    path('info/list/', views.info_list),

    #########################################
    # 登录
    path('login_1/', views.login_1),
    # 注册
    path('register_1/', views.register_1),
    # 注销
    path('logout_1/', views.logout_1),
    # 密码找回
    path('find_password/', views.find_password, name='find_password'),
    # 密码重置
    path('reset_password/', views.reset_password, name='reset_password'),
    # 推荐系统主页
    path('index_1/', views.index_1),
    # 个人信息主页
    path('personal_info_pre/', views.personal_info_pre),
    # 个人信息修改页面
    path('personal_info/', views.personal_info),


]
