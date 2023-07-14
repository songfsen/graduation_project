import os
import random

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse, redirect
from .myforms import MerchantForm, MerchantCheck, MerchantEmail
from .models import Merchant, Comment, Collection
from blog.models import User
from mysite import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.


def index(request):
    # 获取当前页数
    current_page = request.GET.get('page')
    # 拿到商家数据
    # merchants = Merchant.objects.filter().all()
    merchants = Merchant.objects.all().order_by('-collect_num')
    merchant_list = []
    for i in merchants:
        merchant_list.append(i)
    # 分页管理器
    paginator = Paginator(merchant_list, 8)
    try:
        # 拿到当前页面对象列表数据
        contacts = paginator.page(current_page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'contacts': contacts})


def merchant_entry(request):
    return render(request, 'merchant_entry.html')


def merchant_register(request):
    form = MerchantForm()
    if request.method == 'POST':
        # 生成数字混和字母的五位验证码
        checkcode = ''
        for i in range(5):
            current = random.randrange(0, 5)
            if current != i:  # !=  不等于 - 比较两个对象是否不相等
                temp = chr(random.randint(65, 90))
            else:
                temp = random.randint(0, 9)
            checkcode += str(temp)

        form = MerchantForm(request.POST)
        if form.is_valid():
            shop_name = form.cleaned_data.get('shop_name')
            location = form.cleaned_data.get('location')
            email = form.cleaned_data.get('email')
            is_email_exist = Merchant.objects.filter(email=email).exists()
            if is_email_exist:
                messages.error(request, '该邮箱已被注册，请切换另外的邮箱')
                return redirect('/app01/merchant/register/')
            phone = form.cleaned_data.get('phone')

            request.session['shop_name'] = shop_name
            request.session['shop_location'] = location
            request.session['shop_email'] = email
            request.session['shop_phone'] = phone
            request.session['shop_check_code'] = checkcode
            request.session.set_expiry(600)
            # todo
            # send_mail('验证消息', f'您好！验证码为：{checkcode}，请勿随意发送给他人', settings.DEFAULT_FROM_EMAIL, [email])
            print(checkcode)
            messages.success(request, '验证码已发送至邮箱，有效期10分钟，请注意查收。')
            return redirect('/app01/merchant/register/check/')

    return render(request, 'merchant_register.html', {'form': form})


def merchant_register_check(request):
    form = MerchantCheck()
    shop_name = request.session['shop_name']
    shop_location = request.session['shop_location']
    shop_email = request.session['shop_email']
    shop_phone = request.session['shop_phone']
    check_code = request.session['shop_check_code']
    # print(shop_name)
    if request.method == 'POST':
        form = MerchantCheck(request.POST)
        if form.is_valid():
            form_check_code = form.cleaned_data.get('check_code')
            if check_code == str.upper(form_check_code):
                new_merchant = Merchant.objects.create()
                new_merchant.shop_name = shop_name
                new_merchant.location = shop_location
                new_merchant.email = shop_email
                new_merchant.phone = shop_phone
                new_merchant.save()
                messages.success(request, '注册成功！请登录')
                return redirect('/app01/index/')
            else:
                messages.error(request, '验证码错误，请重新输入！')
                return redirect('/app01/merchant/register/check/')
    return render(request, 'merchant_register_check.html', {'form': form})


def merchant_login(request):
    form = MerchantEmail()
    # 生成数字混和字母的五位验证码
    checkcode = ''
    for i in range(5):
        current = random.randrange(0, 5)
        if current != i:  # !=  不等于 - 比较两个对象是否不相等
            temp = chr(random.randint(65, 90))
        else:
            temp = random.randint(0, 9)
        checkcode += str(temp)
    if request.method == 'POST':
        form = MerchantEmail(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # 判断是否有该邮箱注册过
            is_email_exist = Merchant.objects.filter(email=email).exists()
            if not is_email_exist:
                messages.error(request, '该邮箱并未注册过，请重试')
                return redirect('/app01/merchant/login/')

            request.session['merchant_email'] = email
            request.session['merchant_code'] = checkcode
            request.session.set_expiry(300)
            # todo
            # send_mail('验证消息', f'您好！验证码为：{checkcode}，请勿随意发送给他人', settings.DEFAULT_FROM_EMAIL, [email])
            print(checkcode)
            messages.success(request, '验证码已发送至邮箱，有效期5分钟，请注意查收。')
            return redirect('/app01/merchant/login/check/')
    return render(request, 'merchant_login.html', {'form': form})


def merchant_login_check(request):
    form = MerchantCheck()
    if request.method == 'POST':
        form = MerchantCheck(request.POST)
        if form.is_valid():
            session_code = request.session['merchant_code']
            session_email = request.session['merchant_email']
            post_code = form.cleaned_data.get('check_code')

            merchant = Merchant.objects.get(email=session_email)
            if str.upper(post_code) == session_code:
                request.session['is_login'] = True
                request.session['identity'] = 'merchant'
                request.session['merchant_id'] = merchant.id
                request.session['merchant_name'] = merchant.shop_name
                request.session.set_expiry(43200)
                # 跳转到商户信息页面
                messages.success(request, '登录成功，请继续完善店铺信息')
                return redirect('/app01/merchant/info/')
            else:
                messages.error(request, '验证码错误，请重新输入！')
                return redirect('/app01/merchant/login/check/')
    return render(request, 'merchant_login_check.html', {'form': form})


def merchant_info(request):
    identity = request.session.get('identity', None)
    # 用户访问
    if identity == 'user':
        merchant_id = request.GET.get('id')
        if merchant_id:
            merchant_id = int(merchant_id)
            print(merchant_id)
    # 商家自己登录访问
    if identity == 'merchant':
        merchant_id = int(request.session.get('merchant_id', None))
    # 通过session 获取用户信息
    # merchant_id = request.session['merchant_id']
    merchant = Merchant.objects.get(id=merchant_id)
    # 属性
    name = merchant.shop_name
    location = merchant.location
    phone_number = merchant.phone_number
    average_price = merchant.average_price
    recommend = merchant.recommend
    picture = merchant.picture
    average_score = merchant.average_score
    environment_score = merchant.environment_score
    server_score = merchant.server_score
    taste_score = merchant.taste_score
    business_hours = merchant.business_hours
    special = merchant.special
    collect_num = merchant.collect_num

    # 仅允许用户进行评论
    user_or_merchant = request.session.get('identity', None)

    # 获取该商家的评论信息,根据时间排序，获取最近的
    comment_queryset = Comment.objects.filter(commented_merchant=merchant_id).order_by('-publish_time')
    # print(comment_queryset, type(comment_queryset))
    # todo
    if request.method == 'POST':
        # 获取post数据
        data = request.POST
        content = data.get("content")
        taste = data.get("taste")
        server = data.get("server")
        environment = data.get("environment")
        average_price = data.get("average_price")
        # print(content, average_price)
        user_id = request.session.get('user_id')
        # print(user_id)
        user = User.objects.get(id=user_id)
        # 创建新记录保存
        new_comment = Comment.objects.create()
        new_comment.comment_auther = user
        new_comment.commented_merchant = merchant
        new_comment.comment_content = content
        new_comment.taste_score = int(taste)
        new_comment.server_score = int(server)
        new_comment.environment_score = int(environment)
        # 保存
        new_comment.save()
        return render(request, 'merchant_info.html', locals())

    return render(request, 'merchant_info.html', locals())


def merchant_info_edit(request):
    if request.session.get('identity', None) == 'merchant':
        # 通过session获取商家记录
        merchant_id = int(request.session.get('merchant_id'))
        merchant_obj = Merchant.objects.get(id=merchant_id)
        # 获取商家信息
        shop_name = merchant_obj.shop_name
        location = merchant_obj.location
        email = merchant_obj.email
        phone_number = merchant_obj.phone_number
        type = merchant_obj.type
        recommend = merchant_obj.recommend
        business_hours = merchant_obj.business_hours
        special = merchant_obj.special
        picture = merchant_obj.picture
        # 商家用户提交信息
        if request.method == 'POST':
            # 获取商家obj
            merchant_obj = Merchant.objects.get(id=merchant_id)
            # 获取post提交数据
            data = request.POST
            picture = request.FILES.get('picture')
            shop_name = data.get('shop_name')
            location = data.get('location')
            # email = data.get('email')
            phone_number = data.get('phone_number')
            type = data.get('type')
            recommend = data.get('recommend')
            business_hours = data.get('business_hours')
            special = data.get('special')

            # 判断是否上传了新头像
            if picture:
                file_name, suffix = os.path.splitext(picture.name)
                picture.name = str(merchant_id) + str(shop_name) + suffix
                if suffix.upper() not in ['.JPG', '.PNG', '.JPEG']:
                    messages.error(request, '头像仅支持JPG、PNG、JPEG格式的文件')
                if merchant_obj.picture == picture.name:
                    path = os.path.join(settings.BASE_DIR, 'media', str(merchant_obj.picture))
                    os.remove(path)
                # 如果未上传头像则保存
                merchant_obj.picture = picture
            # 保存其他属性信息
            merchant_obj.shop_name = shop_name
            merchant_obj.location = location
            merchant_obj.phone_number = phone_number
            merchant_obj.type = type
            merchant_obj.recommend = recommend
            merchant_obj.business_hours = business_hours
            merchant_obj.special = special
            # 保存
            merchant_obj.save()
            messages.success(request, '修改成功')
            return redirect('/app01/merchant/info/')

    return render(request, 'merchant_info_edit.html', locals())


def merchant_collect(request):
    """收藏商家"""
    is_login = request.session.get('is_login', None)
    if is_login:
        # 获取用户id
        user_id = request.session['user_id']
        # 获取用户id
        merchant_id = int(request.GET.get('merchant_id'))
        # 查询是否已收藏
        is_exist = Collection.objects.filter(collect_user=user_id, collected_merchant=merchant_id).exists()
        if is_exist:
            messages.error(request, '你已收藏过该商家')
            return redirect(f'/app01/merchant/info/?id={merchant_id}')
        # 获取用户对象
        user = User.objects.get(id=user_id)
        # 获取商家对象
        merchant = Merchant.objects.get(id=merchant_id)
        # 创建记录
        new_collection = Collection.objects.create()
        new_collection.collect_user = user
        new_collection.collected_merchant = merchant
        new_collection.save()
        # 返回原来界面
        messages.success(request, '收藏成功！')
        return redirect(f'/app01/merchant/info/?id={merchant_id}')
    else:
        merchant_id = request.GET.get('merchant_id')
        messages.error(request, '请先登录后再收藏')
        return redirect(f'/app01/merchant/info/?id={merchant_id}')


def cancel_collect(request):
    """取消收藏"""
    user_id = int(request.session.get('user_id', None))
    merchant_id = int(request.GET.get('merchant_id'))
    Collection.objects.get(collected_merchant=merchant_id, collect_user=user_id).delete()
    messages.success(request, '取消收藏成功')
    return redirect('/app01/user/collections/')


def personal_collections(request):
    """用户收藏"""
    # 通过session获取用户id
    user_id = request.session.get('user_id', None)
    # 通过url获取当前页数
    current_page = request.GET.get('page')
    # 通过user_id获取到collection表中记录 (按照收藏的先后顺序)
    collection_queryset = Collection.objects.filter(collect_user=user_id).order_by('-collect_time')
    # 将该用户收藏的商家添加到列表
    merchant_obj_list = []
    for record in collection_queryset:
        merchant_obj_list.append(record.collected_merchant)
    print(merchant_obj_list)
    # 类似index页面分页
    # 分页管理器
    paginator = Paginator(merchant_obj_list, 3)
    try:
        # 拿到当前页面对象列表数据
        contacts = paginator.page(current_page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'personal_collections.html', {'contacts': contacts})


import pandas as pd


# todo
def insert(request):
    # (r'D:\八爪鱼下载\【成都火锅】推荐,火锅排行_大全_攻略-大众点评网.xlsx', usecols='A,G,I,K,M,O,Q')
    # D:\八爪鱼下载\咖啡.xlsx  'A,F,H,J,L,N,P'
    df = pd.read_excel(r'D:\八爪鱼下载\datacopy2.xlsx', usecols='C,D,H,J,K,L,M')
    for index, row in df.iterrows():
        type = str(row[0])
        shop_name = str(row[1])
        try:
            average_price = row[2].split('￥')[1]
            average_price = int(average_price)
        except:
            average_price = random.randint(10, 130)

        location = str(row[3])

        recommend1 = row[4]
        recommend2 = row[5]
        recommend3 = row[6]
        if recommend1 and recommend2 and recommend3:
            recommend = str(recommend1) + ',' + str(recommend2) + ',' + str(recommend3)
        else:
            recommend = None
        collect_num = int(random.randint(1, 1000))

        email_pre = ''
        for i in range(6):
            num = random.randint(1, 10)
            email_pre = email_pre + str(num)
        email = email_pre + '@qq.com'

        merchant_obj = Merchant.objects.create()
        merchant_obj.shop_name = shop_name
        merchant_obj.email = email
        merchant_obj.type = type
        merchant_obj.location = location
        merchant_obj.collect_num = collect_num
        merchant_obj.average_price = average_price
        merchant_obj.recommend = recommend

        merchant_obj.save()

    return redirect('/app01/index/')


import numpy as np


def all_collections(request):
    # 所有收藏记录
    collections = Collection.objects.all()
    # print(collections)
    collection_list = []
    for record in collections:
        list1 = []
        # 用户id
        list1.append(record.collect_user.id)
        # 被收藏商家id
        list1.append(record.collected_merchant.id)

        collection_list.append(list1)

    # print(collection_list)

    # 单独构建每个用户的收藏列表
    # 获取二维数组第一个元素即用户id
    collection_list_array = np.array(collection_list)
    user_id_list = collection_list_array[:, 0]
    merchant_id_list = collection_list_array[:, 1]
    # print(user_id_list)
    # 用户id列表去重
    user_id_unique = list(set(user_id_list))
    # print(user_id_unique)
    # 商家id列表去重排序
    merchant_id_unique = list(set(merchant_id_list))
    merchant_id_unique = sorted(merchant_id_unique)
    # print(merchant_id_unique)

    # 循环构建 [user,merchant1,merchant2,merchant3,merchant4,merchant5.....]
    user_merchant_lists = []
    for i in user_id_unique:
        user_merchant_list = [i]
        for j in collection_list:
            if j[0] == i:
                user_merchant_list.append(j[1])
        # print(user_merchant_list)
        user_merchant_lists.append(user_merchant_list)
    print('用户收藏列表')
    print(user_merchant_lists)

    # 构建收藏矩阵
    columns = len(merchant_id_unique)  # 列数
    rows = len(user_id_unique)  # 行数
    x = np.zeros((rows, columns))  # 生成rows/columns全0矩阵
    merchant_id_unique = np.array(merchant_id_unique)
    x = np.insert(x, 0, merchant_id_unique, axis=0)  # 将商家列表插入矩阵
    # print('矩阵')
    # print(x)

    base_rows = 1
    for i in user_merchant_lists:
        for j in i[1:]:  # 去除掉user_id开始循环
            location_element = np.argwhere(x == j)  # 找到商家位置
            next_rows = location_element[0][0] + base_rows  # 用户所在行数
            next_columns = location_element[0][1]  # 商家所在列数
            x[next_rows][next_columns] = 1  # 用户行数商家列数置为1
            # print(location_element)
        base_rows = base_rows + 1
    # print('收藏矩阵')
    # print(x)

    # 登录用户id
    login_user_id = request.session['user_id']
    # print(login_user_id)
    # 初始位置
    the_user_position = 1
    for i in user_merchant_lists:
        if i[0] == login_user_id:
            the_user_position += 1
            break
    # print(f'用户收藏记录位于收藏矩阵第{the_user_position + 1}行')

    # 从用户列表中删除该用户
    user_id_unique.pop(the_user_position - 1)
    # print(user_id_unique)

    # 将收藏矩阵从第三行取出和去除
    login_user_array = x[the_user_position]  # 取出
    # print(login_user_array)
    x = np.delete(x, the_user_position, axis=0)  # 删除
    # print('用户收藏矩阵')
    # print(x)

    # 计算其它用户与该用户的相似度
    similarty = []
    for i in x[1:]:
        cos_sim = i.dot(login_user_array) / (np.linalg.norm(i) * np.linalg.norm(login_user_array))
        similarty.append(cos_sim)
    # print('相似度列表')
    # print(similarty)

    # np.set_printoptions(linewidth=400,suppress=True)
    userid_similarty_array = np.array([user_id_unique, similarty])
    # print('用户相似度')
    # print(userid_similarty_array)

    return redirect('/app01/index/')
