from django.db import models
from datetime import datetime, time


# Create your models


class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    # age = models.IntegerField()
    datetime = models.CharField(max_length=32)


class Role(models.Model):
    position = models.CharField(max_length=16)


# 让上传的文件路径动态地与user的名字有关
def upload_to(instance, filename):  # 返回一个路径名即可。调用时会自动传入user实例和filename两个参数。函数名也不一定需要叫upload_to，只要传入此函数即可。
    return ''.join([instance.user.id, str(int(time.time())) + '_' + filename])


class User(models.Model):
    '''用户表'''

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    introduce = models.CharField(max_length=230, null=True, blank=True)

    avatar = models.ImageField(verbose_name='图片路径', null=True, blank=True,
                               default='/default.jpg')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'
