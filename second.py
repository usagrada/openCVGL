# openCV, openGLの読み込み
import cv2
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from PIL import Image

import numpy as np
import struct
import time

# グローバル変数
cap = cv2.VideoCapture(0)
ypos = 0.0
px = -1
py = -1
g_isLeftButtonOn = False
g_isRightButtonOn = False
xpos = 0.0
avg = None
# x = [-10, 10], y = [10, 100]
objPos = [
    [-5, 20], # 20
    [-3, 20],
    [-1, 20],
    [ 1, 20],
    [ 3, 20],
    [ 5, 20],

    [-9, 30], # 30
    [-7, 30],
    [-5, 30],
    [ 0, 30],
    [ 5, 30],
    [ 7, 30],
    [ 9, 30],

    [-9, 40], # 40
    [ 9, 40],

    [-7, 50], # 50
    [-5, 50],
    [-3, 50],
    [-1, 50],
    [ 1, 50],
    [ 3, 50],
    [ 5, 50],
    [ 7, 50],
    

    [-9, 60], # 60
    [-7, 60],
    [-2, 60],
    [ 0, 60],
    [ 2, 60],
    [ 7, 60],
    [ 9, 60],
    
    [-9, 70], # 70
    [-4, 70],
    [-2, 70],
    [ 0, 70],
    [ 2, 70],
    [ 4, 70],
    [ 9, 70],

    [-8.5, 90], # 90
    [-6, 90],
    [-4, 90],
    [-2, 90],
    [ 2, 90],
    [ 4, 90],
    [ 6, 90],
    [ 8.5, 90]
]
timer = 3.0

gameState = 0
mode = 0

direction = 0
life = 3
# 画像の選択
gTextureHandles = [0, 0, 0]

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
    glutInitWindowSize(500, 500)     # window size
    glutInitWindowPosition(100, 100) # window position
    glutCreateWindow(b"Game")      # show window

def init(width, height):
    """ initialize """
    glClearColor(0.0, 0.0, 0.0, 1.0)
    # glEnable(GL_DEPTH_TEST) # enable shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    ##set perspective
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

    set_texture()

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
    global gameState
    global xpos, ypos
    global timer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    ##set camera
    gluLookAt(xpos, ypos-15, 3.0, xpos, ypos, 0.0, 0.0, -1.0, 1.0)

    glEnable(GL_DEPTH_TEST)
    ##draw a teapot
    glColor3f(1.0, 0.0, 0.0)
    # 道を作る
    if gameState == 3:
        glPushMatrix()
        # glTranslatef(0.0, 80.0, 0.0)
        createClearRoad()
        # glTranslatef(0.0, 100.0, 0.0)
        # createClearRoad()
        glPopMatrix()
    else:
        create_road()

        glPushMatrix()
        glTranslatef(0.0, -100.0, 0.0)
        create_road2()
        glTranslatef(0.0, 200.0, 0.0)
        create_road2()
        glPopMatrix()
    
    
    glPushMatrix()
    glTranslatef(-11.0, 0.0, 0.0)
    makeWall()
    glTranslatef(22.0, 0.0, 0.0)
    makeWall()
    glTranslatef(0.0, 100.0, 0.0)
    makeWall()
    glTranslatef(-22.0, 0.0, 0.0)
    makeWall()
    glPopMatrix()

    # テキストの表示
    if gameState == 0:
        glPushMatrix()
        glTranslatef(xpos, ypos, 2.0)
        # string = "hello world"
        glColor(0.0, 0.0, 0.0)
        text1 = "Press Enter" 
        text2 = "for Game Start"
        draw_str(-2.0, -5.0, text1, gap=0.4)
        glTranslatef(0.0, 0.0, -0.7)
        draw_str(-2.7, -5.0, text2, gap=0.4)
        glPopMatrix()
    
    elif gameState == 1:
        glPushMatrix()
        glTranslatef(xpos, ypos, 2.0)
        # glScalef(2.0, 2.0, 1.0)
        glColor(0.0, 0.0, 0.0)
        text = str(int(timer)+1)
        draw_str(-0.1, -5.0, text, gap=0.4)
        glPopMatrix()
    
    elif gameState == 3:
    # if gameState == 0:
        glPushMatrix()
        glTranslatef(xpos, ypos, 2.0)
        text = "Game Clear"
        glColor3d(1.0, 1.0, 0.0)
        draw_str(-1.8, -8.0, text, gap=0.4)
        glPopMatrix()
    
    elif gameState == 4:
    # if gameState == 0:
        glPushMatrix()
        glTranslatef(xpos, ypos, 2.0)
        text = "Game Over"
        glColor3d(1.0, 0.0, 0.0)
        draw_str(-1.8, -8.0, text, gap=0.4)
        glPopMatrix()

    if gameState > 0 and gameState < 3 or gameState == 6:
        glPushMatrix()
        glTranslatef(xpos+3.5, ypos, 5.0)
        # string = "hello world"
        glColor(0.0, 1.0, 1.0)
        draw_str(-2.0, 0.0, "now :",gap=0.4)
        draw_str(0.0, 0.0, str(int(ypos*10)/10), gap= 0.3)

        
        global life
        glTranslatef(0.0, 0.0, -0.7)
        draw_str(-2.0, 0.0, "life :"+str(int(life)),gap=0.4)
        glTranslatef(0.0, 0.0, 0.7)

        global direction
        if direction < 0:
            draw_str(-9.0, 0.0, "left",gap=0.5)
        elif direction == 0:
            draw_str(-9.0, 0.0, "straight",gap=0.5)
        elif direction > 0:
            draw_str(-9.0, 0.0, "right",gap=0.5)
        # draw_str(-1.0, -1.0, string)
        glPopMatrix()



        # 障害物を作る
        global objPos
        glPushMatrix()
        for i in range(len(objPos)):
            if objPos[i][1] < ypos - 3:
                continue
            glTranslatef(objPos[i][0], objPos[i][1], 1.5)
            glScalef(1.0, 0.1, 1.5)
            create_object()
            glScalef(1.0, 10.0, 0.66)
            glTranslatef(-objPos[i][0], -objPos[i][1], -1.5)
        glPopMatrix()

        # 自分のアイコンを作る
        glPushMatrix()
        glTranslatef(xpos, ypos, 0.5)
        glScalef(0.5, 0.5, 0.5)
        createMe()
        glPopMatrix()
        # glutWireTeapot(1.0)   # wireframe
        # glutSolidTeapot(1.0)  # solid
    glFlush()  # enforce OpenGL command
    glDisable(GL_DEPTH_TEST)

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
    global ypos
    if g_isLeftButtonOn == True:
        if px >= 0 and py >=0:
            ypos += float(y-py)/20
        px = x
        py = y
    else:
        px = -1
        py = -1
    glutPostRedisplay()

def keyboard(key, x, y):
    global mode
    global gameState
    global timer
    global life
    global xpos, ypos
    # print(key)
    if gameState == 0:
        if key == b'\r':
            print("press")
            gameState = 1
    
    if key == b's':
        if gameState == 6:
            print("start")
            gameState = 2
        elif gameState == 2:
            print("stop")
            gameState = 6

    if key == b'q':
        print("exit")
        sys.exit()
        return
    # reset
    if key == b'r':
        gameState = 0
        xpos = 0.0
        ypos = 0.0
        timer = 3.0
        life = 3
    if key == 27:
        sys.exit()
    if key == b'1':
        mode = 1
    if key == b'0':
        mode = 0


def idle():
    global gameState
    global timer
    global xpos, ypos
    global direction
    global mode

    if gameState == 0:
        return
    elif gameState == 1:
        time.sleep(1)
        timer = timer - 1
        # print(timer)
        if timer < 0:
            gameState = 2
        glutPostRedisplay()
        return
    elif gameState == 3 and ypos < 150.0:
        cv2.destroyAllWindows()
        ypos += 0.01
        glutPostRedisplay()
        return
    elif gameState >= 3:
        return
    
    
    ret, frame = cap.read()
    if not ret:
        print("ret not exist")
        sys.exit()
    
    state = move(frame)
    # print(state)
    ypos += 0.1
    if ypos > 100:
        gameState = 3

    if state == 1:
        # left
        # print("left")
        xpos -= 0.1
        direction = -1
        
    elif state == 2:
        # center
        # print("center")
        xpos += 0.0
        direction = 0
    elif state == 3:
        # right
        # print("right")
        xpos += 0.1
        direction = 1
    else:
        print("error")
    
    if xpos < -9.5:
        xpos = -9.5
    elif xpos > 9.5:
        xpos = 9.5
    
    global objPos
    global life
    for i in range(len(objPos)):
        if objPos[i][1] <= ypos <= objPos[i][1]+0.1:
            if objPos[i][0]-1.5 <= xpos <= objPos[i][0]+1.5:
                life -= 1
                # ypos -= 0.1
                if life == 0:
                    gameState = 4
                break
    

    glutPostRedisplay()

    frameShow = np.fliplr(frame).copy()
    windowsize = (400, 300)
    frame = cv2.resize(frame, windowsize)
    frameShow = cv2.resize(frameShow, windowsize)
    # for i in range(len(frame[0])):
    #     frame[i] = frame[i][::-1]
    
    if mode == 1:
        cv2.imshow('camera', frameShow)
        cv2.moveWindow('camera', 700, 100)
        key = cv2.waitKey(30)
        # print(key)
        if key == 48:
            mode = 0
            cv2.destroyAllWindows()
        if key == 27 or key == ord('q'):
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

def createMe():
    '''
    Meを作成するプログラム
    '''
    pointO = [-1.0, -1.0, -1.0]
    pointA = [-1.0, -1.0, 1.0]
    pointB = [-1.0, 1.0, 1.0]
    pointC = [-1.0, 1.0, -1.0]

    pointD = [1.0, -1.0, -1.0]
    pointE = [1.0, -1.0, 1.0]
    pointF = [1.0, 1.0, 1.0]
    pointG = [1.0, 1.0, -1.0]

    global gTextureHandles
    global direction
    
    glBindTexture(GL_TEXTURE_2D, gTextureHandles[4])
    if direction > 0:
        glBindTexture(GL_TEXTURE_2D, gTextureHandles[3])
    glEnable(GL_TEXTURE_2D)

    glColor3d(0.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointO)
    glVertex3dv(pointA)
    glVertex3dv(pointB)
    glVertex3dv(pointC)
    glEnd()

    glColor3d(1.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    glTexCoord2d(1.0, 1.0)
    glVertex3dv(pointO)
    glTexCoord2d(1.0, 0.0)
    glVertex3dv(pointA)
    glTexCoord2d(0.0, 0.0)
    glVertex3dv(pointE)
    glTexCoord2d(0.0, 1.0)
    glVertex3dv(pointD)
    glEnd()

    glColor3d(0.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointA)
    glVertex3dv(pointB)
    glVertex3dv(pointF)
    glVertex3dv(pointE)
    glEnd()

    glColor3d(0.0, 0.0, 1.0)
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

    glColor3d(0.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointD)
    glVertex3dv(pointE)
    glVertex3dv(pointF)
    glVertex3dv(pointG)
    glEnd()

    glDisable(GL_TEXTURE_2D)

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

    global gTextureHandles
    
    glBindTexture(GL_TEXTURE_2D, gTextureHandles[2])
    glEnable(GL_TEXTURE_2D)

    glColor3d(1.0, 0.0, 0.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointO)
    glVertex3dv(pointA)
    glVertex3dv(pointB)
    glVertex3dv(pointC)
    glEnd()

    glColor3d(0.5, 0.5, 0.5)
    glBegin(GL_POLYGON)
    glTexCoord2d(1.0, 1.0)
    glVertex3dv(pointO)
    glTexCoord2d(1.0, 0.0)
    glVertex3dv(pointA)
    glTexCoord2d(0.0, 0.0)
    glVertex3dv(pointE)
    glTexCoord2d(0.0, 1.0)
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

    glDisable(GL_TEXTURE_2D)

def create_road():
    glBindTexture(GL_TEXTURE_2D, gTextureHandles[0])
    glEnable(GL_TEXTURE_2D)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    glTexCoord2d(1.0, 0.0)
    glVertex3f(-10, 0, 0.0)
    glTexCoord2d(0.0, 0.0)
    glVertex3f( 10, 0, 0.0)
    glTexCoord2d(0.0, 4.0)
    glVertex3f( 10, 100, 0.0)
    glTexCoord2d(1.0, 4.0)
    glVertex3f(-10, 100, 0.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def create_road2():
    glBindTexture(GL_TEXTURE_2D, gTextureHandles[1])
    glEnable(GL_TEXTURE_2D)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    glTexCoord2d(1.0, 0.0)
    glVertex3f(-10, 0, 0.0)
    glTexCoord2d(0.0, 0.0)
    glVertex3f( 10, 0, 0.0)
    glTexCoord2d(0.0, 4.0)
    glVertex3f( 10, 100, 0.0)
    glTexCoord2d(1.0, 4.0)
    glVertex3f(-10, 100, 0.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def createClearRoad():
    glBegin(GL_POLYGON)

    glColor3d(1.0, 0.0, 0.0)
    glVertex3f(-10, 0, 0.0)
    glColor3d(1.0, 1.0, 0.0)
    glVertex3f( 10, 0, 0.0)

    glColor3d(0.0, 1.0, 1.0)
    glVertex3f( 10, 100, 0.0)
    glColor3d(1.0, 0.0, 1.0)
    glVertex3f(-10, 100, 0.0)

    glEnd()

    glTranslatef(0.0, 100.0, 0.0)

    glBegin(GL_POLYGON)
    
    glColor3d(1.0, 0.0, 1.0)
    glVertex3f(-10, 0, 0.0)
    glColor3d(0.0, 1.0, 1.0)
    glVertex3f( 10, 0, 0.0)

    glColor3d(1.0, 1.0, 0.0)
    glVertex3f( 10, 100, 0.0)
    glColor3d(1.0, 0.0, 0.0)
    glVertex3f(-10, 100, 0.0)
    
    glEnd()

def draw_str(x, y, string, font=GLUT_BITMAP_TIMES_ROMAN_24, gap=0.25):
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
    # imgName = "index.png"
    name = ["green.png", "block.png", "grayblock.png", "meLeft.png", "meRight.png"]
    # global g_TextureHandlesVideo
    
    global gTextureHandles
    gTextureHandles = glGenTextures(5)
    # print(gTextureHandles)
    # img = Image.open("sample.png")
    # w, h = img.size
    for i in range(len(gTextureHandles)):
        img = Image.open(name[i])
        w, h = img.size
        
        glBindTexture(GL_TEXTURE_2D, gTextureHandles[i])
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # if i == 2:
        #     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        #     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

def makeWall():
    global gTextureHandles
    glBindTexture(GL_TEXTURE_2D, gTextureHandles[1])
    pointO = [-1.0, 0.0, 0.0]
    pointA = [-1.0, 0.0, 3.0]
    pointB = [-1.0, 100.0, 3.0]
    pointC = [-1.0, 100.0, 0.0]

    pointD = [1.0, 0.0, 0.0]
    pointE = [1.0, 0.0, 3.0]
    pointF = [1.0, 100.0, 3.0]
    pointG = [1.0, 100.0, 0.0]

    glEnable(GL_TEXTURE_2D)

    glColor3d(1.0, 0.5, 0.5)
    glBegin(GL_POLYGON)
    glTexCoord2d(0.0, 0.3)
    glVertex3dv(pointO)
    glTexCoord2d(0.0, 0.0)
    glVertex3dv(pointA)
    glTexCoord2d(50.0, 0.0)
    glVertex3dv(pointB)
    glTexCoord2d(50.0, 0.3)
    glVertex3dv(pointC)
    glEnd()
    # glDisable(GL_TEXTURE_2D)

    # glColor3d(0.0, 1.0, 0.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointO)
    glVertex3dv(pointA)
    glVertex3dv(pointE)
    glVertex3dv(pointD)
    glEnd()

    # glColor3d(0.0, 0.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointA)
    glVertex3dv(pointB)
    glVertex3dv(pointF)
    glVertex3dv(pointE)
    glEnd()

    # glColor3d(1.0, 1.0, 0.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointB)
    glVertex3dv(pointC)
    glVertex3dv(pointG)
    glVertex3dv(pointF)
    glEnd()

    # glColor3d(1.0, 0.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointC)
    glVertex3dv(pointO)
    glVertex3dv(pointD)
    glVertex3dv(pointG)
    glEnd()

    # glEnable(GL_TEXTURE_2D)

    # glColor3d(1.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    glTexCoord2d(0.0, 0.3)
    glVertex3dv(pointD)
    glTexCoord2d(0.0, 0.0)
    glVertex3dv(pointE)
    glTexCoord2d(50.0, 0.0)
    glVertex3dv(pointF)
    glTexCoord2d(50.0, 0.3)
    glVertex3dv(pointG)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    

if __name__ == "__main__":
    main()
