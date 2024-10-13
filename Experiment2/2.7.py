from base64 import b64decode
from Cryptodome import Random
from Cryptodome.Cipher import AES
from random import randint

def detect_pck7(padding_msg,block_size):
    if len(padding_msg)%block_size==0 :
        return False
    if padding_msg[-padding_msg[-1]:0]!=bytes([padding_msg[-1]])*padding_msg[-1] :
        return False
    
    return True

def clear_pad(padding_msg) :
    return padding_msg[:padding_msg[-1]]

def test(msg,block_size):
    try:
        if not detect_pck7(msg,block_size):
            raise ValueError
        
    except ValueError:
        print(f"{msg} has invaild PKCS#7 padding.")
        return

    print(f"Padding successfully...")
    print(f"Before padding removal: { msg }")
    print(f"After padding removal: { clear_pad(msg) }")
