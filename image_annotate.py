# -*- coding: utf-8 -*-

import sys
import os
import cv2
import numpy as np
from scipy import interpolate
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
sys.setrecursionlimit(1000000)

class MainWindow(QMainWindow):
    def __init__(self, img_path, save_path):
        super(QMainWindow, self).__init__()

        self.init_widgets()
        self.init_vars()



        self.path_init(img_path, save_path)
        self.init_ui()
        self.load_img()
        self.event_set()
        self.bounding_box()

    def init_vars(self):
        # mem var
        self.ori_img = None

        self.point1 = (0, 0)
        self.point2 = (0, 0)
        self.bounding_coor = None
        self.bounding_img = None

        self.point_list_zoom = []
        # self.point_list_ori = []
        self.fitting_point_list = []
        self.zoom_ratio = 8
        self.zoomCombo.setCurrentText('8')
        self.radius = 12
        self.radiusCombo.setCurrentText('12')
        self.bounding_winna = 'bounding'
        self.ori_winna = 'ori'
        self.point_winna = 'point'
        self.fitting_winna = 'fitting'
        # interploate kind
        self.interploate_kind = 'slinear'
        self.interploateCombo.setCurrentText('slinear')
        self.fitting_flag = 0
        self.bounding_flag = 0
        self.point_flag = 0
        # img
        self.fitting_img = None
        self.label_img = None
        # path
        self.save_path = None
        self.save_file_name = 'label1.png'
        self.img_dir = None
        self.img_file = None
        self.file_list = None
        self.current_index = None

    def init_widgets(self):
        self.showWidget = QWidget()
        # left sub window
        self.dirUpdate = QPushButton('update', self.showWidget)
        self.totalLabel = QLabel(self.showWidget)
        self.currentLabel = QLabel(self.showWidget)

        self.dirLE = QLineEdit(self.showWidget)
        self.totalNum = QLabel(self.showWidget)
        self.currentNum = QLabel(self.showWidget)

        self.previousBT = QPushButton('previous', self.showWidget)
        self.nextBT = QPushButton('next', self.showWidget)

        self.saveBT = QPushButton('save', self.showWidget)
        self.quitBT = QPushButton('quit', self.showWidget)

        # right
        # right up
        self.interploateLabel = QLabel(self.showWidget)
        self.interploateCombo = QComboBox(self.showWidget)
        self.interploateCombo.addItems(['slinear', 'quadratic', 'cubic'])

        self.zoomLabel = QLabel(self.showWidget)
        self.zoomCombo = QComboBox(self.showWidget)
        self.zoomCombo.addItems(['5','6','7','8','9','10','11'])

        self.radiusLabel = QLabel(self.showWidget)
        self.radiusCombo = QComboBox(self.showWidget)
        self.radiusCombo.addItems(['6','7','8','9','10','11','12'])
        # right bottom
        self.boundingBT = QPushButton('bounding', self.showWidget)
        self.pointBT = QPushButton('point', self.showWidget)
        self.fittingBT = QPushButton('fitting', self.showWidget)
        # self.zoomSLD = QSlider(Qt.Horizontal, self.showWidget)

    def path_init(self, img_path, save_path):
        self.save_path = save_path
        self.img_dir, self.img_file = os.path.split(img_path)
        self.file_list = os.listdir(self.img_dir)
        self.file_list.sort(key=lambda x: int(x[:-4]))

        for i in range(len(self.file_list)):
            if self.file_list[i] == self.img_file:
                self.current_index = i
        self.totalNum.setNum(len(self.file_list))
        self.currentNum.setNum(self.current_index+1)

    def load_img(self):
        img_path = os.path.join(self.img_dir, self.img_file)
        self.ori_img = cv2.imread(img_path)
        if self.ori_img is None:
            self.statusBar().showMessage('NOT exist')
            print('image not exist')
            sys.exit(1)

        cv2.imshow('ori', self.ori_img)
        self.bounding_img = self.ori_img
        self.dirLE.setText(img_path)

    def init_ui(self):
        # setting label text
        self.totalLabel.setText('total:')
        self.currentLabel.setText('current:')
        self.interploateLabel.setText('interploate kind:')
        self.zoomLabel.setText('zoom')
        self.radiusLabel.setText('radius')
        # setting shortcuts
        self.boundingBT.setShortcut('b')
        self.pointBT.setShortcut('p')
        self.fittingBT.setShortcut('f')
        self.saveBT.setShortcut('Ctrl+s')

        # appearance setting
        self.dirUpdate.setFont(QFont("Helvetica", 16, QFont.Black))
        self.dirLE.setFont(QFont("Helvetica", 12, QFont.Normal))
        self.totalLabel.setAlignment(Qt.AlignBottom)
        self.totalLabel.setFont(QFont("Helvetica", 14, QFont.Black))
        self.currentLabel.setAlignment(Qt.AlignBottom)
        self.currentLabel.setFont(QFont("Helvetica", 14, QFont.Black))
        pe = QPalette()
        pe.setColor(QPalette.Window, Qt.blue)
        pe.setColor(QPalette.WindowText, Qt.white)
        self.totalNum.setAutoFillBackground(True)
        self.totalNum.setFont(QFont("Helvetica", 14, QFont.Black))
        self.totalNum.setAlignment(Qt.AlignCenter)
        self.totalNum.setPalette(pe)
        self.currentNum.setAlignment(Qt.AlignCenter)
        self.currentNum.setFont(QFont("Helvetica", 14, QFont.Black))
        self.currentNum.setAutoFillBackground(True)
        self.currentNum.setPalette(pe)
        self.previousBT.setFont(QFont("Helvetica", 14, QFont.Black))
        self.nextBT.setFont(QFont("Helvetica", 18, QFont.Black))
        self.saveBT.setFont(QFont("Times", 18, QFont.Bold))
        self.quitBT.setFont(QFont("Times", 18, QFont.Bold))

        self.boundingBT.setFont(QFont("Helvetica", 16, QFont.Black))
        self.fittingBT.setFont(QFont("Helvetica", 16, QFont.Black))
        self.pointBT.setFont(QFont("Helvetica", 18, QFont.Black))

        self.interploateLabel.setFont(QFont("Helvetica", 14, QFont.Black))
        self.interploateCombo.setFont(QFont("Helvetica", 14, QFont.Black))
        self.zoomLabel.setFont(QFont("Helvetica", 14, QFont.Black))
        self.zoomCombo.setFont(QFont("Helvetica", 14, QFont.Black))
        self.radiusLabel.setFont(QFont("Helvetica", 14, QFont.Black))
        self.radiusCombo.setFont(QFont("Helvetica", 14, QFont.Black))

        # layout
        # left up
        self.leftUpLayOut = QGridLayout()
        self.leftUpLayOut.addWidget(self.dirLE, 0, 0, 1, 2)
        self.leftUpLayOut.addWidget(self.dirUpdate, 1, 0)
        self.leftUpLayOut.addWidget(self.totalLabel, 2, 0)
        self.leftUpLayOut.addWidget(self.totalNum, 3, 0)
        self.leftUpLayOut.addWidget(self.currentLabel, 2, 1)
        self.leftUpLayOut.addWidget(self.currentNum, 3, 1)

        self.leftBottomLayOut = QGridLayout()
        self.leftBottomLayOut.addWidget(self.previousBT, 0, 0)
        self.leftBottomLayOut.addWidget(self.nextBT, 0, 1)
        self.leftBottomLayOut.addWidget(self.saveBT, 1, 0)
        self.leftBottomLayOut.addWidget(self.quitBT, 1, 1)
        self.leftLayOut = QVBoxLayout()
        self.leftLayOut.addLayout(self.leftUpLayOut)
        self.leftLayOut.addLayout(self.leftBottomLayOut)

        # right
        self.rightLayOut = QGridLayout()
        self.rightLayOut.addWidget(self.interploateLabel, 0, 0)
        self.rightLayOut.addWidget(self.interploateCombo, 0, 1)
        self.rightLayOut.addWidget(self.zoomLabel, 1, 0)
        self.rightLayOut.addWidget(self.zoomCombo, 1, 1)
        self.rightLayOut.addWidget(self.radiusLabel, 2, 0)
        self.rightLayOut.addWidget(self.radiusCombo, 2, 1)

        self.rightLayOut.addWidget(self.boundingBT, 3, 0)
        self.rightLayOut.addWidget(self.pointBT, 3, 1)
        self.rightLayOut.addWidget(self.fittingBT, 4, 0, 2, 2)
        # main
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayOut)
        self.mainLayout.addLayout(self.rightLayOut)
        self.showWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.showWidget)

        self.show()

    def clear_vars(self):
        # mem var
        self.ori_img = None

        self.point1 = (0, 0)
        self.point2 = (0, 0)
        self.bounding_coor = None
        self.bounding_img = None

        self.point_list_zoom = []
        # self.point_list_ori = []
        self.fitting_point_list = []
        #self.zoom_ratio = 1
        self.bounding_winna = 'bounding'
        self.ori_winna = 'ori'
        self.point_winna = 'point'
        self.fitting_winna = 'fitting'
        # interploate kind
        self.interploate_kind = 'slinear'
        self.interploateCombo.setCurrentText('slinear')
        self.fitting_flag = 0
        self.bounding_flag = 0
        self.point_flag = 0

        # img
        self.fitting_img = None
        self.label_img = None

    def event_set(self):
        self.boundingBT.clicked.connect(self.event_boundingBT)
        self.pointBT.clicked.connect(self.event_pointBT)
        self.fittingBT.clicked.connect(self.event_fittingBT)
        self.interploateCombo.activated[str].connect(self.event_fitting_kind)
        self.saveBT.clicked.connect(self.event_saveBT)
        self.nextBT.clicked.connect(self.event_nextBT)
        self.previousBT.clicked.connect(self.event_previousBT)
        self.zoomCombo.activated[str].connect(self.event_zoom)
        self.radiusCombo.activated[str].connect(self.event_radius)

    def event_radius(self,text):
        self.radius = int(text)
        self.radiusCombo.setCurrentText(text)
        if self.fitting_flag == 1:
            self.fitting()


    def event_zoom(self,text):
        self.zoom_ratio = int(text)
        self.zoomCombo.setCurrentText(text)
        if self.bounding_flag:
            self.point()

    def event_nextBT(self):
        if self.current_index < len(self.file_list) - 1:
            self.current_index += 1
            self.img_file = self.file_list[self.current_index]
            cv2.destroyAllWindows()
            self.clear_vars()
            self.load_img()
            self.currentNum.setNum(self.current_index+1)
            self.bounding_box()
        else:
            print("the last one")

    def event_previousBT(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.img_file = self.file_list[self.current_index]
            cv2.destroyAllWindows()
            self.clear_vars()
            self.load_img()
            self.currentNum.setNum(self.current_index+1)
            self.bounding_box()
        else:
            print("the first one")

    def event_saveBT(self):
        height, width = self.ori_img.shape[:2]
        self.label_img = np.zeros((height, width))
        # zoom in fitting_img
        height_f, width_f = self.fitting_img.shape[:2]
        height_f //= self.zoom_ratio
        width_f //= self.zoom_ratio
        img = cv2.resize(self.fitting_img, (width_f, height_f))
        offset_x = self.bounding_coor[0]
        offset_y = self.bounding_coor[1]
        for i in range(width_f):
            for j in range(height_f):
                if img[j][i][2] == 255:
                    self.label_img[offset_y + j][offset_x + i] = 255
        save_file_name = os.path.join(self.save_path, self.img_file)
        cv2.imwrite(save_file_name, self.label_img)
        cv2.namedWindow('label', cv2.WINDOW_NORMAL)
        cv2.imshow('label', self.label_img)
        cv2.waitKey(300)

    def event_fitting_kind(self, text):
        self.interploate_kind = text
        self.interploateLabel.setText(text)

    def event_fittingBT(self):
        """
        if 1:
            self.bounding_flag = False
            self.point_flag = False
            self.fitting_flag = True
            self.fitting()
        else:
            self.fitting_flag = False
            # self.fitting_finish()
        """
        self.fitting()

    def fitting_slinear(self):
        self.fitting_point_list.clear()

        x = [i[0] for i in self.point_list_zoom]
        y = [i[1] for i in self.point_list_zoom]

        for i in range(len(x) - 1):
            if x[i + 1] - x[i] > 3:
                step = 1
            elif x[i + 1] - x[i] < -3:
                step = -1
            else:
                for j in range(min(y[i], y[i + 1]), max(y[i], y[i + 1])):
                    self.fitting_point_list.append((x[i], j))
                continue

            func = interpolate.interp1d([x[i], x[i + 1]], [y[i], y[i + 1]], 'slinear')
            for j in range(x[i], x[i + 1], step):
                self.fitting_point_list.append((j, func(j)))

    def fitting_quadratic(self):
        self.fitting_point_list.clear()

        if self.point_list_zoom[0][0] > self.point_list_zoom[1][0]:
            flag = -1
        elif self.point_list_zoom[0][0] < self.point_list_zoom[1][0]:
            flag = 1
        else:
            flag = 0

        point_seg = []
        point_to_interpolate = [self.point_list_zoom[0]]
        for i in range(len(self.point_list_zoom) - 1):
            x1 = self.point_list_zoom[i][0]
            x2 = self.point_list_zoom[i + 1][0]
            if (x2 - x1) * flag > 0 or (x2 == x1 and flag == 0):
                point_to_interpolate.append(self.point_list_zoom[i + 1])
            else:
                point_seg.append(point_to_interpolate.copy())
                point_to_interpolate.clear()
                point_to_interpolate.append(self.point_list_zoom[i])
                if self.point_list_zoom[i][0] > self.point_list_zoom[i + 1][0]:
                    flag = -1
                elif self.point_list_zoom[i][0] < self.point_list_zoom[i + 1][0]:
                    flag = 1
                else:
                    flag = 0

        point_seg.append(point_to_interpolate.copy())

        for point_to_interpolate in point_seg:
            x = [i[0] for i in point_to_interpolate]
            y = [i[1] for i in point_to_interpolate]
            if x[0] > x[-1]:
                func = interpolate.interp1d(x, y, 'quadratic')
                for i in range(x[0], x[-1], -1):
                    self.fitting_point_list.append((i, func(i)))
            elif x[0] < x[-1]:
                func = interpolate.interp1d(x, y, 'quadratic')
                for i in range(x[0], x[-1]):
                    self.fitting_point_list.append((i, func(i)))
            else:
                for i in range(min(y), max(y)):
                    self.fitting_point_list.append((x[0], i))

    def fitting_cubic(self):
        self.fitting_point_list.clear()

        if self.point_list_zoom[0][0] > self.point_list_zoom[1][0]:
            flag = -1
        elif self.point_list_zoom[0][0] < self.point_list_zoom[1][0]:
            flag = 1
        else:
            flag = 0

        point_seg = []
        point_to_interpolate = [self.point_list_zoom[0]]
        for i in range(len(self.point_list_zoom) - 1):
            x1 = self.point_list_zoom[i][0]
            x2 = self.point_list_zoom[i + 1][0]
            if (x2 - x1) * flag > 0 or (x2 == x1 and flag == 0):
                point_to_interpolate.append(self.point_list_zoom[i + 1])
            else:
                point_seg.append(point_to_interpolate.copy())
                point_to_interpolate.clear()
                point_to_interpolate.append(self.point_list_zoom[i])
                if self.point_list_zoom[i][0] > self.point_list_zoom[i + 1][0]:
                    flag = -1
                elif self.point_list_zoom[i][0] < self.point_list_zoom[i + 1][0]:
                    flag = 1
                else:
                    flag = 0

        point_seg.append(point_to_interpolate.copy())

        for point_to_interpolate in point_seg:
            x = [i[0] for i in point_to_interpolate]
            y = [i[1] for i in point_to_interpolate]
            if x[0] > x[-1]:
                func = interpolate.interp1d(x, y, 'cubic')
                for i in range(x[0], x[-1], -1):
                    self.fitting_point_list.append((i, func(i)))
            elif x[0] < x[-1]:
                func = interpolate.interp1d(x, y, 'cubic')
                for i in range(x[0], x[-1]):
                    self.fitting_point_list.append((i, func(i)))
            else:
                for i in range(min(y), max(y)):
                    self.fitting_point_list.append((x[0], i))

    def fitting(self):
        self.point_flag = 1
        if self.interploate_kind == 'slinear':
            self.fitting_slinear()
        elif self.interploate_kind == 'quadratic':
            self.fitting_quadratic()
        else:
            self.fitting_cubic()

        img_tmp = self.zoom_img(self.bounding_img)
        self.draw_point_zoom(img_tmp, 'fitting')
        self.fitting_img = img_tmp
        self.fitting_flag = 1
        cv2.namedWindow(self.fitting_winna, cv2.WINDOW_NORMAL)
        cv2.imshow(self.fitting_winna, img_tmp)
        cv2.waitKey(300)
        self.event_saveBT()

    def event_pointBT(self):
        """
        if pressed:
            self.bounding_flag = False
            self.point_flag = True
            self.fitting_flag = False
            self.point()
        else:
            self.point_flag = False
            #self.point_finish()
        """
        self.point()

    def event_boundingBT(self):
        '''
        if pressed == 0:
            self.bounding_flag = False
            self.bounding_finish()
        else:
            self.bounding_flag = True
            self.point_flag = False
            self.fitting_flag = False
            self.bounding_box()
        '''
        self.bounding_box()

    def point(self):
        cv2.destroyAllWindows()
        self.point_list_zoom.clear()
        img_tmp = self.zoom_img(self.bounding_img)
        cv2.imshow(self.point_winna, img_tmp)
        cv2.setMouseCallback(self.point_winna, self.point_mouse)
        self.statusBar().showMessage('point')
        cv2.waitKey(0)

    def point_mouse(self, event, x, y, flags, param):
        img_tmp = self.zoom_img(self.bounding_img)
        if event == cv2.EVENT_RBUTTONDOWN:
            self.add_point(x, y)
            self.draw_point_zoom(img_tmp, 'point')
            cv2.imshow(self.point_winna, img_tmp)
        elif event == cv2.EVENT_LBUTTONDBLCLK:
            self.fitting()

    def add_point(self, x, y):
        self.point_list_zoom.append((x, y))
        # self.point_list_ori.append(self.cal_point_coor(x, y))
        # add listwidget

    def cal_point_coor(self, x, y):
        x = x // self.zoom_ratio
        y = y // self.zoom_ratio
        x += self.bounding_coor[0]
        y += self.bounding_coor[1]
        return x, y

    def draw_point_zoom(self, img, mode):
        if mode == 'point':
            for point_coor in self.point_list_zoom:
                cv2.circle(img, point_coor, self.radius, (255, 0, 0), -1)
            # cv2.putText(img, str(len(self.point_list_zoom)), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 5)
        elif mode == 'fitting':
            for point_coor in self.fitting_point_list:
                cv2.circle(img, point_coor, self.radius, (0, 0, 255), -1)
        return img

    def zoom_img(self, img):
        height, width = img.shape[:2]
        width *= self.zoom_ratio
        height *= self.zoom_ratio
        return cv2.resize(img, (width, height))

    def bounding_box(self):
        cv2.destroyAllWindows()
        cv2.imshow(self.bounding_winna, self.ori_img)
        cv2.setMouseCallback(self.bounding_winna, self.bounding_mouse)
        self.statusBar().showMessage('bounding')
        cv2.waitKey(0)

    def bounding_finish(self):
        cv2.destroyAllWindows()
        self.zoom_ratio = 8
        img_tmp = self.zoom_img(self.bounding_img)
        cv2.imshow(self.bounding_winna, img_tmp)
        self.statusBar().showMessage('bounding OK')
        cv2.waitKey(0)

    def bounding_mouse(self, event, x, y, flags, param):
        img_tmp = self.ori_img.copy()
        if event == cv2.EVENT_LBUTTONDOWN:
            self.point1 = (x, y)
            cv2.circle(img_tmp, self.point1, 10, (0, 255, 0), 1)
            cv2.imshow(self.bounding_winna, img_tmp)
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
            cv2.rectangle(img_tmp, self.point1, (x, y), (0, 255, 0), 1)
            cv2.imshow(self.bounding_winna, img_tmp)
        elif event == cv2.EVENT_LBUTTONUP:
            self.point2 = (x, y)
            cv2.rectangle(img_tmp, self.point1, self.point2, (0, 255, 0), 1)
            cv2.imshow(self.bounding_winna, img_tmp)
            min_x = min(self.point1[0], self.point2[0])
            min_y = min(self.point1[1], self.point2[1])
            width = abs(self.point1[0] - self.point2[0])
            height = abs(self.point1[1] - self.point2[1])
            self.bounding_img = self.ori_img[min_y:min_y + height, min_x:min_x + width]
            self.bounding_coor = (min_x, min_y, width, height)
            print(self.bounding_coor)
            self.bounding_flag = 1
            self.point()


if __name__ == '__main__':
    path = '/home/wuyudong/Project/ImageData/guidewire/send_guidewire_img/1.0.png'
    app = QApplication(sys.argv)
    w = MainWindow(sys.argv[1], sys.argv[2])
    sys.exit(app.exec())
