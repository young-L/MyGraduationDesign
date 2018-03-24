from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # 添加时间
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    # 最近修改时间
    update_date = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    # 逻辑删除
    isDelete = models.BooleanField(default=False, verbose_name='逻辑删除')
    class Meta:  # ttsx-->dailyfresh-->df
        db_table = 'user'


