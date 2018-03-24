# coding=gbk
__author__ = 'yangle'
__time__ = '2018/3/22 0:13'

import socket;
import threading;
import os;
import time;
import numpy
import cv2
import re
from django.shortcuts import render
from django.http import request
class webCamConnect:
    def __init__(self, resolution = [640,480], remoteAddress = ("192.168.1.104", 7999), windowName = "video"):
        self.remoteAddress = remoteAddress;
        self.resolution = resolution;
        self.name = windowName;
        self.mutex = threading.Lock();
        self.src=911+15
        self.interval=0
        self.path=os.getcwd()
        self.img_quality = 15
    def _setSocket(self):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
    def connect(self):
        self._setSocket();
        self.socket.connect(('100.65.30.81',7999));
    def _processImage(self):
        self.socket.send('926640480'.encode('utf-8'));   # struct.pack("lhh",self.src,self.resolution[0],self.resolution[1])
        while(1):
            # info = struct.unpack("l", self.socket.recv(8));
            info = self.socket.recv(4).decode('utf-8')
            print(info)
            bufSize = int(info)
            if bufSize:
                 try:
                    self.mutex.acquire();
                    self.buf=b''
                    # tempBuf=self.buf
                    while(bufSize):                 #ѭ����ȡ��һ��ͼƬ�ĳ���
                        tempBuf = self.socket.recv(bufSize);
                        bufSize -= len(tempBuf);
                        self.buf += tempBuf;
                        print('1')
                        data = numpy.fromstring(self.buf,dtype='uint8')
                        print(2)
                        self.image=cv2.imdecode(data,1)
                        print(3)
                        yield render(request,'video.html',{'video':self.image})
                        cv2.imshow(self.name,self.image)
                 except:
                     print("����ʧ��")
                     pass;
                 finally:
                     self.mutex.release();
                     if cv2.waitKey(10) == 27:
                         self.socket.close()
                         cv2.destroyAllWindows()
                         print("��������")
                         break

    def playVideo(self):
        while(1):
            next(self._processImage())
    def getData(self, interval):
        showThread=threading.Thread(target=self.playVideo);
        showThread.start();
        if interval != 0:   # ��0�����������ͼ�����صĹ���
            saveThread=threading.Thread(target=self._savePicToLocal,args = (interval,
                ));
            saveThread.setDaemon(1);
            saveThread.start();
    def setWindowName(self, name):
        self.name = name;
    def setRemoteAddress(self,remoteAddress):
        self.remoteAddress = remoteAddress;
    def _savePicToLocal(self, interval):
        while(1):
            try:
                self.mutex.acquire();
                path="~/Desktop/MyGraduationWork/static/img/video";
                if not os.path.exists(path):
                    os.mkdir(path);
                cv2.imwrite(path + "/" + time.ctime()+'msg' + ".jpg",self.image)
            except:
                pass;
            finally:
                self.mutex.release();
                time.sleep(interval);
    def check_config(self):
        path=os.getcwd()
        print(path)
        if os.path.isfile(r'%s\video_config.txt'%path) is False:
            f = open("video_config.txt", 'w+')
            print("w = %d,h = %d" %(self.resolution[0],self.resolution[1]),file=f)
            print("IP is %s:%d" %(self.remoteAddress[0],self.remoteAddress[1]),file=f)
            print("Save pic flag:%d" %(self.interval),file=f)
            print("image's quality is:%d,range(0~95)"%(self.img_quality),file=f)
            f.close()
            print("��ʼ������");
        else:
            f = open("video_config.txt", 'r+')
            tmp_data=f.readline(50)#1 resolution
            num_list=re.findall(r"\d+",tmp_data)
            self.resolution[0]=int(num_list[0])
            self.resolution[1]=int(num_list[1])
            tmp_data=f.readline(50)#2 ip,port
            num_list=re.findall(r"\d+",tmp_data)
            str_tmp="%d.%d.%d.%d" %(int(num_list[0]),int(num_list[1]),int(num_list[2]),int(num_list[3]))
            self.remoteAddress=(str_tmp,int(num_list[4]))
            tmp_data=f.readline(50)#3 savedata_flag
            self.interval=int(re.findall(r"\d",tmp_data)[0])
            tmp_data=f.readline(50)#3 savedata_flag
            #print(tmp_data)
            self.img_quality=int(re.findall(r"\d+",tmp_data)[0])
           #print(self.img_quality)
            self.src=911+self.img_quality
            f.close()
            print("��ȡ����")
def main():
    print("��������...")
    cam = webCamConnect();
    cam.check_config()
    print("����Ϊ:%d * %d"%(cam.resolution[0],cam.resolution[1]))
    print("Ŀ��ipΪ%s:%d"%(cam.remoteAddress[0],cam.remoteAddress[1]))
    cam.connect();
    cam.getData(cam.interval);
if __name__ == "__main__":
    main()
