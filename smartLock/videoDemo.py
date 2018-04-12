import socket
import threading
import struct
import cv2
import time
import os
import numpy

class webCamera:
    def __init__(self, resolution = (640, 480), host = ("", 7999)):
        self.resolution = resolution
        self.host = host
        self.setSocket(self.host)
        self.img_quality = 15
    def setImageResolution(self, resolution):    # 设定像素
        self.resolution = resolution
    def setHost(self, host):    #  设定地址与端口
        self.host = host
    def setSocket(self, host):  # 建立socket
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.socket.bind(self.host)
        self.socket.listen(5)
        print("Server running on port:%d" % host[1])
    def recv_config(self,client):
        info = struct.unpack("ihh",client.recv(12))
        if info[0]>911:        #print(info[0])
            self.img_quality=int(info[0])-911
            self.resolution=list(self.resolution)
            self.resolution[0]=info[1]
            self.resolution[1]=info[2]
            self.resolution=tuple(self.resolution)
            return 1
        else :
            return 0
    def _processConnection(self, client,addr):
        if(self.recv_config(client)==0):
            return
        camera = cv2.VideoCapture(0)
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),self.img_quality]
        f = open("video_info.txt", 'a+')
        print("Got connection from %s:%d" % (addr[0], addr[1]),file=f);
        print("像素为:%d * %d"%(self.resolution[0],self.resolution[1]),file=f)
        print ("打开摄像头成功",file=f)
        print("连接开始时间:%s"%time.strftime("%Y-%m-%d %H:%M:%S",
                time.localtime(time.time())),file=f)
        f.close()
        while(1):
            time.sleep(0.13)
            (grabbed, self.img) = camera.read()
            self.img  = cv2.resize(self.img,self.resolution)
            result, imgencode = cv2.imencode('.jpg',self.img,encode_param)
            img_code = numpy.array(imgencode)
            self.imgdata  = img_code.tostring()
            try:
                client.send(struct.pack("lhh",len(self.imgdata),
                        self.resolution[0],self.resolution[1])+self.imgdata)  #发送图片信息(图片长度,分辨率,图片内容)
            except:
                f = open("video_info.txt", 'a+')
                print("%s:%d disconnected!" % (addr[0], addr[1]),file=f)
                print("连接结束时间:%s"%time.strftime("%Y-%m-%d %H:%M:%S",
                    time.localtime(time.time())),file=f)
                print("****************************************",file=f)
                camera.release()
                f.close()
                return
    def run(self):
        while(1):
            client,addr = self.socket.accept()
            clientThread = threading.Thread(target = self._processConnection,
                args = (client, addr, ))  #有客户端连接时产生新的线程进行处理
            clientThread.start()


def main():
    cam = webCamera()
    cam.run()


if __name__ == "__main__":
    main()








# # coding=gbk
# __author__ = 'yangle'
# __time__ = '2018/3/22 0:13'
#
# import socket;
# import threading;
# import os;
# import time;
# import numpy
# import cv2
# import re
# import sys
# from django.conf import settings
#
# class webCamConnect:
#     def __init__(self, resolution = [640,480], remoteAddress = ("192.168.0.101", 7999), windowName = "video"):
#         self.remoteAddress = remoteAddress;
#         self.resolution = resolution;
#         self.name = windowName;
#         self.mutex = threading.Lock();
#         self.src=911+15
#         self.interval=0
#         self.path=os.getcwd()
#         self.img_quality = 15
#     def _setSocket(self):
#         self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
#         self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
#     def connect(self):
#         self._setSocket();
#         self.socket.connect(('192.168.0.100',7999));
#     def _processImage(self):
#         self.socket.send('926640480'.encode('utf-8'));   # struct.pack("lhh",self.src,self.resolution[0],self.resolution[1])
#         i = 1
#         flag = 1
#         with open('/home/python/Desktop/MyGraduationDesign/static/stopVideo.txt', 'w') as f:
#             f.write('1')
#         while(flag):
#             # info = struct.unpack("l", self.socket.recv(8));
#             with open('/home/python/Desktop/MyGraduationDesign/static/stopVideo.txt','r') as f:
#                 flag = int(f.read())
#             info = self.socket.recv(4).decode('utf-8')
#             print(info)
#             bufSize = int(info)
#             self.control = 'start'
#             if bufSize:
#                  try:
#                     self.mutex.acquire();
#                     self.buf=b''
#                     # tempBuf=self.buf
#
#                     while(bufSize):                 #循环读取到一张图片的长度
#                         tempBuf = self.socket.recv(bufSize);
#                         bufSize -= len(tempBuf);
#                         self.buf += tempBuf;
#                         print('1')
#                         data = numpy.fromstring(self.buf,dtype='uint8')
#                         print(2)
#                         self.image=cv2.imdecode(data,1)
#                         path = '/home/python/Desktop/MyGraduationDesign/static/img/video/image%d.jpg' %i
#
#                         print(path)
#                         with open(path,'wb')as f:
#                             f.write(tempBuf)
#                         i = i + 1
#
#                         if self.control == 'stop':
#                             break
#
#                         # cv2.imshow(self.name,self.image)
#
#                  except:
#                      print("接收失败")
#                      pass;
#                  finally:
#                      self.mutex.release();
#                      if cv2.waitKey(10) == 27:
#                          self.socket.close()
#                          # cv2.destroyAllWindows()
#                          print("放弃连接")
#                          break
#     def getData(self, interval):
#         showThread=threading.Thread(target=self._processImage);
#         showThread.start();
#         # if interval != 0:   # 非0则启动保存截图到本地的功能
#         #     saveThread=threading.Thread(target=self._savePicToLocal,args = (interval,
#         #         ));
#         #     saveThread.setDaemon(1);
#         #     saveThread.start();
#     def setWindowName(self, name):
#         self.name = name;
#     def setRemoteAddress(self,remoteAddress):
#         self.remoteAddress = remoteAddress;
#     # def _savePicToLocal(self, interval):
#     #     i = 1
#     #     while(1):
#     #         try:
#     #             self.mutex.acquire();
#     #             print('55555555555')
#     #             path='/home/python/Desktop/MyGraduationDesign/static/img/video/';
#     #             print('6666666666')
#     #             if not os.path.exists(path):
#     #                 os.mkdir(path);
#     #             print('7777777777')
#     #             cv2.imwrite(path + 'image%d.jpg'%i,self.image)
#     #             i += 1
#     #         except:
#     #             print('888888888888')
#     #
#     #         finally:
#     #             self.mutex.release();
#     #             time.sleep(interval);
#     # def check_config(self):
#     #     path=os.getcwd()
#     #     print(path)
#     #     if os.path.isfile(r'%s\video_config.txt'%path) is False:
#     #         f = open("video_config.txt", 'w+')
#     #         print("w = %d,h = %d" %(self.resolution[0],self.resolution[1]),file=f)
#     #         print("IP is %s:%d" %(self.remoteAddress[0],self.remoteAddress[1]),file=f)
#     #         print("Save pic flag:%d" %(self.interval),file=f)
#     #         print("image's quality is:%d,range(0~95)"%(self.img_quality),file=f)
#     #         f.close()
#     #         print("初始化配置");
#     #     else:
#     #         f = open("video_config.txt", 'r+')
#     #         tmp_data=f.readline(50)#1 resolution
#     #         num_list=re.findall(r"\d+",tmp_data)
#     #         self.resolution[0]=int(num_list[0])
#     #         self.resolution[1]=int(num_list[1])
#     #         tmp_data=f.readline(50)#2 ip,port
#     #         num_list=re.findall(r"\d+",tmp_data)
#     #         str_tmp="%d.%d.%d.%d" %(int(num_list[0]),int(num_list[1]),int(num_list[2]),int(num_list[3]))
#     #         self.remoteAddress=(str_tmp,int(num_list[4]))
#     #         tmp_data=f.readline(50)#3 savedata_flag
#     #         self.interval=int(re.findall(r"\d",tmp_data)[0])
#     #         tmp_data=f.readline(50)#3 savedata_flag
#     #         #print(tmp_data)
#     #         self.img_quality=int(re.findall(r"\d+",tmp_data)[0])
#     #        #print(self.img_quality)
#     #         self.src=911+self.img_quality
#     #         f.close()
#     #         print("读取配置")
#     def stopVideo(self):
#         self.control = 'stop'
# def main():
#     print("创建连接...")
#     cam = webCamConnect();
#     # cam.check_config()
#     print("像素为:%d * %d"%(cam.resolution[0],cam.resolution[1]))
#     print("目标ip为%s:%d"%(cam.remoteAddress[0],cam.remoteAddress[1]))
#     cam.connect();
#     cam.getData(cam.interval);
#
#
# if __name__ == "__main__":
#     main()

