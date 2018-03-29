from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^zhuce$',views.zhuceView.as_view()),
    url(r'^active/(.+)$',views.active),
    url(r'^login$',views.LoginView.as_view()),
    url(r'^exists$',views.exists),
    url(r'^info$',views.info),
    url(r'^video$',views.video),
    url(r'^logout$',views.logout_user),
    url(r'^chgpwd$',views.ChgpwdView.as_view()),
    url(r'^judge_pwd$',views.judge_pwd),
    url(r'^video_img$',views.video_img),
    url(r'^forgetPassword$',views.forgetPassword.as_view()),
    url(r'^check_email$',views.check_email),
    url(r'^ch_password/(.+)$',views.ch_password.as_view()),

]