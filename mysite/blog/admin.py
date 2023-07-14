from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.User)

admin.site.site_header = '商家推荐系统'  # 设置header 管理后台
admin.site.site_title = '商家推荐系统'  # 设置title 管理后台
admin.site.index_title = '商家推荐系统'
