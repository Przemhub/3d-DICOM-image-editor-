import pydicom
import sys
import matplotlib.image as mpimg
import math
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import json

magic_variable = {}
load_bool = False
class ImageWidget(QWidget):
    def __init__(self, sliderPointer, statusBarPointer, active_button, output, sliderPrecisionPointer):
        super().__init__()
        self.activeButton = active_button
        self.output = output
        self.output_list = []
        self.list_blue = []
        self.list_red = []
        self.list_of_lines_blue = []
        self.list_of_lines_red = []
        self.precision = 50

        self.sliderPrecisionPointer = sliderPrecisionPointer
        self.mouse_pressed = False
        self.mouse_right_pressed = False
        self.sliderPointer = sliderPointer
        self.statusBar = statusBarPointer
        self.file_extension = ".jpg"
        self.R_MIN = 0
        self.R_MAX = 0
        self.zoom = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.draw_x = 0
        self.draw_y = 0
        self.sliderPointer.setMinimum(0)
        self.sliderPointer.setMaximum(0)
        self.sliderPointer.setValue(0)
        self.sliderPointer.valueChanged.connect(self.valueChange)

        self.sliderPrecisionPointer.setMinimum(10)
        self.sliderPrecisionPointer.setMaximum(100)
        self.sliderPrecisionPointer.setValue(50)
        self.sliderPrecisionPointer.setTickInterval(10)
        self.sliderPrecisionPointer.setTickPosition(QSlider.TicksBelow)
        self.sliderPrecisionPointer.valueChanged.connect(
            self.valueChangePrecision)
        self.rows = 0
        self.cols = 0
        self.format = QtGui.QImage.Format_Grayscale8
        self.dataset = mpimg.imread('start.png')
        self.image = QtGui.QImage()
        self.image.load("start.png")
        self.rows = int(len(self.dataset))
        self.cols = self.rows
        # self.image = QtGui.QImage(
        #    self.dataset, self.rows, self.cols, QtGui.QImage.Format_RGB32)
        self.windowWidth = int(self.frameGeometry().width())
        self.windowHeight = int(self.frameGeometry().height())
        self.setMouseTracking(True)
        policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(policy)
        self.setAcceptDrops(True)
   # def saveImage(self):

    def valueChange(self):
        self.zoom = self.sliderPointer.value()
        self.updateImage()

    def valueChangePrecision(self):
        self.precision = self.sliderPrecisionPointer.value()

    def updateImage(self):
        if(self.file_extension.lower() == ".dcm"):
            self.image = QtGui.QImage(
                self.dataset.pixel_array[self.zoom], self.rows, self.cols, self.format)
            self.statusBar.showMessage(
                "Layer: " + str(self.zoom+1) + ", Coordinates: (x:"+str(self.mouse_x)+", y:"+str(self.mouse_y)+")")

        elif(self.file_extension == ".png"):
            self.image = QtGui.QImage(
                self.dataset, self.rows, self.cols, QtGui.QImage.Format_RGB32)
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(self.draw_x, self.draw_y, self.image)
        self.drawOnImage(
            painter, self.zoom, self.draw_x)
        painter.end()

    def wheelEvent(self, event):
        self.zoom += int(event.angleDelta().y()/100)
        if(self.zoom < self.R_MIN):
            self.zoom = self.R_MIN
        if(self.zoom > self.R_MAX):
            self.zoom = self.R_MAX
        self.updateImage()
        self.sliderPointer.setValue(self.zoom)

    def mouseMoveEvent(self, event):
        global magic_variable
        global load_bool
        if load_bool == True:
            if magic_variable.keys().__contains__("red"):
                self.list_of_lines_red = magic_variable["red"]
            if magic_variable.keys().__contains__("blue"):
                self.list_of_lines_blue = magic_variable["blue"]

            for line in self.list_of_lines_red:
                for point in line:
                    tmp = QListWidgetItem((str(point[0]) + ", " + str(point[1]) + ", ") + str(point[2]))
                    tmp.setForeground(QtGui.QColor("red"))
                    self.output.addItem(tmp)
                    self.output_list.append(point)
            for line in self.list_of_lines_blue:
                for point in line:
                    tmp = QListWidgetItem((str(point[0]) + ", " + str(point[1]) + ", ") + str(point[2]))
                    tmp.setForeground(QtGui.QColor("blue"))
                    self.output.addItem(tmp)
                    self.output_list.append(point)
            if magic_variable.keys().__contains__("red"):
                print(1)
                magic_variable.pop("red")
                print(2)
            if magic_variable.keys().__contains__("blue"):
                magic_variable.pop("blue")
            load_bool = False

        self.mouse_x = event.x()-self.draw_x
        self.mouse_y = event.y()-self.draw_x
        QApplication.restoreOverrideCursor()

        if self.mouse_right_pressed == True:
            if len(self.list_of_lines_red) > 0 and self.activeButton[0] == 1:
                temp = []
                for line in self.list_of_lines_red:
                    # print(self.list_of_lines_red)
                    # print(line)

                    for i in range(1, len(line)):
                        points = self.get_line((line[i-1][0],line[i-1][1]),(line[i][0],line[i][1]))

                        for point in points:
                            if (self.mouse_x <= point[0] + 5 and self.mouse_x >= point[0] - 5) and (self.mouse_y <= point[1] + 5 and self.mouse_y >= point[1] - 5):
                                if self.mouse_right_pressed == True:
                                    if i == 1: # if first line
                                        temp.append(self.list_of_lines_red.index(line))
                                        temp.append(line[0])
                                        # print(temp)
                                    elif i == len(line)-1:
                                        temp.append(self.list_of_lines_red.index(line))
                                        # print(temp)
                                        temp.append(line[i])
                                        break
            if len(self.list_of_lines_blue) > 0 and self.activeButton[0] == 2:
                temp = []
                for line in self.list_of_lines_blue:
                    # print(self.list_of_lines_red)
                    # print(line)
                    for i in range(1, len(line)):
                        points = self.get_line((line[i - 1][0], line[i - 1][1]), (line[i][0], line[i][1]))

                        for point in points:
                            if (self.mouse_x <= point[0] + 5 and self.mouse_x >= point[0] - 5) and (
                                    self.mouse_y <= point[1] + 5 and self.mouse_y >= point[1] - 5):
                                if self.mouse_right_pressed == True:
                                    if i == 1:  # if first line
                                        temp.append(self.list_of_lines_blue.index(line))
                                        temp.append(line[0])
                                        # print(temp)
                                    elif i == len(line) - 1:
                                        temp.append(self.list_of_lines_blue.index(line))
                                        # print(temp)
                                        temp.append(line[i])
                                    break

            if (self.activeButton[0] == 1 or self.activeButton[0] == 2):
                if len(temp) > 0:
                    if self.activeButton[0] == 1:
                        self.list_of_lines_red[temp[0]].remove(temp[1])
                    elif self.activeButton[0] == 2:
                        self.list_of_lines_blue[temp[0]].remove(temp[1])
                    self.output.takeItem(self.output_list.index(temp[1]))
                    self.output_list.remove(temp[1])
                    if self.activeButton[0] == 1:
                        if len(self.list_of_lines_red[temp[0]]) == 1:
                            self.output.takeItem(self.output_list.index(self.list_of_lines_red[temp[0]][0]))
                            self.output_list.remove(self.list_of_lines_red[temp[0]][0])
                            self.list_of_lines_red[temp[0]].clear()
                    if self.activeButton[0] == 2:
                        if len(self.list_of_lines_blue[temp[0]]) == 1:
                            self.output.takeItem(self.output_list.index(self.list_of_lines_blue[temp[0]][0]))
                            self.output_list.remove(self.list_of_lines_blue[temp[0]][0])
                            self.list_of_lines_blue[temp[0]].clear()
                    temp.clear()

        if self.mouse_pressed:
            #self.mouse(x1, y1, self.zoom)
            dist = math.sqrt((self.mouse_x - self.start_x) **
                             2 + (self.mouse_y - self.start_y)**2)
            if dist > self.precision:
                self.mouse(self.mouse_x, self.mouse_y, self.zoom)
                self.start_x = self.mouse_x
                self.start_y = self.mouse_y
        self.statusBar.showMessage(
            "Layer: " + str(self.zoom+1) + ", Coordinates: (x:"+str(self.mouse_x)+", y:"+str(self.mouse_y)+")")

    def resizeEvent(self, event):
        self.windowWidth = int(self.frameGeometry().width())
        self.windowHeight = int(self.frameGeometry().height())
        self.draw_x = (self.windowHeight-self.rows)//2
        self.draw_y = self.draw_x
        self.updateImage()
        self.setMinimumWidth(self.windowHeight)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ingore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        self.changeImage(urls[0].toLocalFile())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse(self.mouse_x, self.mouse_y, self.zoom)
            self.start_x = self.mouse_x
            self.start_y = self.mouse_y
            self.mouse_pressed = True
        if event.button() == Qt.RightButton:
            self.mouse_right_pressed = True

    def mouseReleaseEvent(self, event):

        if self.activeButton[0] == 1 and self.mouse_right_pressed == False:
            self.list_of_lines_red.append(self.list_red.copy())
            self.list_red.clear()
        elif self.mouse_right_pressed == False:
            self.list_of_lines_blue.append(self.list_blue.copy())
            self.list_blue.clear()
        # print(self.list_of_lines_red)
        # print("relese")
        self.mouse_pressed = False
        self.mouse_right_pressed = False

    def changeImage(self, fileName):
        self.file_extension = fileName[(fileName.rfind(".")):]
        self.dataset = pydicom.dcmread(fileName)
        self.format = QtGui.QImage.Format_Grayscale8
        for i in self.dataset.pixel_array[0]:
            for j in i:
                if(j > 255):
                    self.format = QtGui.QImage.Format_Grayscale16
                    break

        self.clearOutput()
        self.R_MAX = len(self.dataset.pixel_array)-1
        self.rows = int(self.dataset.Rows)
        self.cols = int(self.dataset.Columns)
        self.zoom = 0
        self.sliderPointer.setMinimum(self.R_MIN)
        self.sliderPointer.setMaximum(self.R_MAX)
        self.sliderPointer.setValue(self.R_MIN)
        self.draw_x = (self.windowHeight-self.rows)//2
        self.draw_y = self.draw_x
        self.updateImage()

    def get_line(self, start, end):

        # Setup initial conditions
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1

        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)

        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Swap start and end points if necessary and store swap state
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True

        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1

        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        # Reverse the list if the coordinates were swapped
        if swapped:
            points.reverse()
        return points

    def mouse(self, x, y, z):
        # print(x, y, z)
        # print(self.activeButton[0])
        if self.activeButton[0] == 1:
            tmp = QListWidgetItem((str(x)+", "+str(y)+", ")+str(z))
            tmp.setForeground(QtGui.QColor("red"))
            #print(x, y, z)
            self.output.addItem(tmp)
            self.output_list.append([x,y,z])
            self.list_red.append([x, y, z])

        elif self.activeButton[0] == 2:
            tmp = QListWidgetItem((str(x)+", "+str(y)+", ")+str(z))
            tmp.setForeground(QtGui.QColor("blue"))
            self.output.addItem(tmp)
            self.output_list.append([x,y,z])
            self.list_blue.append([x, y, z])

    def drawOnImage(self, painter, layer, offset):
        for j in self.list_of_lines_red:
            if(len(j) > 0):
                painter.setPen(QPen(QColor(255, 0, 0),2))
                for i in range(1, len(j)):
                    x1, y1, z1 = j[i-1]
                    x2, y2, z2 = j[i]
                    if layer == z1:
                        points = self.get_line((x1, y1), (x2, y2))
                        for i in points:
                            x, y = i
                            painter.drawPoint(x+offset, y+offset)

        for j in self.list_of_lines_blue:
            if(len(j) > 0):
                painter.setPen(QPen(QColor(0, 0, 255),2))
                for i in range(1, len(j)):
                    x1, y1, z1 = j[i-1]
                    x2, y2, z2 = j[i]
                    if layer == z1:
                        points = self.get_line((x1, y1), (x2, y2))
                        for i in points:
                            x, y = i
                            painter.drawPoint(x+offset, y+offset)

        if(len(self.list_red) > 0):
            painter.setPen(QPen(QColor(255, 0, 0),2))
            for i in range(1, len(self.list_red)):
                x1, y1, z1 = self.list_red[i-1]
                x2, y2, z2 = self.list_red[i]
                if layer == z1:
                    points = self.get_line((x1, y1), (x2, y2))
                    for i in points:
                        x, y = i
                        painter.drawPoint(x+offset, y+offset)

        if(len(self.list_blue) > 0):
            painter.setPen(QPen(QColor(0, 0, 255),2))
            for i in range(1, len(self.list_blue)):
                x1, y1, z1 = self.list_blue[i-1]
                x2, y2, z2 = self.list_blue[i]
                if layer == z1:
                    points = self.get_line((x1, y1), (x2, y2))
                    for i in points:
                        x, y = i
                        painter.drawPoint(x+offset, y+offset)
        if len(self.list_of_lines_red) > 0:
            magic_variable["red"] = self.list_of_lines_red
        if len(self.list_of_lines_blue) > 0:
            magic_variable["blue"] = self.list_of_lines_blue
        self.update()

    def clearOutput(self):
        self.output.clear()
        self.list_blue.clear()
        self.list_red.clear()
        self.list_of_lines_red.clear()
        self.list_of_lines_blue.clear()


class MainWidget(QWidget):
    def __init__(self, statusBarPointer):
        super().__init__()

        self.sl = QSlider()
        self.sl.setOrientation(Qt.Vertical)

        self.sl2 = QSlider()
        self.sl2.setOrientation(Qt.Horizontal)

        self.listwidget = QListWidget()
        self.buttonStatus = [0, ]
        self.iw = ImageWidget(self.sl, statusBarPointer,
                              self.buttonStatus, self.listwidget, self.sl2)
        self.button_object = QPushButton("Object marker")
        self.button_object.clicked.connect(self.objectMarker)
        self.button_base = QPushButton("Base marker")
        self.button_base.clicked.connect(self.baseMarker)
        layout = QHBoxLayout()
        layout.addWidget(self.sl)
        layout.addWidget(self.iw)
        layout_buttons = QVBoxLayout()
        layout.addLayout(layout_buttons)
        layout_buttons.addWidget(self.button_object)
        layout_buttons.addWidget(self.button_base)
        layout_buttons.addWidget(self.listwidget)
        layout_buttons.addWidget(QLabel("Precision:"))
        layout_buttons.addWidget(self.sl2)
        self.setLayout(layout)
        layout_buttons.setSizeConstraint(QLayout.SetFixedSize)
        layout_buttons.setContentsMargins(0, 0, 0, 0)

    def changeImage(self, filename):
        self.iw.changeImage(filename)

    def objectMarker(self):
        if self.buttonStatus[0] == 1:
            self.buttonStatus[0] = 0
        else:
            self.buttonStatus[0] = 1

    def baseMarker(self):
        if self.buttonStatus[0] == 2:
            self.buttonStatus[0] = 0
        else:
            self.buttonStatus[0] = 2


class MainWindow(QMainWindow):
    def  __init__(self):
        super().__init__()
        self.is_running = True
        self.setStyleSheet(open('style.qss').read())
        grid = QGridLayout()
        # self.setLayout(grid)
        self.setWindowTitle("Dcm viewer")
        self.filename = ""
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.mainWidget = MainWidget(self.statusBar)
        self.setCentralWidget(self.mainWidget)

        menubar = QMenuBar()
        self.setMenuBar(menubar)
        menuFile = menubar.addMenu('&File')
        menuEdit = menubar.addMenu('&Edit')
        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(qApp.quit)
        openFileAction = QAction("Open", self)
        openFileAction.triggered.connect(self.openFileNameDialog)
        saveFileAction = QAction("Save",self)
        saveFileAction.triggered.connect(self.saveFileDialog)
        loadFileAction = QAction("Load Project", self)
        loadFileAction.triggered.connect(self.loadFileDialog)
        settingsAction = QAction("Settings", self)
        menuFile.addAction(openFileAction)
        menuFile.addAction(loadFileAction)
        menuFile.addAction(saveFileAction)
        menuFile.addAction(exitAction)
        menuEdit.addAction(settingsAction)
        # self.setMinimumSize(600, 400)
        # self.setFixedSize(700, 560)
        self.resize(700, 520)
        self.show()

    def closeEvent(self, event):
        self.is_running = False

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            magic_variable["filename"] = fileName
            self.mainWidget.changeImage(fileName)


    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(
            self, "QFileDialog.getOpenFileNames()", "", "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
    def loadFileDialog(self):
        global magic_variable
        global load_bool
        fName, ok = QInputDialog.getText(self, "Load Project", "Load File:", QLineEdit.Normal, "")
        if ok == True:
            file = open("Saves/" + fName + ".json", 'r')
            magic_variable = json.load(file)
            load_bool = True
            file.close()
            self.mainWidget.changeImage(magic_variable["filename"])

    def saveFileDialog(self):
        fName,ok = QInputDialog.getText(self, "Save Project", "Save File:", QLineEdit.Normal, "")
        if ok==True:
            file = open("Saves/" + fName + ".json", 'w')
            json.dump(magic_variable, file)
            file.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


