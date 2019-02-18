#!/usr/bin/python

"""
This Class generates a random password and RSA keys when needed. It also encrypts and ecrypts
data using PKA

Reference: https://medium.com/@ismailakkila/black-hat-python-encrypt-and
-decrypt-with-rsa-cryptography-bd6df84d65bc

"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import zlib
import gzip
import base64
import random
import time
import os

class Generator(object):

    def password(self):

        characters = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
        length = 12
        passwd = "".join(random.sample(characters,length))
        #print passwd
        return passwd

    def RSA_keys(self):
        
        print "[*] Generating Keys. Please be patient"
        print

        keys = RSA.generate(4096)
        
        public_key = keys.publickey().exportKey("PEM")
        private_key = keys.exportKey("PEM")

        print "[*] Sucessfully generated Private Key"
        time.sleep(2)
        print private_key
        print

        print "[*] Sucessfully generated Public Key"
        time.sleep(2)
        print public_key
        print

        with open("private_key.pem","wb") as private:
            private.write(private_key)

        with open("public_key.pem","wb") as public:
            public.write(public_key)

    def RSA_encrypt(self,filename):
        
        with open("public_key.pem","rb") as public:
            public_key = public.read()

        with open(filename,'rb') as fobj:
            filedata = fobj.read()
        
        key = RSA.importKey(public_key)
        
        key = PKCS1_OAEP.new(key)
        
        print "[*] Compressing: %d bytes" % len(filedata)
        
        data = zlib.compress(filedata)

        chunk_size = 470
        offset = 0
        encrypted = ""

        while offset < len(data):

            chunk = data[offset:offset+chunk_size]

            if len(chunk) % chunk_size != 0:

                chunk += " " * (chunk_size - len(chunk))

            encrypted += key.encrypt(chunk)
            offset += chunk_size

        encrypted = base64.b64encode(encrypted)

        new_file = filename + ".enc"

        with open(new_file,'wb') as fobj:
            fobj.write(encrypted)

        print "[*] File has been successfully encrypted and Base64 encoded."
        print "[*] location: %s" % os.path.abspath(new_file)

    def RSA_decrypt(self,filename):
        
        with open("keys/private_key.pem","rb") as private:
            private_key = private.read()

        with open(filename,"rb") as fobj:
            encrypted = fobj.read()
        
        key1 = RSA.importKey(private_key)
        
        key1 = PKCS1_OAEP.new(key1)
        
        chunk_size = 512
        offset = 0
        decrypted = ""

        encrypted = base64.b64decode(encrypted)

        while offset < len(encrypted):

            chunk = encrypted[offset:offset+chunk_size]

            decrypted += key1.decrypt(chunk)
            offset += chunk_size

        plaintext = zlib.decompress(decrypted)

        new_file = os.path.splitext(filename)[0]

        with open(new_file,'wb') as fobj:
            fobj.write(plaintext)
        
        print "[*] File has been successfully decrypted and Base64 decoded."
        print "[*] location: %s" % os.path.abspath(new_file)



#keys = Generator()
#keys.RSA_encrypt('test')
#keys.RSA_decrypt("test.rsa")







