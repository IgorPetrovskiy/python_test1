from PIL.ImageFilter import SHARPEN
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PIL import Image, ImageFilter
import os



app = QApplication([])
main_win = QWidget()
main_win.resize(1000, 500)
main_win.setWindowTitle('Easy Editor')

hline1 = QHBoxLayout()
vline2 = QVBoxLayout()
vline3 = QVBoxLayout()
hline4 = QHBoxLayout()

s_b = QPushButton('Папка')
s_l = QListWidget()
s_p = QLabel('Картинка')

s_b1 = QPushButton('Ліворуч')
s_b2 = QPushButton('Праворуч')
s_b3 = QPushButton('Дзеркало')
s_b4 = QPushButton('Різкість')
s_b5 = QPushButton('Ч/Б')

hline1.addLayout(vline2, 35)
hline1.addLayout(vline3, 65)
main_win.setLayout(hline1)

vline2.addWidget(s_b)
vline2.addWidget(s_l)

vline3.addWidget(s_p, 95)
vline3.addLayout(hline4)

hline4.addWidget(s_b1)
hline4.addWidget(s_b2)
hline4.addWidget(s_b3)
hline4.addWidget(s_b4)
hline4.addWidget(s_b5)


main_win.show()
workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
   result = []
   for filename in files:
      for ext in extensions:
          if filename.endswith(ext):
             result.append(filename)
   return result

def showFilenamesList():
   extensions = ['.png', '.jpeg', '.jpg', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)
   s_l.clear()
   for filename in filenames:
      s_l.addItem(filename)



s_b.clicked.connect(showFilenamesList)
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.dir = None
        self.save_dir = 'Modefied/'
    def loadImage(self, dir, filename):
        self.filename = filename
        self.dir = dir
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def d0_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showImage(self, path):
        s_p.hide()
        s_pix = QPixmap(path)
        s_w, s_h = s_p.width(), s_p.height()
        s_pix = s_pix.scaled(s_w, s_h, Qt.KeepAspectRatio)
        s_p.setPixmap(s_pix)
        s_p.show()
work_img = ImageProcessor()

def showChooseImage():
    if s_l.currentRow() >= 0:
        filename = s_l.currentItem().text()
        work_img.loadImage(workdir, filename)
        image_path = os.path.join(work_img.dir, work_img.filename)
        work_img.showImage(image_path)
s_l.currentRowChanged.connect(showChooseImage)
s_b1.clicked.connect(work_img.do_left)
s_b2.clicked.connect(work_img.do_right)
s_b3.clicked.connect(work_img.do_flip)
s_b4.clicked.connect(work_img.d0_sharpen)
s_b5.clicked.connect(work_img.do_bw)
app.exec_()