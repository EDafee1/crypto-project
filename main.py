import core
import cv2
from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt #importing matplotlib
import numpy as np
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pyqtgraph as pg

class Main(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)    

        self.setWindowTitle("Fernet RSA Hybrid")
        self.setFixedSize(900, 1000)

        self.lbl_title = QLabel('Fernet and RSA Hybrid Cryptography')
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setFont(QFont('Arial', 19, weight=QFont.Bold))

        # Fernet Widget
        self.fernet = QLabel('')
        self.lbl_fernet = QLabel('Fernet Key')
        self.lbl_fernet.setFont(QFont('Arial', 8, weight=QFont.Bold))
        self.lbl_fernet.setAlignment(Qt.AlignCenter)
        self.key_fernet = QTextEdit('')
        self.key_fernet.setReadOnly(True)

        self.btn_fernet = QPushButton('Generate Fernet Key!')
        self.btn_fernet.clicked.connect(self.get_fernet)

        # RSA Widget
        self.lbl_rsa = QLabel('')
        self.lbl_rsa_pub = QLabel('RSA Public Key')
        self.lbl_rsa_pub.setFont(QFont('Arial', 8, weight=QFont.Bold))
        self.lbl_rsa_pub.setAlignment(Qt.AlignCenter)
        self.key_rsa_pub = QTextEdit('')
        self.lbl_rsa_prv = QLabel('RSA Private Key')
        self.lbl_rsa_prv.setFont(QFont('Arial', 8, weight=QFont.Bold))
        self.lbl_rsa_prv.setAlignment(Qt.AlignCenter)
        self.key_rsa_prv = QTextEdit('')
        self.key_rsa_pub.setReadOnly(True)
        self.key_rsa_prv.setReadOnly(True)
        self.btn_rsa = QPushButton('Generate RSA Key!')
        self.btn_rsa.clicked.connect(self.get_rsa)

        #Encryption Widget
        self.space = QLabel('')
        self.testing = QLabel('Plain Text Messege')
        self.testing.setFont(QFont('Arial', 8, weight=QFont.Bold))
        self.testing.setAlignment(Qt.AlignCenter)
        self.plain_text = QTextEdit()
        self.plain_text.setFixedHeight(200)
        self.plain_text.setPlaceholderText('Type your message!')

        self.btn_enc = QPushButton('Encrypt Message!')
        self.btn_enc.clicked.connect(lambda: self.enc(self.plain_text.toPlainText()))

        # Cipher Image Widget
        self.cipher_img_title = QLabel('Encrypted Image')
        self.cipher_img_title.setAlignment(Qt.AlignCenter)
        self.cipher_img_title.setFont(QFont('Arial', 8, weight=QFont.Bold))
        self.cipher_img = QLabel()
        self.cipher_img.setAlignment(Qt.AlignCenter)
        self.mse_label = QLabel('MSE')
        self.mse_label.setFixedWidth(300)
        self.ava_label = QLabel('AVA')
        self.psnr_label = QLabel('PSNR')
        self.uaci_label = QLabel('UACI')
        self.npcr_label = QLabel('NPCR')


        self.hidden_msg = QLabel('Hidden Message')
        self.hidden_msg.setFont(QFont('Arial', 8, weight=QFont.Bold))
        self.hidden_msg.setAlignment(Qt.AlignCenter)

        self.btn_dec = QPushButton('Decrypt Image!')
        self.btn_dec.clicked.connect(self.dec)

        self.plain_text2 = QTextEdit()
        self.plain_text2.setReadOnly(True)

        # Plain Image Widget
        self.btn_img = QPushButton('Browse Images!')
        self.btn_img.setFixedWidth(300)
        self.btn_img.clicked.connect(self.get_img)
        # self.btn_img.clicked.connect(self.show_new_window)
        self.plain_img_title = QLabel('Original Image')
        self.plain_img_title.setAlignment(Qt.AlignCenter)
        self.plain_img_title.setFont(QFont('Arial', 8, weight=QFont.Bold))
        self.plain_img = QLabel()
        self.plain_img.setFixedHeight(200)
        self.plain_img.setAlignment(Qt.AlignCenter)

        self.btn_hist_ori = QPushButton('Plain Histogram')
        self.btn_hist_ori.clicked.connect(self.show_histogram_ori)

        self.btn_hist_cpr = QPushButton('Cipher Histogram')
        self.btn_hist_cpr.clicked.connect(self.show_histogram_cpr)

        layout = QVBoxLayout()
        layout_fernet = QVBoxLayout()

        layout_rsa = QVBoxLayout()
        layout_rsa_pub = QVBoxLayout()
        layout_rsa_prv = QVBoxLayout()
        layout_rsa_keys = QHBoxLayout()

        layout_keys = QHBoxLayout()

        layout_plain = QHBoxLayout()
        layout_plain_msg = QVBoxLayout()
        layout_img_ori = QVBoxLayout()

        layout.setContentsMargins(QMargins(50,10,50,10))
        layout.addWidget(self.lbl_title)

        # Fernet Layout
        layout_fernet.addWidget(self.space)
        layout_fernet.addWidget(self.lbl_fernet)
        layout_fernet.addWidget(self.key_fernet)
        layout_fernet.addWidget(self.btn_fernet)

        layout_keys.addLayout(layout_fernet)

        # RSA Layout
        layout_rsa.addWidget(self.space)
        layout_rsa_pub.addWidget(self.lbl_rsa_pub)
        layout_rsa_pub.addWidget(self.key_rsa_pub)
        layout_rsa_prv.addWidget(self.lbl_rsa_prv)
        layout_rsa_prv.addWidget(self.key_rsa_prv)
        layout_rsa_keys.addLayout(layout_rsa_pub)
        layout_rsa_keys.addLayout(layout_rsa_prv)
        layout_rsa.addLayout(layout_rsa_keys)
        layout_rsa.addWidget(self.btn_rsa)
        layout_keys.addLayout(layout_rsa)

        layout.addLayout(layout_keys)


        # Original Image Layout
        layout_img_ori.addWidget(self.plain_img_title)
        layout_img_ori.addWidget(self.plain_img)
        layout_img_ori.addWidget(self.btn_img)


        # Encrypt Layout
        layout_plain_msg.addWidget(self.testing)
        layout_plain_msg.addWidget(self.plain_text)
        layout_plain_msg.addWidget(self.btn_enc)

        layout_plain.addLayout(layout_img_ori)
        layout_plain.addLayout(layout_plain_msg)
        layout.addLayout(layout_plain)


        layout_img_cpr = QVBoxLayout()
        layout_cipher_msg = QVBoxLayout()
        layout_ciphir_btm = QHBoxLayout()
        layout_cipher = QVBoxLayout()
        # Decrypt Layout


        layout_img_cpr.addWidget(self.cipher_img_title)
        layout_img_cpr.addWidget(self.cipher_img)
        layout_img_cpr.addWidget(self.mse_label)
        layout_img_cpr.addWidget(self.psnr_label)
        layout_img_cpr.addWidget(self.ava_label)
        layout_img_cpr.addWidget(self.uaci_label)
        layout_img_cpr.addWidget(self.npcr_label)

        
        layout_cipher_msg.addWidget(self.space)
        layout_cipher_msg.addWidget(self.hidden_msg)
        layout_cipher_msg.addWidget(self.plain_text2)
        layout_hist = QHBoxLayout()
        layout_hist.addWidget(self.btn_hist_ori)
        layout_hist.addWidget(self.btn_hist_cpr)
        layout_cipher_msg.addLayout(layout_hist)

        layout_ciphir_btm.addLayout(layout_img_cpr)
        layout_ciphir_btm.addLayout(layout_cipher_msg)
        
        layout_img_cpr.addWidget(self.btn_dec)
        layout_cipher.addLayout(layout_ciphir_btm)
        layout.addLayout(layout_cipher)
        # self.chart = Canvas(self, 'wand_ori.png')

        self.setLayout(layout)

    def get_fernet(self):
        self.f = core.generate_fernet()
        self.key_fernet.setText(str(self.f))

    def get_rsa(self):
        self.publicKey, self.privateKey = core.generate_rsa()
        self.key_rsa_pub.setText(str(self.publicKey))
        self.key_rsa_prv.setText(str(self.privateKey))

    def enc(self, text):
        im = Image.open(self.img_path)
        self.payload = ''
        self.payload, self.cipherData = core.encData(im, text, self.f, self.publicKey)

        pixmap = QPixmap('temp_img.png')
        pixmap = pixmap.scaledToHeight(100)

        ms, ps = self.get_mse()
        av = self.get_ava()
        uaci = self.get_uaci()
        npcr = self.get_npcr()

        # err = str(ms, av)
        self.mse_label.setText(str(ms))
        self.psnr_label.setText(str(ps))
        self.ava_label.setText(str(av))
        self.uaci_label.setText(str(uaci))
        self.npcr_label.setText(str(npcr))
        self.cipher_img.setPixmap(QPixmap(pixmap))

    def dec(self):
        im = Image.open('temp_img.png')
        self.message = core.decData(im, self.payload, self.privateKey)
        self.plain_text2.setText(self.message)

    def get_img(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'D:\\UDINUS\Cryptography\crypto-project', 'Image files (*.png)')
        self.img_path = fname[0]

        pixmap = QPixmap(self.img_path)
        pixmap = pixmap.scaledToHeight(100)
        self.plain_img.setPixmap(QPixmap(pixmap))

    def get_mse(self):
        pln = cv2.imread(self.img_path)
        cpr = cv2.imread('temp_img.png')

        errormse = core.imgError(pln, cpr)
        errormse = 'MSE : ',  errormse

        errorpsnr = cv2.PSNR(pln, cpr)
        errorpsnr = 'PSNR : ', errorpsnr

        return str(errormse), str(errorpsnr)
    
    def get_ava(self):
        errorava = core.txtError(self.plain_text.toPlainText(), self.f, self.publicKey)
        errorava = 'AVA : ', errorava
        return str(errorava)
    
    def get_uaci(self):
        plain = cv2.imread(self.img_path, 0)
        cipher = cv2.imread('temp_img.png', 0)

        erroruaci = core.uaci1(plain, cipher)
        erroruaci = 'UACI : ', erroruaci

        return str(erroruaci)
    
    def get_npcr(self):
        plain = cv2.imread(self.img_path, 0)
        cipher = cv2.imread('temp_img.png', 0)

        errornpcr = core.npcr1(plain, cipher)
        errornpcr = 'NPCR : ', errornpcr

        return str(errornpcr)
    
    def show_histogram_ori(self):
        self.w = HistogramOri(self.img_path)
        self.w.show()

    def show_histogram_cpr(self):
        self.z = HistogramCpr()
        self.z.show()
    
class HistogramOri(QWidget):
    def __init__(self, img_path):
        super().__init__()
        self.setWindowTitle("Original Image Histogram")
        self.resize(500, 400)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.chart = Canvas(self, img_path)

class HistogramCpr(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Encrypted Image Histogram")
        self.resize(500, 400)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.chart = Canvas(self, 'temp_img.png')
    
class Canvas(FigureCanvas):
    def __init__(self, parent, img_path):
        fig, self.ax = plt.subplots(figsize=(5,4), dpi=100)
        super().__init__(fig)
        self.setParent(parent)

        img = cv2.imread(img_path, 0)
        histr = cv2.calcHist([img],[0],None,[256],[0,256])
        plt.plot(histr)

    


if __name__ == '__main__':
    app = QApplication([])
    window = Main()

    window.show()
    app.exec_()