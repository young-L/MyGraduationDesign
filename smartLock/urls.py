from django.conf.urls import url
from  . import views
urlpatterns=[
    url(r'^$',views.index),
    url(r'^123$',views.yy),
    url(r'^zhuce$',views.zhuce),
    url(r'^create$',views.chuangjian),
    url(r'^page_dl$',views.page_dl),
    url(r'^denglu$',views.denglu),
    url(r'cuowu',views.cuowu),
    url(r'^changePwd(\d+)$',views.page_changePwd),
]