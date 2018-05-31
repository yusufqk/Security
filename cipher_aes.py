#!/usr/bin/python

"""

Author: Yusuf Kassim

This script uses AES to encrypt and decrypt a file
The flag is used so that this script can be used via command line or imported within another
script.

In fact the flag option is not necessary. If the user wants to use this class as an imported object in another
script, then simply uncomment the last two lines of the script.

"""

from Crypto.Cipher import AES
import os
import random
import struct
import optparse

with open('password','rb') as fobj:
    key = fobj.read().strip()

chunk_size = 64*1024
chunk_size1 = 24*1024

class Cipher(object):

    def __init__(self,filepath=None,action=None,flag=False):
        
        self.filepath = filepath
        self.flag = flag
        self.action = action
        


    def main(self):

        parser = optparse.OptionParser("usage: %prog" + " -f [filename] --encrypt [encryption] --decrypt [decryption]")
        parser.add_option("-f","--filename",dest="filename",type="string",help="specify filename")
        parser.add_option("--encrypt",action="store_true",dest="encrypt",default=False,help="to encrypt use --encrypt")
        parser.add_option("--decrypt",action="store_true",dest="decrypt",default=False,help="to decrypt use --decrypt")
        (options,args) = parser.parse_args()
        filename = options.filename
        encrypt = options.encrypt
        decrypt = options.decrypt
       
        if filename == None:
            parser.error("[!] Please give a file name")
        elif os.path.exists(filename) == False:
            parser.error("[!] Please give a file that exists")
        elif encrypt:
            self.encrypt(key,filename,chunk_size)
        elif decrypt:
            self.decrypt(key,filename,chunk_size1)
        else:
            parser.error("[!] Something went wrong. Try again.")


    def encrypt(self,key,filename,chunk_size):

        file_encrypt = filename + ".e"
        iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))

        encryptor = AES.new(key,AES.MODE_CBC,iv)

        filesize = os.path.getsize(filename)
    
        with open(filename,'rb') as plaintext:
            with open(file_encrypt,'wb') as ciphertext:
                ciphertext.write(struct.pack('<Q',filesize))
                ciphertext.write(iv)

                while True:
                    chunk = plaintext.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)

                    ciphertext.write(encryptor.encrypt(chunk))

                    
        print "[*] %s has been successfully encrypted" % filename
        print "[*] located at: %s" % os.path.abspath(file_encrypt)

                 

    def decrypt(self,key,filename,chunk_size1):

        file_decrypt = os.path.splitext(filename)[0]

        with open(filename,'rb') as ciphertext:
            size = struct.unpack('<Q',ciphertext.read(struct.calcsize('Q')))[0]
            iv = ciphertext.read(16)
            
            decryptor = AES.new(key,AES.MODE_CBC,iv)

            with open(file_decrypt,'wb') as plaintext:

                while True:
                    chunks = ciphertext.read(chunk_size1)
                    if len(chunks) == 0:
                        break
                    elif len(chunks) % 16 != 0:
                        chunks += ' ' * (16 - len(chunks) % 16)

                    plaintext.write(decryptor.decrypt(chunks))
                
                plaintext.truncate(size)

        
        print "[*] %s has been successfully decrypted" % file_decrypt
        print "[*] located at: %s" % os.path.abspath(file_decrypt)


hidden = Cipher()
hidden.main()
