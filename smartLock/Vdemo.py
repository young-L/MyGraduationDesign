# import cv2
# img = cv2.imread('jiaxiao.JPEG')
#
# cv2.namedWindow("w")
# cv2.imshow('w',img)
# cv2.waitKey(0)

# import cv2
#
# cv2.namedWindow('testcamera')
#
# capture = cv2.imread()
#
# while 1:
#     ret, img = capture.read()
#     cv2.imshow('testcamera', img)
#     key = cv2.waitKey(1)
#     num += 1
#     if key == 1048603:  # <ESC>
#         break
#
# capture.release()
# cv2.destroyAllWindows()


import cv2.cv as cv
import socket, time, Image, StringIO

HOST, PORT = "192.168.0.102", 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
f = sock.makefile()

cv.NamedWindow("camera_server")

while True:
    msg = f.readline()
    if not msg:
        break
    print(len(msg), msg[-2])
    jpeg = msg.replace("\-n", "\n")
    buf = StringIO.StringIO(jpeg[0:-1])
    buf.seek(0)
    pi = Image.open(buf)
    img = cv.CreateImageHeader((640, 480), cv.IPL_DEPTH_8U, 3)
    cv.SetData(img, pi.tostring())
    buf.close()
    cv.ShowImage("camera_server", img)
    if cv.WaitKey(10) == 27:
        break

sock.close()
cv.DestroyAllWindows()