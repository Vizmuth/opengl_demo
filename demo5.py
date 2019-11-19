import sys
from PySide2 import QtCore, QtGui, QtWidgets, QtOpenGL

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image
import numpy as np
import cv2
import matplotlib.cm as cm

import joblib


class OpenGLShow(QtOpenGL.QGLWidget):
    def __init__(self, parent=None, file_path='', compensate_height=0, container=None, max_val=0, min_val=0):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.file_path = file_path
        self.container = container
        self.compensate_height = compensate_height

        self.translate_x, self.translate_y = 0, 0
        self.click_x, self.click_y = 0, 0
        self.angle = 0
        # x,y,z zoom Number
        self.zoom_x, self.zoom_y, self.zoom_z = 1, 1, 1
        # now zoom Number
        self.zoom_num = 0

        # 图片被点住(鼠标左键)标志位
        self.isLeftPressed = bool(False)
        # Moving speed
        self.movingSpeed = 0.0013

        self.zoom_x_default, self.zoom_y_default = 1, 1

        self.img_width, self.img_height = 0, 0
        self.max_val, self.min_val = max_val, min_val
        self.default_max_val, self.default_min_val = 0, 0

        self.tex_id = 2
        

    def loadPicture(self):
        res = joblib.load('0_1.pkl')
        # res = np.fft.ifft(res, axis=-1)
        res_abs = np.abs(res)
        # normalize
        # TODO: clip with dynamic range
        res_n = (res_abs - res_abs.min()) / (res_abs.max() - res_abs.min())
        res_rgb = (cm.hot(res_n) * 255).astype(np.uint8)  # TODO: choose colormap: gray, hot etc
        self.img_width, self.img_height = res_rgb.shape[1], res_rgb.shape[0]
        img = res_rgb.tobytes()
        return img
        # img = Image.open(self.file_path)
        # self.img_width, self.img_height = img.size
        # img = img.tobytes('raw', 'RGBX', 0, -1)
        # # print(self.container)
        # self.syncNavigationInfo()
        # return img
    
    # def syncNavigationInfo(self):
    #     self.container['info_value']['set_width'].setText(str(self.img_width))
    #     self.container['info_value']['set_height'].setText(str(self.img_height))
    #     self.container['info_value']['set_max_val'].setText(str(self.max_val))
    #     self.container['info_value']['set_min_val'].setText(str(self.min_val))

    #     self.container['info_value']['set_max_val'].setPlaceholderText(str(self.default_max_val))
    #     self.container['info_value']['set_min_val'].setPlaceholderText(str(self.default_min_val))
    
    def loadGLTextures(self):
        # img = self.loadPicture()
        # single_tex = SingleTex()
        # # single_tex.setTex(img)
        # single_tex.setInit(img, self.img_width, self.img_height)
        # self.tex_id = single_tex.tex_ids[1]
        # print('loadGL right', single_tex.tex_ids, self.tex_id)

        img = self.loadPicture()
        glGenTextures(1, self.tex_id)
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, self.img_width, self.img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
        # glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self.img_width, self.img_height, GL_RGBA, GL_UNSIGNED_BYTE, img)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    def initializeGL(self):
        self.loadGLTextures()
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glHint(GL_POINT_SMOOTH_HINT,GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT,GL_NICEST)
        glHint(GL_POLYGON_SMOOTH_HINT,GL_FASTEST)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, 0.0, 10.0)
        glMatrixMode(GL_MODELVIEW)
        

    def paintGL(self):
        glClearColor(0.5, 0.5, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.makeTexture()
        self.syncNavigation()

    def makeTexture(self):
        print('make', self.tex_id)
        self.x, self.y = self.paint_ratio()
        
        glLoadIdentity()
        glTranslate(0, 0, -5.0)
        glRotate(0, 0, 0, 0.0)
        glScaled(1,1,1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glBegin(GL_LINES)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1, 1, 1.0)
        glVertex3f(1, 1, 1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1, 1, 1.0)
        glVertex3f(1, -1, 1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1, -1, 1.0)
        glVertex3f(-1, -1, 1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1, -1, 1.0)
        glVertex3f(-1, 1, 1.0)
        glEnd()

        glLoadIdentity()
        #沿z轴平移
        if self.x < self.y:
            ratio_y = self.width() / self.height()
            self.zoom_x_default = 1
            self.zoom_y_default = ratio_y
            self.zoom_y = ratio_y if self.zoom_y == 1 else self.zoom_y
            self.zoom_x = 1 if self.zoom_y == self.zoom_y_default else self.zoom_x
            glTranslated(self.translate_x, self.translate_y*ratio_y, -5.0)
            glScaled(self.zoom_x, self.zoom_y, self.zoom_z)
            glRotatef(self.angle, 0, 0, -1.0)
            self.y /= ratio_y
        else:
            ratio_x = self.height() / self.width()
            self.zoom_x_default = ratio_x
            self.zoom_y_default = 1
            self.zoom_x = ratio_x if self.zoom_x == 1 else self.zoom_x
            self.zoom_y = 1 if self.zoom_x == self.zoom_x_default else self.zoom_y
            glTranslated(self.translate_x*ratio_x, self.translate_y, -5.0)
            glScaled(self.zoom_x, self.zoom_y, self.zoom_z)
            glRotatef(self.angle, 0, 0, -1.0)
            self.x /= ratio_x
        # glTranslated(self.translate_x, self.translate_y, -5.0)
        # glScaled(self.zoom_x, self.zoom_y, self.zoom_z)
        # glRotatef(self.angle, 0, 0, -1.0)
        #开始绘制立方体的每个面，同时设置纹理映射
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        #绘制四边形
        glBegin(GL_QUADS)
        #设置纹理坐标
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-self.x, -self.y, 1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(self.x, -self.y, 1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(self.x, self.y, 1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-self.x, self.y, 1.0)
        glEnd()

    def resizeGL(self, w, h):
        glViewport(0, self.compensate_height, self.win_width(), self.win_height())
        self.syncNavigation()
        # self.paintGL()
        # self.updateGL()

    def get_transform(self):
        a = (GLfloat * 16)()
        mvm = glGetFloatv(GL_MODELVIEW_MATRIX, a)
        return np.array(list(a)).reshape(4, 4)

    def cursor_to_canvas(self, cursor_x, cursor_y):
        width = self.width()
        height = self.height()
        src_points = np.float32([
            [0, 0],
            [0, height],
            [width, height],
        ])
        dst_points = np.float32([
            [-1, 1],
            [-1, -1],
            [1, -1],
        ])
        click_canvas = cv2.getAffineTransform(src_points, dst_points)
        canvas_coords = click_canvas @ np.array([cursor_x, cursor_y, 1])
        return canvas_coords


    def win_width(self):
        return self.width()

    def win_height(self):
        return self.height() - self.compensate_height
    
    def paint_ratio(self):
        win_width = self.win_width()
        win_height = self.win_height()
        paint_width, paint_height = self.resizePicture()
        paint_width_ratio = paint_width / win_width
        paint_height_ratio = paint_height / win_height

        return paint_width_ratio, paint_height_ratio

    '''重载一下鼠标按下事件(单击)'''
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:                            # 左键按下
            print("鼠标左键单击")  # 响应测试语句
            self.isLeftPressed = True;                                         # 左键按下(图片被点住),置Ture
            self.click_x, self.click_y = event.x(), event.y()                  # 获取鼠标当前位置
            canvas_coords = self.cursor_to_canvas(self.click_x, self.click_y)
            transform = self.get_transform()
            print('inv mapping test', canvas_coords, np.array([[canvas_coords[0], canvas_coords[1], -5, 1]]) @ np.linalg.inv(transform))

    '''重载一下鼠标键公开事件'''
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:                            # 左键释放
            self.isLeftPressed = False;  # 左键释放(图片被点住),置False
            print("鼠标左键松开")  # 响应测试语句
        elif event.button() == QtCore.Qt.RightButton:                                 # 右键释放
            self.emptyPaint()
            print("鼠标右键松开")  # 响应测试语句
    
    '''重载一下鼠标移动事件'''
    def mouseMoveEvent(self,event):
        if self.isLeftPressed:                                                   # 左键按下
            self.translate_x += ((event.x() - self.click_x) * self.movingSpeed)             # 更新偏移量 x
            self.translate_y -= ((event.y() - self.click_y) * self.movingSpeed)             # 更新偏移量 y
            self.syncNavigation()
            self.updateGL()                                                      # 重绘
            self.click_x, self.click_y = event.x(), event.y()                    # 更新当前鼠标在窗口上的位置，下次移动用

    '''重载一下滚轮滚动事件'''
    def wheelEvent(self, event):
        angle=event.angleDelta() / 8                                           # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        angleY=angle.y()                                                       # 竖直滚过的距离
        
        if angleY > 0:                                                        # 滚轮上
            self.zoomInPicture(event)
        else:                                                                  # 滚轮下滚
            self.zoomOutPicture(event)

    def zoomInPicture(self, event=None):
        before = self.get_transform()
        if self.zoom_x < 40:
            self.zoom_x += float(self.zoom_x_default) * 0.1
            self.zoom_y += float(self.zoom_y_default) * 0.1

            anchor = self.cursor_to_canvas(float(event.x()), float(event.y()))
            after = before.copy()
            after[:3, :] *= np.array([self.zoom_x / (self.zoom_x - 0.1), self.zoom_y / (self.zoom_y - 0.1), 1, 1]).reshape(1, 4)
            extra_translate = (np.array([anchor[0], anchor[1], -5, 1]).reshape(1, 4)) @ (np.eye(4) - np.linalg.inv(before) @ after)  # TODO: fix -5
            self.translate_x += extra_translate[0][0]
            self.translate_y += extra_translate[0][1]
            
            self.syncNavigation()
            self.updateGL()

    def zoomOutPicture(self, event=None):
        before = self.get_transform()
        if self.zoom_x > 0.5:
            self.zoom_x -= float(self.zoom_x_default) * 0.1
            self.zoom_y -= float(self.zoom_y_default) * 0.1

            anchor = self.cursor_to_canvas(float(event.x()), float(event.y()))
            after = before.copy() 
            after[:3, :] *= np.array([self.zoom_x / (self.zoom_x + 0.1), self.zoom_y / (self.zoom_y + 0.1), 1, 1]).reshape(1, 4)
            extra_translate = (np.array([anchor[0], anchor[1], -5, 1]).reshape(1, 4)) @ (np.eye(4) - np.linalg.inv(before) @ after)  # TODO: fix -5
            self.translate_x += extra_translate[0][0]
            self.translate_y += extra_translate[0][1]

            self.syncNavigation()
            self.updateGL()

    
    def resizePicture(self, parent_width=0, parent_height=0):
        if not parent_width or not parent_height:
            parent_width = self.win_width()
            parent_height = self.win_height()

        wratio = self.img_width * 1.0 / parent_width
        hratio = self.img_height * 1.0 / parent_height
        
        if self.img_width > parent_width or self.img_height > parent_height:
            if wratio > hratio:
                parent_height = self.img_height / wratio
            else:
                parent_width = self.img_width / hratio
        else:
            parent_height = self.img_height
            parent_width = self.img_width
        return int(parent_width), int(parent_height)


    def rotatePicture(self, angle):
        self.angle = angle
        self.syncNavigation()
        self.max_val = 1.428705e-05
        self.reloadNavigationGLTextures()
        self.updateGL()
    
    def updatePicture(self, old_picture):
        self.translate_x, self.translate_y = old_picture.translate_x, old_picture.translate_y
        self.angle = old_picture.angle
        # x,y,z zoom Number
        self.zoom_x, self.zoom_y, self.zoom_z = old_picture.zoom_x, old_picture.zoom_y, old_picture.zoom_z
        self.updateGL()
    
    def emptyPaint(self):
        self.translate_x, self.translate_y = 0, 0
        self.click_x, self.click_y = 0, 0
        self.angle = 0
        # x,y,z zoom Number
        self.zoom_x, self.zoom_y, self.zoom_z = self.zoom_x_default, self.zoom_y_default, 1
        # now zoom Number
        self.zoom_num = 0
        # 图片被点住(鼠标左键)标志位
        self.isLeftPressed = bool(False)
        self.syncNavigation()
        self.updateGL()
    
    def syncNavigation(self):
        paint_w, paint_h = self.paint_ratio()
        # self.container['image_navigation'].updateBorder(
        #     zoom_x=self.zoom_x, zoom_y=self.zoom_y, 
        #     zoom_x_default=self.zoom_x_default, zoom_y_default=self.zoom_y_default,
        #     translate_x=self.translate_x, translate_y=self.translate_y,
        #     paint_w=paint_w, paint_h=paint_h, angle=self.angle)
    
    def updateTranslate(self, translate_x, translate_y, navigation_img_width, navigation_img_height):
        paint_w, paint_h = self.paint_ratio()
        self.translate_x = -(translate_x * (paint_w / navigation_img_width) * self.zoom_x)
        self.translate_y = -(translate_y * (paint_h / navigation_img_height) * self.zoom_x)
        self.updateGL()
    
    def reloadNavigationGLTextures(self):
        pass

    def reloadTextures(self):
        pass



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = OpenGLShow(file_path='../test_data/123.jpg')
    # window = MainWindow()
    window.show()
    sys.exit(app.exec_())
