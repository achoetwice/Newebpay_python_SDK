# from django.apps import apps
from Crypto.Cipher import AES
import urllib.parse
import binascii
import hashlib
# import json, string, uuid, os, time, requests


'''Encrypt/Decrypt'''

def AES_encrypt(data, key, iv):
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    return cryptor.encrypt(data)

def AES_decrypt(data, key, iv):
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    return cryptor.decrypt(data)

def NEWEBPAY_AES(order_params, key, iv):
    order_params = urllib.parse.urlencode(order_params)
    BS = 32
    pad_params = order_params + (BS - len(order_params) % BS) * chr(BS - len(order_params) % BS)
    AES_info = AES_encrypt(pad_params, key, iv)
    AES_info_str = str(binascii.hexlify(AES_info), 'ascii')
    return AES_info_str

def NEWEBPAY_SHA(AES_plus):
    m = hashlib.sha256()
    m.update(AES_plus.encode('ascii'))
    SHA_info = m.digest()
    SHA_info_str = str(binascii.hexlify(SHA_info), 'ascii')
    SHA_info_STR = SHA_info_str.upper()
    return SHA_info_STR
    
def NEWEBPAY_AES_decrypt(AES_info_str, key, iv):
    AES_info = AES_info_str.encode('utf-8')
    AES_info = binascii.unhexlify(AES_info)
    AES_info = AES_decrypt(AES_info, key, iv)
    AES_info = AES_info.decode("utf-8")
    padding_str = AES_info[-1]
    AES_info = AES_info.strip(padding_str)
    AES_info = json.loads(AES_info)
    return (AES_info)