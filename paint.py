#At this point, there is no way to save the result into an image file.

import PyQt5 as PyQt5
from PyQt5.QtWidgets import *
import sys as sys
import _thread as thread
import os as os

def event(eventType, debug = True):
    global applicationRunning, pencolor
    eventType = str(eventType)
    if (debug):
        print (eventType)
    if (eventType == 'exitProgram'):
        applicationRunning = False
        exit()
    elif (eventType.split(':')[0] == 'setcolor'):
        pencolor = str(eventType.split(':')[1])
    elif (eventType == 'canvasClear'):
        print ('This doesnt work yet')

applicationRunning = True

application = QApplication(sys.argv)

screen = application.primaryScreen()

window = QWidget()
window.setWindowTitle('Paint')
window.setStyleSheet('QWidget{background-color:white;}')
window.setMinimumSize(500, 300)
window.setWindowIcon(PyQt5.QtGui.QIcon('paint_application_icon.png'))
window.resize((screen.size().width() / 2), (screen.size().height() / 2))

window_header_bar = QMenuBar(window)
window_header_bar.resize(window.width(), 20)

window_header_bar_widgetStyleSheet = '''
QMenu{background-color:lightgray;border:1px solid #636361;color:black;font-family:Calibri;font-size:13px;}
'''

window_header_bar_widgets_file = window_header_bar.addMenu('File')
window_header_bar_widgets_file.setGeometry(0, 0, 40, 20)
window_header_bar_widgets_file.setStyleSheet(window_header_bar_widgetStyleSheet)
window_header_bar_widgets_file.addAction('New/Clear').triggered.connect(lambda: event('canvasClear'))
window_header_bar_widgets_file.addAction('Open Image').triggered.connect(lambda: event('canvasOpenFile'))
window_header_bar_widgets_file.addAction('Exit').triggered.connect(lambda: event('exitProgram'))

window_header_bar_widgets_edit = window_header_bar.addMenu('Edit')
window_header_bar_widgets_edit.setGeometry((window_header_bar_widgets_file.x() + window_header_bar_widgets_file.width()), 0, 40, 20)
window_header_bar_widgets_edit.setStyleSheet(window_header_bar_widgetStyleSheet)

window_header_bar_widgets_edit_new_brush = window_header_bar_widgets_edit.addMenu('Brush')

window_header_bar_widgets_edit_new_brush_color = window_header_bar_widgets_edit_new_brush.addMenu('Set Color...')
window_header_bar_widgets_edit_new_brush_color.addAction('Black').triggered.connect(lambda: event('setcolor:black'))
window_header_bar_widgets_edit_new_brush_color.addAction('Gray').triggered.connect(lambda: event('setcolor:gray'))
window_header_bar_widgets_edit_new_brush_color.addAction('White').triggered.connect(lambda: event('setcolor:white'))
window_header_bar_widgets_edit_new_brush_color.addAction('Blue').triggered.connect(lambda: event('setcolor:blue'))
window_header_bar_widgets_edit_new_brush_color.addAction('Red').triggered.connect(lambda: event('setcolor:red'))
window_header_bar_widgets_edit_new_brush_color.addAction('Green').triggered.connect(lambda: event('setcolor:green'))

pencolor = 'black'

def paintEvent(x1, y1, x2, y2):
    global renderView, pencolor
    hwh = renderView.height() // 2
    hww = renderView.width() // 2
    x1 -= hww
    x2 -= hww
    y1 -= hwh
    y2 -= hwh
    a = QGraphicsLineItem(PyQt5.QtCore.QLineF(x1, y1, x2, y2))
    a.setPen(PyQt5.QtGui.QPen(eval('PyQt5.QtCore.Qt.{}'.format(pencolor))))
    renderView.scene().addItem(a)

renderView = QGraphicsView(window)
renderView.move(0, window_header_bar.height())
renderView.setScene(QGraphicsScene(window))
renderView.setSceneRect(PyQt5.QtCore.QRectF(renderView.viewport().rect()))

mousePos = False
mouseXY = ''
mouseLastXy = ''

def mouseDown(e):
    global mousePos, mouseXY
    mousePos = True
    mouseXY = (e.x(), e.y())

def mouseUp(e):
    global mousePos
    mousePos = False

def assignXY(x, y):
    global mouseXY, mouseLastXy
    mouseXY = (x, y)
    if (mouseLastXy == ''):
        mouseLastXy = (x, y)
    paintEvent(mouseXY[0], mouseXY[1], mouseLastXy[0], mouseLastXy[1])
    mouseLastXy = mouseXY

renderView.mousePressEvent = lambda e: mouseDown(e)
renderView.mouseReleaseEvent = lambda e: mouseUp(e)
renderView.mouseMoveEvent = lambda e: assignXY(e.x(), e.y())

def resizeThread():
    global applicationRunning, mouseLastXy, mousePos
    while (applicationRunning):
        window_header_bar.resize(window.width(), 20)
        renderView.resize(window.width(), (window.height() - window_header_bar.height()))
        if (mousePos == False):
            mouseLastXy = ''

thread.start_new_thread(resizeThread, ())

window.show()

application.exec_()

applicationRunning = False

#I got fed up with QPainter so I didnt use it        ;-;
