
import sys
from PySide2 import QtCore, QtGui, QtWidgets, QtOpenGL

from OpenGL.GL import *

# import textures_rc


class GLWidget(QtOpenGL.QGLWidget):


    coords = (
        ( ( +1, -1, -1 ), ( -1, -1, -1 ), ( -1, +1, -1 ), ( +1, +1, -1 ) ),
        ( ( +1, +1, -1 ), ( -1, +1, -1 ), ( -1, +1, +1 ), ( +1, +1, +1 ) ),
        ( ( +1, -1, +1 ), ( +1, -1, -1 ), ( +1, +1, -1 ), ( +1, +1, +1 ) ),
        ( ( -1, -1, -1 ), ( -1, -1, +1 ), ( -1, +1, +1 ), ( -1, +1, -1 ) ),
        ( ( +1, -1, +1 ), ( -1, -1, +1 ), ( -1, -1, -1 ), ( +1, -1, -1 ) ),
        ( ( -1, -1, +1 ), ( +1, -1, +1 ), ( +1, +1, +1 ), ( -1, +1, +1 ) )
    )

    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        
    
    def loadGLTextures(self):
        pass

    # def minimumSizeHint(self):
    #     return QtCore.QSize(50, 50)

    # def sizeHint(self):
    #     return QtCore.QSize(200, 200)
    
    def initializeGL(self):

        # glLoadIdentity()
        # glTranslated(0.0, 0.0, -10.0)

        self.textures = []
        self.textures.append(self.bindTexture(QtGui.QPixmap("./aaa.jpeg")))
        tex = self.textures[0]
        glGenTextures(1,self.textures[0])
        glBindTexture(GL_TEXTURE_2D, self.textures[0])

        # 平滑效果处理
        # glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
        # glEnable(GL_DEPTH_TEST)
        # glEnable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)
    
    def paintGL(self):
        # for i in range(6):
        glBindTexture(GL_TEXTURE_2D, self.textures[0])

        glBegin(GL_QUADS)
        i = 0
        for j in range(4):
            tx = {False: 0, True: 1}[j == 0 or j == 3]
            ty = {False: 0, True: 1}[j == 0 or j == 1]
            # print(tx, ty)
            glTexCoord2d(tx, ty)
            # print(2 * GLWidget.coords[i][j][0],
            #             2 * GLWidget.coords[i][j][1],
            #             2 * GLWidget.coords[i][j][2])
            glVertex3d(1 * GLWidget.coords[i][j][0],
                        1 * GLWidget.coords[i][j][1],
                        1 * GLWidget.coords[i][j][2])

        glEnd()
    
    # def resizeGL(self, width, height):
    #     side = min(width, height)
    #     glViewport(int((width - side) / 2), int((height - side) / 2), side, side)

    #     glMatrixMode(GL_PROJECTION)
    #     glLoadIdentity()
    #     glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
    #     glMatrixMode(GL_MODELVIEW)
    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GLWidget()
    window.show()
    sys.exit(app.exec_())
