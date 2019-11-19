
import sys
from PySide2 import QtCore, QtGui, QtWidgets, QtOpenGL

from OpenGL.GL import *
from OpenGL.GLUT import *

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
        self.textures = QtGui.QImage('123.png')
        self.tex_width = self.textures.width()
        self.tex_height = self.textures.height()
        self.tex_prt = self.textures.bits()

        self._imageTextureID = glGenTextures(1)
        print(self._imageTextureID)

        glBindTexture(GL_TEXTURE_2D, self._imageTextureID) 
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.tex_width, self.tex_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.tex_prt)

        # glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )

        
    
    def initializeGL(self):
        self.loadGLTextures()
        glutInitWindowSize(500, 500)
        glEnable( GL_TEXTURE_2D )
    
    def paintGL(self):
        # for i in range(6):
        glBindTexture(GL_TEXTURE_2D, self._imageTextureID)

        glBegin(GL_QUADS)
        i = 0
        # for j in range(4):
        #     tx = {False: 0, True: 1}[j == 0 or j == 3]
        #     ty = {False: 0, True: 1}[j == 0 or j == 1]

        #     glTexCoord2d(tx, ty)
        #     glVertex3d(1 * GLWidget.coords[i][j][0],
        #                 1 * GLWidget.coords[i][j][1],
        #                 1 * GLWidget.coords[i][j][2])
        glTexCoord2d(1, 1)
        glVertex3f(+1, -1, -1)       # 设置三角形顶点
        glTexCoord2d(0, 1)
        glVertex3f(-1, -1, -1)        # 设置三角形顶点
        glTexCoord2d(0, 0)
        glVertex3f(-1, 1, -1)           # 设置三角形顶点
        glTexCoord2d(1, 0)
        glVertex3f(1, 1, -1)           # 设置三角形顶点

        glEnd()
    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GLWidget()
    window.show()
    sys.exit(app.exec_())
