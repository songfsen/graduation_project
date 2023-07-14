from django.db import models
from blog.models import User


# Create your models here.

class Merchant(models.Model):
    """商户表"""
    shop_name = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    type = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=64)
    average_price = models.IntegerField(verbose_name='均价', null=True, blank=True)
    recommend = models.CharField(max_length=128, null=True, blank=True)

    picture = models.ImageField(verbose_name='商户头像', null=True, blank=True, default='/merchant_default.jpg')
    create_time = models.DateTimeField(auto_now_add=True)

    average_score = models.FloatField(verbose_name='平均评分', null=True, blank=True, )
    environment_score = models.FloatField(verbose_name='环境评分', null=True, blank=True, )
    server_score = models.FloatField(verbose_name='服务评分', null=True, blank=True, )
    taste_score = models.FloatField(verbose_name='味道评分', null=True, blank=True, )

    business_hours = models.CharField(max_length=128, verbose_name='营业时间')

    special = models.CharField(max_length=128, verbose_name='特色', null=True, blank=True)

    collect_num = models.IntegerField(verbose_name="收藏人数", null=True, blank=True)

    def __str__(self):
        return self.shop_name

    class Meta:
        ordering = ['create_time']
        verbose_name = '商家'
        verbose_name_plural = '商家'


class Comment(models.Model):
    '''评论表'''
    comment_auther = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='评论者', null=True, blank=True)
    commented_merchant = models.ForeignKey(to=Merchant, on_delete=models.CASCADE, verbose_name='被评论商家', null=True,
                                           blank=True)

    comment_content = models.CharField(max_length=255, verbose_name='评论内容')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    score = (
        ('1', '1分'),
        ('2', '2分'),
        ('3', '3分'),
        ('4', '4分'),
        ('5', '5分'),
    )
    taste_score = models.CharField(max_length=32, verbose_name='味道', choices=score, null=True, blank=True)
    server_score = models.CharField(max_length=32, verbose_name='服务', choices=score, null=True, blank=True)
    environment_score = models.CharField(max_length=32, verbose_name='环境', choices=score, null=True, blank=True)

    comment_picture_one = models.ImageField(verbose_name='图片评论1', null=True, blank=True)
    comment_picture_second = models.ImageField(verbose_name='图片评论2', null=True, blank=True)
    comment_picture_third = models.ImageField(verbose_name='图片评论3', null=True, blank=True)

    def __str__(self):
        return self.commented_merchant.shop_name + '/' + self.comment_auther.name + '/' + self.publish_time.strftime(
            '%Y-%m-%d %H:%M:%S')

    class Meta:
        ordering = ['publish_time']
        verbose_name = '评论'
        verbose_name_plural = '评论'


class Collection(models.Model):
    collected_merchant = models.ForeignKey(to=Merchant, on_delete=models.CASCADE, verbose_name='被收藏商家', null=True,
                                           blank=True)
    collect_user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='收藏用户', null=True, blank=True)

    collect_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    def __str__(self):
        return self.collect_user.name + '/' + self.collected_merchant.shop_name + '/' + self.collect_time.strftime(
            '%Y-%m-%d %H:%M:%S')

    class Meta:
        ordering = ['collect_time']
        verbose_name = '收藏'
        verbose_name_plural = '收藏'

