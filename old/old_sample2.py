# openCV, openGLの読み込み
import cv2
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

import numpy as np
import struct

# グローバル変数
cap = cv2.VideoCapture(0)
g_distance = 5.0
px = -1
py = -1
g_isLeftButtonOn = False
g_isRightButtonOn = False
xpos = 0.0
avg = None

def main():
    if not cap.isOpened():
        print("camera is disable")
        return
    
    init_GL(len(sys.argv), sys.argv)

    set_callback_functions()
    init(300, 300)
    glutMainLoop()

def init_GL(argc, argv):
    glutInit(argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(300, 300)     # window size
    glutInitWindowPosition(100, 100) # window position
    glutCreateWindow(b"teapot")      # show window

def init(width, height):
    """ initialize """
    glClearColor(0.0, 0.0, 0.0, 1.0)
    # glEnable(GL_DEPTH_TEST) # enable shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    ##set perspective
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

    # set_texture()

def set_callback_functions():
    glutDisplayFunc(display)         # draw callback function
    glutReshapeFunc(reshape)         # resize callback function
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutPassiveMotionFunc(motion)
    glutIdleFunc(idle)
    


def display():
    """ display """
    # global xpos, g_distance
    xpos = 0
    g_distance = 0
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    ##set camera
    gluLookAt(xpos, g_distance-15, 3.0, xpos, g_distance, 0.0, 0.0, -1.0, 1.0)

    glEnable(GL_DEPTH_TEST)
    ##draw a teapot
    glColor3f(1.0, 0.0, 0.0)
    # glutWireTeapot(1.0)   # wireframe
    create_road()
    x = 3
    # string = chr(x + 97)
    glPushMatrix()
    glTranslatef(xpos, g_distance, 1.0)
    string = "hello world"
    glColor(1.0, 1.0, 1.0)
    draw_str(-0.75, -0.75, string)
    glPopMatrix()

#     glPushMatrix()
#     glTranslatef(xpos, g_distance, 0.0)
#     create_object()
#     glPopMatrix()
# #    glutSolidTeapot(1.0)  # solid
    glFlush()  # enforce OpenGL command
    glDisable(GL_DEPTH_TEST)
    glutSwapBuffers()

def reshape(width, height):
    """callback function resize window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)


def mouse(button, state, x, y):
    global g_isLeftButtonOn, g_isRightButtonOn
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            g_isLeftButtonOn = True
        elif state == GLUT_UP:
            g_isLeftButtonOn = False
    # elif button == GLUT_MIDDLE_BUTTON:
    #     print("middle button")

    elif button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            g_isRightButtonOn = True
        elif state == GLUT_UP:
            g_isRightButtonOn = False
    # else:
    #     print("unknown button:", button)

    # if state == GLUT_DOWN:
    #     print("down mouse button")
    # elif state == GLUT_UP:
    #     print("up mouse button")
    # else:
    #     print("unknown state:", state)

    # print(x, y)


def motion(x, y):
    global px, py
    global g_isLeftButtonOn, g_isRightButtonOn
    global g_distance
    if g_isLeftButtonOn == True:
        if px >= 0 and py >=0:
            g_distance += float(y-py)/20
        px = x
        py = y
    else:
        px = -1
        py = -1
    glutPostRedisplay()

def keyboard(key, x, y):
    if key == b'q':
        print("exit")
        sys.exit()
        return


def idle():
    ret, frame = cap.read()
    if not ret:
        print("ret not exist")
        sys.exit()
    
    state = move(frame)
    # print(state)
    global xpos, g_distance
    g_distance += 0.1

    if state == 1:
        # left
        # print("left")
        xpos -= 0.1
        
    elif state == 2:
        # center
        # print("center")
        xpos += 0.0
    elif state == 3:
        # right
        # print("right")
        xpos += 0.1
    else:
        print("error")
    glutPostRedisplay()

    windowsize = (800, 600)
    frame = cv2.resize(frame, windowsize)
    
    cv2.imshow('camera', frame)
    if cv2.waitKey(30) & 0xff == 27:  
        sys.exit()

def move(frame):
    '''
    自分の位置を知らせる関数
    左のとき1
    中央のとき2
    右のとき3
    を返す
    '''
    global avg
    
    # グレースケールに変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 比較用のフレームを取得する
    if avg is None:
        avg = gray.copy().astype("float")
        # return 0

    # 現在のフレームと移動平均との差を計算
    cv2.accumulateWeighted(gray, avg, 0.6)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # デルタ画像を閾値処理を行う
    thresh = cv2.threshold(frameDelta, 8, 255, cv2.THRESH_BINARY)[1]
    # 画像の閾値に輪郭線を入れる
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    # windowsize = (800, 600)
    # thresh = cv2.resize(thresh, windowsize)
    # # cv2.imshow("Frame", frame)
    # cv2.imshow("move", thresh)
    # key = cv2.waitKey(30)
    # if key == 27:
    #     return 0

    np_thresh = np.array(thresh)
    topicSum = np.sum(np_thresh, axis=0)

    # 現在右左中央のどこにいるのかを判定するプログラム
    left = 0
    center = 0
    right = 0
    
    for i in range(len(topicSum)):
        if i*3 < len(topicSum):
            right+=topicSum[i]
        elif i*3 < len(topicSum)*2:
            center += topicSum[i]
        else:
            left+=topicSum[i]
    if left > center and left > right:
        return 1
        # print("left")
    elif right > center and right > left:
        return 3
        # print("right")
    else:
        return 2
        # print("center")

    return 0

def create_object():
    '''
    障害物を作成するプログラム
    '''
    pointO = [-1.0, -1.0, -1.0]
    pointA = [-1.0, -1.0, 1.0]
    pointB = [-1.0, 1.0, 1.0]
    pointC = [-1.0, 1.0, -1.0]

    pointD = [1.0, -1.0, -1.0]
    pointE = [1.0, -1.0, 1.0]
    pointF = [1.0, 1.0, 1.0]
    pointG = [1.0, 1.0, -1.0]

    glColor3d(1.0, 0.0, 0.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointO)
    glVertex3dv(pointA)
    glVertex3dv(pointB)
    glVertex3dv(pointC)
    glEnd()

    glColor3d(0.0, 1.0, 0.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointO)
    glVertex3dv(pointA)
    glVertex3dv(pointE)
    glVertex3dv(pointD)
    glEnd()

    glColor3d(0.0, 0.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointA)
    glVertex3dv(pointB)
    glVertex3dv(pointF)
    glVertex3dv(pointE)
    glEnd()

    glColor3d(1.0, 1.0, 0.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointB)
    glVertex3dv(pointC)
    glVertex3dv(pointG)
    glVertex3dv(pointF)
    glEnd()

    glColor3d(1.0, 0.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointC)
    glVertex3dv(pointO)
    glVertex3dv(pointD)
    glVertex3dv(pointG)
    glEnd()

    glColor3d(1.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointD)
    glVertex3dv(pointE)
    glVertex3dv(pointF)
    glVertex3dv(pointG)
    glEnd()

def create_road():
    glEnable(GL_TEXTURE_2D)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex3f(-10, 0, 0.0)
    glVertex3f( 10, 0, 0.0)
    glVertex3f( 10, 100, 0.0)
    glVertex3f(-10, 100, 0.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)


# これで描写できた
def draw_str(x, y, string, font=GLUT_BITMAP_HELVETICA_18, gap=0.25):
    '''
    文字列を描画する

    Parameters
    ----------
    x, y : float
        描画する座標．
    string : str
        描画する文字列．
    font : , default GLUT_BITMAP_HELVETICA_18
        フォント．以下から指定．
        GLUT_BITMAP_8_BY_13
        GLUT_BITMAP_9_BY_15
        GLUT_BITMAP_TIMES_ROMAN_10
        GLUT_BITMAP_TIMES_ROMAN_24
        GLUT_BITMAP_HELVETICA_10
        GLUT_BITMAP_HELVETICA_12
        GLUT_BITMAP_HELVETICA_18
    gap : float, default 0.25
        文字間隔．
    '''
	
    for k in range(len(string)):
        glRasterPos2f(x + gap*k, y)                 # 描画位置指定
        glutBitmapCharacter(font, ord(string[k]))   # 文字列描画

def set_texture():
    # TEXTURE_HEIGHT = 1024/8
    # TEXTURE_WIDTH = 1024/8
    imgName = "sample.png"
    # global g_TextureHandlesVideo
    img = cv2.imread(imgName)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img)

# def glut_print( x,  y,  font,  text, r,  g , b , a):

#     blending = False 
#     if glIsEnabled(GL_BLEND) :
#         blending = True

#     #glEnable(GL_BLEND)
#     glColor3f(1,1,1)
#     glRasterPos2f(x,y)
#     for ch in text :
#         glutBitmapCharacter( font , ctypes.c_int( ord(ch) ) )


#     if not blending :
#         glDisable(GL_BLEND) 


if __name__ == "__main__":
    main()
