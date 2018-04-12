import os
import socket

from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views.generic import View
import re
from MyGraduationWork import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from . import Vdemo
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request,'index.html')

class zhuceView(View):
    def get(self, request):
        return render(request, 'zhuce.html',{'title':'注册'})

    def post(self, request):
        # 接收数据
        dict = request.POST
        uname = dict.get('user_name')
        upwd = dict.get('pwd')
        cpwd = dict.get('cpwd')
        uemail = dict.get('email')


        # 判断数据是否填写完整
        if not all([uname, upwd, cpwd, uemail]):
            return render(request, 'zhuce.html', {'err_msg': '请将信息填写完整'})

        # 用户错误提示的数据
        context = {
            'uname': uname,
            'upwd': upwd,
            'cpwd': cpwd,
            'email': uemail,
            'err_msg': '',
            'title':'注册处理'
        }

        # 判断两次密码是否一致
        if upwd != cpwd:
            context['err_msg'] = '两次密码不一致'
            return render(request, 'zhuce.html', context)

        # 判断用户名是否存在
        if models.User.objects.filter(username=uname).count() > 0:
            context['err_msg'] = '用户名已经存在'
            return render(request, 'zhuce.html', context)

        # 判断邮箱格式是否正确
        if not re.match(r'[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}', uemail):
            context['err_msg'] = '邮箱格式不正确'
            return render(request, 'zhuce.html', context)

        # 判断邮箱是否存在
        # if User.objects.filter(email=uemail).count() > 0:
        #     context['err_msg'] = '邮箱已经存在'
        #     return render(request, 'register.html', context)

        # 处理（创建用户对象）
        user = models.User.objects.create_user(uname, '', upwd)
        # 稍候进行邮件激发，或许账户不被激活
        user.is_active = False
        user.save()

        # 将账号信息进行加密
        serializer = Serializer(settings.SECRET_KEY, 60 * 60 * 2)
        value = serializer.dumps({'id': user.id,'email':uemail})  # 返回bytes
        value = value.decode()  # 转成字符串，用于拼接地址

        # 向用户发送邮件
        # msg='<a href="http://127.0.0.1:8000/user/active/%d">点击激活</a>'%user.id
        msg = '<a href="http://127.0.0.1:8000/active/%s">点击激活</a>' % value
        send_mail('smartLock账户激活', '', settings.EMAIL_FROM, [uemail], html_message=msg)



        # 给出响应
        return HttpResponse('请在两个小时内前往邮箱，激活账户')


def active(request, value):
    serializer = Serializer(settings.SECRET_KEY)
    try:
        # 解析用户编号
        dict = serializer.loads(value)
        userid = dict.get('id')
        # 激活账户
        user = models.User.objects.get(pk=userid)
        user.is_active = True
        user.email = dict.get('email')
        user.save()

        # 转向登录页面
        return redirect('/login')
    except SignatureExpired as e:
        return HttpResponse('对不起，激活链接已经过期')

def exists(request):
    '判断用户名是否存在'
    uname=request.GET.get('uname')
    if uname is not None:
        #查询用户名是否存在
        result=models.User.objects.filter(username=uname).count()
    return JsonResponse({'result':result})

def check_email(request):
    '判断邮箱是否存在'
    uemail = request.GET.get('uemail')
    if uemail is not None:
        result = models.User.objects.filter(email=uemail).count()
    return JsonResponse({'result':result})

class LoginView(View):
    def get(self,request):
        uname=request.COOKIES.get('uname','')
        return render(request,'login.html',{'title':'登录','uname':uname})
    def post(self,request):
        #接收数据
        dict=request.POST
        uname=dict.get('username')
        pwd=dict.get('pwd')
        remember=dict.get('remember')

        #构造返回值
        context={
            'title':'登录处理',
            'uname':uname,
            'pwd':pwd,
            'err_msg': '请填写完成信息'
        }

        #验证是否填写数据
        if not all([uname,pwd]):
            return render(request,'login.html',context)

        #验证用户名、密码是否正确
        user=authenticate(username=uname,password=pwd)
        if user is None:
            context['err_msg']='用户名或密码错误'
            return render(request,'login.html',context)

        #判断用户是否激活
        if not user.is_active:
            context['err_msg']='请到邮箱中激活账户'
            return render(request,'login.html',context)

        #记录状态
        login(request,user)

        response=redirect('/info')

        next_page = request.GET.get('next')

        #是否记住用户名
        if remember is not None:
            response.set_cookie('uname',uname,expires=60*60*24*7)
        else:
            response.delete_cookie('uname')

        # 设置socket连接
        # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
        # server_socket.connect(('192.168.0.100', 7999));
        # response.set_cookie('server_socket',server_socket,expires=60*60*24*7)

        if next_page:
            return redirect(next_page)
        else:
            return response


@login_required
def info(request):
    return render(request,'info.html')

@login_required
def video(request):
    # 视频
    # server_socket = request.COOKIES.get('server_socket')
    # print(server_socket)
    # Vdemo.recv_image(server_socket)

    # 修改控制图片传输文件的值
    with open(settings.VIDEO_SWITCH_URL, 'w') as f:
        f.write('1')
    Vdemo.recv_image()
    return render(request,'video.html')

def logout_user(request):
    response = redirect('/')
    response.delete_cookie('server_socket')
    logout(request)
    return response

# 登陆状态检测
class LoginRequireMixin(object):
    @classmethod
    def as_view(cls):
        view = super().as_view()
        return login_required(view)

def judge_pwd(request):
    '判断密码是否正确'
    password = request.GET.get('opwd')
    print(password)
    name = request.user.username
    print(name)
    result = authenticate(username=name,password=password)
    if result is None:
        return JsonResponse({'result': 'NO'})
    else:
        return JsonResponse({'result':'YES'})

class forgetPassword(View):
    # 将账号信息进行加密
    def get(self,request):
        return render(request,'forgetPassword.html')

    def post(self,request):
        dict = request.POST
        uname = dict.get('user_name')
        email = dict.get('email')
        user = models.User.objects.get(username=uname)
        serializer = Serializer(settings.SECRET_KEY, 60 * 60 * 2)
        value = serializer.dumps({'id': user.id})
        value = value.decode()  # 转成字符串，用于拼接地址

        # 向用户发送邮件
        msg = '<a href="http://127.0.0.1:8000/ch_password/%s">点击修改密码</a>' % value
        send_mail('smartLock更改密码', '', settings.EMAIL_FROM, [email], html_message=msg)
        return HttpResponse('请在两个小时内前往邮箱，设置新密码')

class ch_password(View):
    def get(self,request,value):
        serializer = Serializer(settings.SECRET_KEY)
        try:
            # 解析用户编号
            dict = serializer.loads(value)
            userid = dict.get('id')

            user = models.User.objects.get(pk=userid)
            # 返回密码修改页
            return render(request,'ch_password.html',{'user':user})
        except SignatureExpired as e:
            return HttpResponse('对不起，链接已经过期')

    def post(self,request,value):
        dict = request.POST
        npwd = dict.get('npwd')
        serializer = Serializer(settings.SECRET_KEY)
        dict = serializer.loads(value)
        userid = dict.get('id')
        user = models.User.objects.get(pk=userid)
        print(user.username)
        print(npwd)
        user.set_password(npwd)
        user.save()
        return redirect('/')


class ChgpwdView(LoginRequireMixin,View):
    def get(self,request):
        user = request.user
        return render(request,'chgpwd.html',{'user':user})

    def post(self,request):

        dic = request.POST
        opwd = dic.get('opwd')
        npwd = dic.get('npwd')
        cpwd = dic.get('cpwd')
        context = {'opwd':opwd,'npwd':npwd,'cpwd':cpwd,'err_msg':'','title':'修改密码'}
        if not all([opwd, npwd, cpwd]):
            context['err_msg'] = '请将信息填写完整'
            return render(request, 'chgpwd.html', context)

        if npwd != cpwd:
            context['err_msg'] = '两次密码不一致'
            return render(request, 'zhuce.html', context)
        username = request.user.username
        user = models.User.objects.get(username=username)
        user.set_password(npwd)
        user.save()
        
        return redirect('/login')

def video_img(request):
    # with open(settings.BASE_DIR+'/static/img/video/image.jpg', 'rb') as f:
    #     data = f.read()

    return JsonResponse({'data':'/static/img/video/image'})

@login_required
def stop_video(request):
    # 停止摄像头
    # Vdemo.stop()
    # with open('/home/python/Desktop/MyGraduationDesign/static/stopVideo.txt','w') as f:
    with open(settings.VIDEO_SWITCH_URL, 'w') as f:
        f.write('0')

    # print(os.listdir(settings.VIDEO_IMAGE_URL))

    return redirect('/info')


@login_required
def open_lock(request):
    # 开锁
    # server_socket = request.COOKIES.get('server_socket')
    Vdemo.open_lock()
    return render(request,'info.html')

@login_required
def close_lock(request):
    # 关锁
    # server_socket = request.COOKIES.get('server_socket')
    Vdemo.close_lock()
    return render(request, 'info.html')