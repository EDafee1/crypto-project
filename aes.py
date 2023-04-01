from Crypto.Cipher import Blowfish as alg
import base64
import stepic
from PIL import Image

""" 
Naufal  = AES
Saniya  = ARC2
Anis    = Blowfish 
        = CAST
        = DES (secret_key = 8 bit)
        = DES3
        = Salsa20 (no mode)
"""

secret_key = b'0123456789101112'
msg_text = b'aku tamfan'

def create_cipher(secret_key):
    cipher = alg.new(secret_key, alg.MODE_EAX)
    nonce = cipher.nonce
    return cipher, nonce

def encrypt(cipher, msg_text):
    encoded = base64.b64encode(cipher.encrypt(msg_text))
    return encoded

def decrypt(encoded, secret_key, nonce):
    acipher = alg.new(secret_key, alg.MODE_EAX, nonce=nonce)
    decoded = acipher.decrypt(base64.b64decode(encoded))
    return (decoded)

def encrypt_img(img, data):
    cipImg = stepic.encode(img, data)
    cipImg.save('temp_img.png')

def decrypt_img(img):
    message = stepic.decode(img)
    message = bytes(message, encoding=('utf-8'))
    return message

# Text Encryption
c, n = create_cipher(secret_key)

e = encrypt(c, msg_text)

print('Cipher Text dari Alg = ', e)

# Image Encryption
original_img = Image.open('wand_ori.png')
encrypt_img(original_img, e)

# Image Decryption
encoded_img = Image.open('temp_img.png')
d_img = decrypt_img(encoded_img)

print('Plain Text dari Image = ', d_img)

# Text Decryption
d = decrypt(d_img, secret_key, n)

print('Plain text dari Alg = ', d)

# https://stackoverflow.com/questions/15956952/how-do-i-decrypt-using-hashlib-in-python
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html