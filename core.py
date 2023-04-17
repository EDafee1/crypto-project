import rsa
import stepic
import math
import numpy as np
import ava as av
from sewar.full_ref import mse
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode
from PIL import Image

def percent_f(f):
    f = float(f)/100
    return '{:.2%}'.format(f)

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

def txtError(plain, fernet, pubKey):
    err = av.getAva(plain, fernet, pubKey)
    return err

def imgPsnr(plain, cipher):
    errmse = mse(plain, cipher)
    if errmse == 0:
        return 100
    max_pixel = 255
    psnr = 20 * math.log10(max_pixel) - 10 * math.log10(errmse)
    return psnr

def imgUaci(img1, img2):
    diff = np.abs(img1 - img2)
    diff = np.sum(diff)

    total = (255 * img1.shape[0] * img2.shape[1])

    print(diff)
    print(total)

    uaci =  diff / total
    
    return uaci * 100

def sumofpixel(height,width,img1,img2):
    matrix = np.empty([width, height])
    for y in range(0, height):
        for x in range(0, width):
            if img1[x,y] == img2[x,y]:
                matrix[x,y] = 0
            else:
                matrix[x,y] = 1
    
    psum=0
    for y in range(0,height):
        for x in range(0,width):
            psum = matrix[x,y]+psum
    return psum

def npcr(img1, img2):

    original_arr = np.array(img1)
    stego_arr = np.array(img2)

    num_changed_pixels = 0
    for x in range(original_arr.shape[0]):
        for y in range(original_arr.shape[1]):
            if (original_arr[x][y] == stego_arr[x][y]).all():
                num_changed_pixels += 1

    total_pixels = original_arr.shape[0] * original_arr.shape[1]

    npcr = (num_changed_pixels / total_pixels) * 100

    return npcr

def imgNpcr(plain, cipher):
    c1 = plain
    c2 = cipher
    width, height = c1.shape
    ematrix = np.empty([width, height])
    per = ((sumofpixel(height,width,c1, c2)/(height*width))*100)
    return per

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