# -*- coding: utf-8 -*-

# -------------------------------------------
# quidam_01.py 三维空间的世界坐标系和三角形
# -------------------------------------------

from OpenGL.GL import *
from OpenGL.GLUT import *

def draw():

    glLoadIdentity()
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-0.8, 0.8, 1.0)
    glVertex3f(0.8, 0.8, 1.0)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.8, 0.8, 1.0)
    glVertex3f(0.8, -0.8, 1.0)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.8, -0.8, 1.0)
    glVertex3f(-0.8, -0.8, 1.0)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(-0.8, -0.8, 1.0)
    glVertex3f(-0.8, 0.8, 1.0)
    glEnd()


    # ---------------------------------------------------------------
    glBegin(GL_LINES)                    # 开始绘制线段（世界坐标系）
    
    # 以红色绘制x轴
    glColor4f(1.0, 0.0, 0.0, 1.0)        # 设置当前颜色为红色不透明
    glVertex3f(-1, 0.0, 0.0)           # 设置x轴顶点（x轴负方向）
    glVertex3f(1, 0.0, 0.0)            # 设置x轴顶点（x轴正方向）
    
    # 以绿色绘制y轴
    glColor4f(0.0, 1.0, 0.0, 1.0)        # 设置当前颜色为绿色不透明
    glVertex3f(0.0, -1, 0.0)           # 设置y轴顶点（y轴负方向）
    glVertex3f(0.0, 1, 0.0)            # 设置y轴顶点（y轴正方向）
    
    # 以蓝色绘制z轴
    glColor4f(0.0, 0.0, 1.0, 1.0)        # 设置当前颜色为蓝色不透明
    glVertex3f(0.0, 0.0, -1)           # 设置z轴顶点（z轴负方向）
    glVertex3f(0.0, 0.0, 1)            # 设置z轴顶点（z轴正方向）
    
    glEnd()                              # 结束绘制线段
    
    # ---------------------------------------------------------------
    glBegin(GL_QUADS)                # 开始绘制三角形（z轴负半区）
    
    glColor4f(1.0, 0.0, 0.0, 1.0)        # 设置当前颜色为红色不透明
    glVertex3f(+0.5, -0.366, -0.5)       # 设置三角形顶点
    glColor4f(0.0, 1.0, 0.0, 1.0)        # 设置当前颜色为绿色不透明
    glVertex3f(-0.5, -0.366, -0.5)        # 设置三角形顶点
    glColor4f(0.0, 0.0, 1.0, 1.0)        # 设置当前颜色为蓝色不透明
    glVertex3f(-0.5, 0.366, -0.5)           # 设置三角形顶点
    glColor4f(0.0, 1.0, 1.0, 0.0)        # 设置当前颜色为蓝色不透明
    glVertex3f(0.5, 0.366, -0.5)           # 设置三角形顶点
    
    glEnd()                              # 结束绘制三角形
    
    # ---------------------------------------------------------------
    glFlush()                            # 清空缓冲区，将指令送往硬件立即执行

if __name__ == "__main__":
    glClearColor(0.0, 0.0, 0.0, 1.0) # 设置画布背景色。注意：这里必须是4个参数
    glEnable(GL_DEPTH_TEST)          # 开启深度测试，实现遮挡关系
    glDepthFunc(GL_LEQUAL)           # 设置深度测试函数（GL_LEQUAL只是选项之一）
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear session
    glutInit()                           # 1. 初始化glut库
    glutInitWindowSize(500, 500)
    glutCreateWindow('Quidam Of OpenGL') # 2. 创建glut窗口
    glutDisplayFunc(draw)                # 3. 注册回调函数draw()
    glutMainLoop()                       # 4. 进入glut主循环