#!/usr/bin/python

from key_gen import Generator
from Crypto.Cipher import AES
from passlib.hash import pbkdf2_sha256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import bcrypt
import getpass
import sys
import struct
import base64
import gzip
import zlib
import optparse
import time
import os

def decrypt_key(edit,view):
   
    passwd = getpass.getpass("Enter Password: ")
    
    #hash1 = "$2b$12$GOI.Bn1BVCRB/H8Owiqacu79wugPW8x9O49YVghdKglT9LaCtWsMe"
    hash2 = "$2a$12$hLiCfiMkJQcIt.h9zw4pXOCiWQXw4.Nv4m1alSKrhuaUVZ08AcVGS"
  
    if (hash2 == bcrypt.hashpw(str(passwd),hash2)) == False:
        print "[!] Incorrect password. Goodbye."
        sys.exit()

    plaintext = ''

    with open("private_key.pem.e",'rb') as ciphertext:

        size = struct.unpack('<Q',ciphertext.read(struct.calcsize('Q')))[0]
        iv = ciphertext.read(16)

        decryptor = AES.new(passwd,AES.MODE_CBC,iv)

        while True:
            
            chunks = ciphertext.read(24*1024)
            if len(chunks) == 0:
                break
            elif len(chunks) % 16 != 0:
                chunks += ' ' * (16 - len(chunks) % 16)

            plaintext += decryptor.decrypt(chunks)
        
        plaintext = plaintext[:int(size)]

    with open("passwords.enc","rb") as ciphertext:
        passwords_enc = ciphertext.read()

    private_key = RSA.importKey(plaintext)

    private_key = PKCS1_OAEP.new(private_key)

    chunk_size = 512
    offset = 0
    decrypted = ""

    passwords_enc = base64.b64decode(passwords_enc)

    while offset < len(passwords_enc):

        chunk = passwords_enc[offset:offset+chunk_size]
        decrypted += private_key.decrypt(chunk)
        offset += chunk_size

    passwords = zlib.decompress(decrypted)

    if view:
        print 
        print passwords
        time.sleep(20)
        os.system("reset")

    if edit:
        with open("passwords","wb") as fobj:
            fobj.write(passwords)

def encrypt_file():

    test = Generator()
    test.RSA_encrypt("passwords")
    time.sleep(2)
    print "[*] Saving new password file..."
    os.system("shred passwords")
    time.sleep(2)
    os.system("rm passwords")
    print "Done."

def main():

    parser = optparse.OptionParser("usage: %prog" + " --view [view passwords] --edit [edit passwords]")
    parser.add_option("--view",action="store_true",dest="view",default=False,help="to view passwords use --view")
    parser.add_option("--edit",action="store_true",dest="edit",default=False,help="to edit passwords use --edit")
    parser.add_option("--encrypt",action="store_true",dest="encrypt",default=False,help="encrypt file")

    (options,args) = parser.parse_args()
    view = options.view
    edit = options.edit
    encrypt = options.encrypt

    if view or edit:
        decrypt_key(edit,view)
    elif encrypt:
        encrypt_file()
    else:
        parser.error("[!] Please select an option")



main()


