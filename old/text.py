from OpenGL.GL import *
from OpenGL.GLUT import *

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