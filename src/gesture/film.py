# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Fri Nov 22 17:28:07 2019

URL: https://github.com/wakame-tech/vendredi-noir/tree/master/src/gesture
@author: n_toba
@id: 4617054
"""
import sys, os
from PyQt5.QtWidgets import(
    QGraphicsView, QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem
)
from PyQt5.QtCore import(
    QTimer
)
from PyQt5.QtGui import(
    QPen, QColor, QBrush, QImage, QPixmap
)
import cv2



class ObjDetector():


    def __init__(self, fname: str=None):

        # initializing cascade classifier
        self.cascade = cv2.CascadeClassifier()  # generating instance of cascade classifier
        
        # loading model file
        if fname is None:
            raise IOError(f'filename must not be None')

        self.cascade.load(fname)
        if self.cascade.empty():
            raise IOError(f'error in loading cascade file "{fname}"')


    def detect(self, im):

        # objects detector processor
        if self.cascade.empty():
            return []

        scaleFactor  = 1.1
        minNeighbors = 3
        objects = self.cascade.detectMultiScale(im, scaleFactor=scaleFactor, minNeighbors=minNeighbors)

        return objects



class VideoCaptureView(QGraphicsView):

    # updating image per ms
    repeat_interval = 20    # 20 ms = (50 Hz)**-1

    def __init__(self, parent = None):

        super(VideoCaptureView, self).__init__(parent)

        self.pixmap     = None
        self.item       = None
        self.rect_items = []

        # initializing video capture from front camera
        self.capture = cv2.VideoCapture(0)

        if not self.capture.isOpened():
            raise IOError('failed in opening VideoCapture')

        # initializing canvas
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pen = QPen(QColor(0xff, 0x00, 0x00))     # generating pen (RGB)
        self.pen.setWidth(3)                          # pen's width
        self.brush = QBrush()

        self.setVideoImage()

        # タイマー更新 (一定間隔でsetVideoImageメソッドを呼び出す)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setVideoImage)
        self.timer.start(self.repeat_interval)


    def setVideoImage(self) -> None:
        """ ビデオの画像を取得して表示 """
        ret, cv_img = self.capture.read()                # ビデオキャプチャデバイスから画像を取得
        if ret is False:
            return

        cv_img = cv2.cvtColor(cv_img,cv2.COLOR_BGR2RGB)  # 色変換 BGR->RGB
        cv_img = cv2.flip(cv_img, 1)
        height, width, dim = cv_img.shape
        bytesPerLine = dim * width                       # 1行辺りのバイト数

        # detecting objects
        self.image = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # first 
        if self.pixmap is None:                          # 初回はQPixmap, QGraphicsPixmapItemインスタンスを作成
            self.pixmap = QPixmap.fromImage(self.image)
            self.item = QGraphicsPixmapItem(self.pixmap)
            self.scene.addItem(self.item)                # キャンバスに配置
        else:
            self.pixmap.convertFromImage(self.image)     # ２回目以降はQImage, QPixmapを設定するだけ
            self.item.setPixmap(self.pixmap)

        # 物体検出を実行
        rects = detector.detect(cv_img)
        # 直前に描画した矩形を削除
        for item in self.rect_items:
            self.scene.removeItem(item)
        # 新しい矩形を描画
        self.rect_items = []

        print(rects)
        for xywh in rects:
            self.rect_items.append(self.scene.addRect(*xywh, self.pen, self.brush))



if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)

    model_fname = 'models/haarcascades/haarcascade_frontalface_default.xml'
    xml = [
        'aGest.xml',
        'closed_frontal_palm.xml',
        'fist.xml',
        'haarcascade_eye_tree_eyeglasses.xml',
        'haarcascade_frontalface_alt2.xml',
        'palm.xml'
    ][0]
    model_fname = f'haargesture/{xml}'
    detector = ObjDetector(model_fname) 

    main = QMainWindow()              # メインウィンドウmainを作成
    main.setWindowTitle("Face Detector")
    viewer = VideoCaptureView()       # VideoCaptureView ウィジエットviewを作成
    main.setCentralWidget(viewer)     # mainにviewを埋め込む
    main.show()

    app.exec_()

    viewer.capture.release()

