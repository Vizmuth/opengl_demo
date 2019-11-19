import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np


translate_x, translate_y = 0, 0
click_x, click_y = 0,0
angle = 0
zoom_x, zoom_y, zoom_z = 1, 1, 1

WIN_W, WIN_H = 640, 480                             # 保存窗口宽度和高度的变量
def draw():
    global WIN_W, WIN_H
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    

    glLoadIdentity()
    #沿z轴平移
    glTranslate(0.0, 0.0, -5.0)
    #开始绘制立方体的每个面，同时设置纹理映射
    glBindTexture(GL_TEXTURE_2D, 1)
    #绘制四边形
    glBegin(GL_QUADS)        
    #设置纹理坐标
    glTexCoord2f(0.0, 0.0)
    #绘制顶点
    glVertex3f(-1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glEnd()


    glLoadIdentity()

    # glScalef(0,0,0.5)
    #沿z轴平移
    glTranslate(translate_x,translate_y,-4)
    glRotated(angle, translate_x,translate_y,-4)
    glScaled(zoom_x, zoom_y, zoom_z)
    #分别绕x,y,z轴旋转
    glRotatef(0.0, 1.0, 0.0, 0.0)
    glRotatef(0.0, 0.0, 1.0, 0.0)
    glRotatef(0.0, 0.0, 0.0, 1.0)


    # 设置视口
    # glViewport(0, 0, WIN_W, WIN_H)
    # glLoadIdentity(2)
    glBindTexture(GL_TEXTURE_2D, 1)
    glBegin(GL_LINES)

    glTexCoord2f(0.0, 0.0)
    #绘制顶点
    glVertex3f(-0.8, 0.8, 1.0)
    glVertex3f(0.8, 0.8, 1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(0.8, 0.8, 1.0)
    glVertex3f(0.8, -0.8, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(0.8, -0.8, 1.0)
    glVertex3f(-0.8, -0.8, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-0.8, -0.8, 1.0)
    glVertex3f(-0.8, 0.8, 1.0)
    
    # glColor4f(1.0, 0.0, 0.0, 1.0)        # 设置当前颜色为红色不透明
    # glVertex3f(-0.8, 0.8, 1.0)           # 设置x轴顶点（x轴负方向）
    # glVertex3f(0.8, 0.8, 1.0)            # 设置x轴顶点（x轴正方向）
    # glColor4f(1.0, 0.0, 0.0, 1.0)        # 设置当前颜色为红色不透明
    # glVertex3f(0.8, 0.8, 1.0)           # 设置x轴顶点（x轴负方向）
    # glVertex3f(0.8, -0.8, 1.0)            # 设置x轴顶点（x轴正方向）


    # glColor4f(1.0, 0.0, 0.0, 1.0)        # 设置当前颜色为红色不透明
    # glVertex3f(0.8, -0.8, 1.0)           # 设置x轴顶点（x轴负方向）
    # glVertex3f(-0.8, -0.8, 1.0)            # 设置x轴顶点（x轴正方向）
    # glColor4f(1.0, 0.0, 0.0, 1.0)        # 设置当前颜色为红色不透明
    # glVertex3f(-0.8, -0.8, 1.0)           # 设置x轴顶点（x轴负方向）
    # glVertex3f(-0.8, 0.8, 1.0)            # 设置x轴顶点（x轴正方向）
    
    glEnd()                              # 结束绘制线段

    # # ---------------------------------------------------------------
    # glBegin(GL_LINES)                    # 开始绘制线段（世界坐标系）
    
    # # 以红色绘制x轴
    # glColor4f(1.0, 0.0, 0.0, 1.0)        # 设置当前颜色为红色不透明
    # glVertex3f(-1, 0.0, 0.0)           # 设置x轴顶点（x轴负方向）
    # glVertex3f(1, 0.0, 0.0)            # 设置x轴顶点（x轴正方向）
    
    # # 以绿色绘制y轴
    # glColor4f(0.0, 1.0, 0.0, 1.0)        # 设置当前颜色为绿色不透明
    # glVertex3f(0.0, -1, 0.0)           # 设置y轴顶点（y轴负方向）
    # glVertex3f(0.0, 1, 0.0)            # 设置y轴顶点（y轴正方向）
    
    # # 以蓝色绘制z轴
    # glColor4f(0.0, 0.0, 1.0, 1.0)        # 设置当前颜色为蓝色不透明
    # glVertex3f(0.0, 0.0, -1)           # 设置z轴顶点（z轴负方向）
    # glVertex3f(0.0, 0.0, 1)            # 设置z轴顶点（z轴正方向）
    
    # glEnd()                              # 结束绘制线段
    
    # # ---------------------------------------------------------------
    # glBegin(GL_QUADS)                # 开始绘制三角形（z轴负半区）
    
    # glColor4f(1.0, 0.0, 0.0, 1.0)        # 设置当前颜色为红色不透明
    # glVertex3f(+0.5, -0.366, -0.5)       # 设置三角形顶点
    # glColor4f(0.0, 1.0, 0.0, 1.0)        # 设置当前颜色为绿色不透明
    # glVertex3f(-0.5, -0.366, -0.5)        # 设置三角形顶点
    # glColor4f(0.0, 0.0, 1.0, 1.0)        # 设置当前颜色为蓝色不透明
    # glVertex3f(-0.5, 0.366, -0.5)           # 设置三角形顶点
    # glColor4f(0.0, 1.0, 1.0, 0.0)        # 设置当前颜色为蓝色不透明
    # glVertex3f(0.5, 0.366, -0.5)           # 设置三角形顶点
    
    # glEnd()                              # 结束绘制三角形
    
    # ---------------------------------------------------------------
    # glFlush()                            # 清空缓冲区，将指令送往硬件立即执行
    glutSwapBuffers()

def LoadTexture():
    img = Image.open('with angle.bmp')
    width, height = img.size
    img = img.tobytes('raw', 'RGBX', 0, -1)
    
    glGenTextures(2)
    glBindTexture(GL_TEXTURE_2D, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE,img)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def mouseclick(button, state, x, y):
    global click_x, click_y, zoom_x, zoom_y, zoom_z
    click_x, click_y = x, y
    zoom_x, zoom_y, zoom_z = 1, 1, 1
    glutPostRedisplay()
    print('mouse click!!!')
    
def mousemotion(x, y):
    global angle, translate_x, translate_y, click_x, click_y
    translate_x += ((x - click_x) * 0.005)
    translate_y -= ((y - click_y) * 0.005)
    angle = 0
    glutPostRedisplay()

    click_x, click_y = x , y

if __name__ == "__main__":
    # LoadTexture()
    # glEnable(GL_TEXTURE_2D)
    # glClearDepth(1.0)
    # glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    # glutDisplayFunc(draw)
    # glutIdleFunc(draw)

    glClearColor(0.0, 0.0, 0.0, 1.0) # 设置画布背景色。注意：这里必须是4个参数
    glEnable(GL_DEPTH_TEST)          # 开启深度测试，实现遮挡关系
    glDepthFunc(GL_LEQUAL)           # 设置深度测试函数（GL_LEQUAL只是选项之一）
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear session
    glutInit()                           # 1. 初始化glut库
    glutInitWindowSize(WIN_W, WIN_H)
    glutCreateWindow('OpenGL') # 2. 创建glut窗口
    glutDisplayFunc(draw)                # 3. 注册回调函数draw()
    # glutReshapeFunc(reshape)            # 注册响应窗口改变的函数reshape()
    glutMouseFunc(mouseclick)           # 注册响应鼠标点击的函数mouseclick()
    glutMotionFunc(mousemotion)         # 注册响应鼠标拖拽的函数mousemotion()
    # glutKeyboardFunc(keydown)           # 注册键盘输入的函数keydown()

    
    LoadTexture()
    glEnable(GL_TEXTURE_2D)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    # ---
    glCullFace(GL_BACK)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glHint(GL_POINT_SMOOTH_HINT,GL_NICEST)
    glHint(GL_LINE_SMOOTH_HINT,GL_NICEST)
    glHint(GL_POLYGON_SMOOTH_HINT,GL_FASTEST)
    glLoadIdentity()
    gluPerspective(45.0, float(500)/float(500), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    glutMainLoop()                       # 4. 进入glut主循环