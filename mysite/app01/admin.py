from django.contrib import admin
from .models import Merchant, Comment, Collection

# Register your models here.


# 添加商家模型
admin.site.register(Merchant)
# 添加评论模型
admin.site.register(Comment)
# 添加收藏模型
admin.site.register(Collection)
