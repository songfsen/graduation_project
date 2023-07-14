import os

from django.shortcuts import render, HttpResponse, redirect
from .models import UserInfo, Role, User
import hashlib
from .myform import UserForm, RegisterForm, ForgetPwdForm, ResetPwdForm
from django.contrib import messages
from mysite import settings
import random
from django.core.mail import send_mail
from app01.models import Collection, Merchant


# Create your views here.


def orm(request):
    """测试orm操作表中数据"""
    # 1.新建数据
    # Role.objects.create(position='销售')
    # Role.objects.create(position='经理')
    # UserInfo.objects.create(name='sfs', password='123', age=21)
    # UserInfo.objects.create(name='lyf', password='123', age=22)

    # 2.删除数据
    # Role.objects.filter(id=4).delete()
    # Role.objects.all().delete()

    # 3.获取数据 得到queryset类型数据 [对象,对象,对象]
    # data_list = Role.objects.all()
    # for obj in data_list:
    #     print(obj.id, obj.position)
    # obj = Role.objects.filter(id=2).first()
    # print(obj.id, obj.position)

    return HttpResponse('orm操作成功！')


def info_list(request):
    """用户列表展示"""
    user_list = UserInfo.objects.all()

    return render(request, 'info_list.html', {'user_list': user_list})


# 添加 密码 MD5加密
def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index_1(request):
    # 通过session来获取登录用户的id
    user_id = request.session.get('user_id', None)
    user_name = request.session.get('user_name', None)
    return render(request, 'index_1.html', {'user_name': user_name})


def login_1(request):
    if request.session.get('is_login', None):
        return redirect('/app01/index/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    # session设置为已登录状态
                    request.session['is_login'] = True
                    request.session['identity'] = 'user'
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    # session登陆状态保存12小时
                    request.session.set_expiry(43200)
                    return redirect('/app01/index/')
                else:
                    messages.error(request, "密码不正确！请重新输入")
            except:
                messages.error(request, "用户不存在！请先注册")
        return render(request, 'login_1.html', locals())

    login_form = UserForm()
    return render(request, 'login_1.html', locals())


def register_1(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect('/app01/index/')
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                # message = "两次输入的密码不同！请重新填写"
                messages.error(request, "两次输入的密码不同！请重新填写")
                return render(request, 'register_1.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    # message = '用户已经存在，请重新选择用户名！'
                    messages.error(request, '用户已经存在，请重新选择用户名！')
                    return render(request, 'register_1.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    # message = '该邮箱地址已被注册，请使用别的邮箱！'
                    messages.error(request, '该邮箱地址已被注册，请使用别的邮箱！')
                    return render(request, 'register_1.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/blog/login_1/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'register_1.html', locals())


def logout_1(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect('/app01/index/')
    # 清空session缓存信息
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/blog/login_1/')


def personal_info_pre(request):
    # 通过session获取用户信息
    user_id = request.session.get('user_id', None)
    user_name = request.session.get('user_name', None)

    # 通过id查询用户相关信息
    user_obj = User.objects.filter(id=user_id).first()
    email = user_obj.email
    create_time = user_obj.c_time
    if user_obj.sex == 'female':
        sex = '女'
    else:
        sex = '男'
    avatar = user_obj.avatar
    phone = user_obj.phone
    introduce = user_obj.introduce
    if not user_obj.introduce:
        introduce = '暂无'

    return render(request, 'personal_info_pre.html', locals())


def personal_info(request):
    """用户个人信息"""
    # 通过session获取用户信息
    user_id = request.session.get('user_id', None)
    user_name = request.session.get('user_name', None)

    # 通过id查询用户相关信息
    user_obj = User.objects.filter(id=user_id).first()
    email = user_obj.email
    create_time = user_obj.c_time
    sex = user_obj.sex
    avatar = user_obj.avatar
    phone = user_obj.phone
    introduce = user_obj.introduce

    if request.method == "POST":
        # 获取用户对象
        user = User.objects.get(id=user_id)
        # 获取表单内容
        data = request.POST
        image = request.FILES.get('avatar')
        username = data.get("username")
        sex = data.get("sex")
        phone = data.get("phone")
        email = data.get("email")
        introduce = data.get("introduce")

        # 判断是否上传了头像
        if image:
            file_name, suffix = os.path.splitext(image.name)
            image.name = str(user_id) + create_time.strftime('%Y%m%d%H%M%S') + suffix
            if suffix.upper() not in ['.JPG', '.PNG', '.JPEG']:
                messages.error(request, '头像仅支持JPG、PNG、JPEG格式的文件')
            if user.avatar == image.name:
                path = os.path.join(settings.BASE_DIR, 'media', str(user.avatar))
                os.remove(path)
            # 如果未上传头像则保存
            user.avatar = image

        # 判断用户名是否已存在（用户名是不允许重复的）
        judge_user = User.objects.filter(name=username).first()
        if judge_user:
            if user_id == judge_user.id:
                pass
            else:
                print('chongfu')
                messages.error(request, '用户名重复！请重新填写用户名')
                return redirect('/blog/personal_info/')
        else:
            user.name = username
        # 修改其它信息
        user.email = email
        user.phone = phone
        user.introduce = introduce
        user.sex = sex
        # 保存信息
        user.save()
        messages.success(request, '修改成功!')

        return redirect('/blog/personal_info_pre/')

    return render(request, 'personal_info.html', locals())


def find_password(request):
    """ 通过邮箱验证码找回密码 """
    # 生成数字混和字母的五位验证码
    checkcode = ''
    for i in range(5):
        current = random.randrange(0, 5)
        if current != i:  # !=  不等于 - 比较两个对象是否不相等
            temp = chr(random.randint(65, 90))
        else:
            temp = random.randint(0, 9)
        checkcode += str(temp)

    # 获取用户输入的注册邮箱
    form = ForgetPwdForm()
    if request.method == "POST":
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            exists = User.objects.filter(email=email).exists()
            # 检验注册邮箱是否存在
            if exists:
                # 发送邮件
                send_mail('验证消息', f'您好！验证码为：{checkcode}，请勿随意发送给他人', settings.DEFAULT_FROM_EMAIL, [email])
                # 将验证码缓存至session中 300s后过期
                request.session['check_code'] = checkcode
                request.session['check_email'] = email
                request.session.set_expiry(300)
                messages.success(request, '验证码发送成功，请及时查看邮件！')
                return redirect('/blog/reset_password/')
            else:
                messages.error(request, '对不起，请输入您的注册邮箱')
                return redirect('/blog/find_password/')
    return render(request, 'find_password.html', {'form': form})


def reset_password(request):
    form = ResetPwdForm()
    session_check_code = request.session['check_code']
    session_check_email = request.session['check_email']
    # 获取表单内容
    if request.method == "POST":
        form = ResetPwdForm(request.POST)
        # 校验数据是否合法
        if form.is_valid():
            new_pwd = form.cleaned_data.get('new_pwd')
            confirm_pwd = form.cleaned_data.get('confirm_pwd')
            check_code = form.cleaned_data.get('check_code')
            # 判断密码是否相同
            if new_pwd == confirm_pwd:
                # 判断验证码是否相同
                if str.upper(check_code) == session_check_code:
                    # 通过邮箱获取用户信息
                    user = User.objects.get(email=session_check_email)
                    # 将新密码md5加密后保存与数据库
                    user.password = hash_code(new_pwd)
                    messages.success(request, '密码修改成功！请登录')
                    return redirect('/blog/login_1/')
                else:
                    messages.error(request, '验证码错误！请重试')
                    return redirect('/blog/reset_password/')
            else:
                messages.error(request, '两次输入的密码不一致，请重新输入！')
                return redirect('/blog/reset_password/')
    return render(request, 'reset_password.html', {'form': form})



