from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    return render(request,'first/index.html')

def yy(request):
    return render(request, 'first/123.html')

def zhuce(request):
    return render(request,'first/zhuce.html')

def chuangjian(request):
    dic = request.POST
    name = dic.get('userName')
    word = dic.get('password')
    people = Users.man.create(name,word)
    people.save()
    return redirect('/')

def page_dl(request):
    return render(request,'first/denglu.html')

def denglu(request):
    dic = request.POST
    name = dic.get('dengluming')
    word = dic.get('denglumima')
    if Users.man.filter(userName = name,password=word):
        use = Users.man.get(userName=name)
        return render(request,'first/kongzhi.html',{'use':use})
    return render(request,'first/denglu.html',{'alert':'<script>$(function () {alert("用户名或密码错误")})</script>'})

def cuowu(request):
    return render(request,'first/cuowu.html')

def page_changePwd(request,id):
    list = Users.man.get(id=id)
    return render(request,'first/page_changePwd.html',{'list':list})