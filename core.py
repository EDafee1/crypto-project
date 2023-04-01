import rsa
import stepic
import math
import numpy as np
import avalanche as av
from sewar.full_ref import mse
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode

def generate_rsa():
    publicKey, privateKey = rsa.newkeys(2048)
    return publicKey, privateKey

def generate_fernet():
    uniKey = Fernet.generate_key()
    return uniKey

def encImg(img, data):
    cipImg = stepic.encode(img, data)
    cipImg.save('temp_img.png')

def decImg(img):
    message = stepic.decode(img)
    return message

def encData(img, data, uniKey, pubKey):
    f = Fernet(uniKey)

    enc_data = f.encrypt(data.encode('utf-8'))
    enc_data = b64encode(enc_data).decode('utf-8')

    enc_uniKey = rsa.encrypt(uniKey, pubKey)
    enc_uniKey = b64encode(enc_uniKey).decode('utf-8')

    encImg(img, bytes(enc_data, encoding='utf-8'))

    return enc_uniKey, enc_data

def decData(img, enc_uniKey, prvKey):
    enc_data = decImg(img)

    enc_data = b64decode(enc_data)
    enc_uniKey = b64decode(enc_uniKey)

    uniKey = rsa.decrypt(enc_uniKey, prvKey)

    f = Fernet(uniKey)

    data = f.decrypt(enc_data).decode('utf-8')

    return data

def imgError(plain, cipher):
    err = mse(plain, cipher)
    return err

def txtError(cipher):
    err = av.getAva(cipher)
    return err

def imgPsnr(plain, cipher):
    errmse = mse(plain, cipher)
    if errmse == 0:
        return 100
    max_pixel = 255
    psnr = 20 * math.log10(max_pixel) - 10 * math.log10(errmse)
    return psnr

# import cv2
# im1 = cv2.imread('wand_ori.png')
# im2 = cv2.imread('temp_img.png')

# ps = cv2.PSNR(im1, im2)
# ps2 = imgPsnr(im1, im2)
# ps3 = gpsnr(luma(im1), luma(im2))
# print(ps)
# print(ps2)
# print(ps3)
# f = generate_fernet()
# publicKey, privateKey = generate_rsa()
# d = 'iyaaaaa udahhh'
# en_d = encData(d, f, publicKey)
# de_d = decData(en_d, privateKey)

# print(d)
# print(en_d)
# print(de_d)