import random
import base64
import rsa
from cryptography.fernet import Fernet

def string_to_bytes(s):
    txt = s.encode('utf-8')
    return txt

def bytes_to_string(b):
    g = base64.b64decode(b)
    return g.decode('utf-8')

def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

def list_to_string(s):
    str = ''
    
    for x in s:
        str += x

    return str

def bytes_to_bits(b):
    arr = []
    for x in b:
        arr.append(f'{x:0>8b}')
    bit = list_to_string(arr)
    return bit

def string_to_bits(s):
    byt = string_to_bytes(s)
    bit = bytes_to_bits(byt)
    return bit

def change_bit(bit):
    j = len(bit)
    k = random.randrange(j)
    bit = list(bit)
    if bit[k] == '0':
        bit[k] = '1'
    else:
        bit[k] = '0'
    bit = ''.join(bit)
    return bit

def differentBits(b1, b2):
    r = len(b1)
    diff = 0
    for i in range(r):
        if (b1[i] != b2[i]):
            diff += 1
    result = diff/r*100
    return result

def encAva(data, uniKey, pubKey):
    f = Fernet(uniKey)

    enc_data = f.encrypt(data)

    enc_uniKey = rsa.encrypt(uniKey, pubKey)

    return enc_uniKey, enc_data

def getAva(plain, fernet, pubKey):

    p = string_to_bits(plain)
    p2 = change_bit(p)

    p = bitstring_to_bytes(p)
    p2 = bitstring_to_bytes(p2)

    tKey, tData = encAva(p, fernet, pubKey)
    t2Key, t2Data = encAva(p2, fernet, pubKey)

    tData = bytes_to_bits(tData)
    tKey = bytes_to_bits(tKey)
    t2Data = bytes_to_bits(t2Data)
    t2Key = bytes_to_bits(t2Key)
    
    t = tKey + tData
    t2 = t2Key + t2Data

    diff = differentBits(t, t2)
    return diff