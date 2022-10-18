from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

import glob
import pickle
import os.path

def decryptFile(myfilespath, key, iv):
	cipher = AES.new(key, AES.MODE_CBC, iv)
	for efile in myfilespath:
		with open (efile, "r+") as f:
			ct = f.read()
			try:
				ct = b64decode(ct)
				pt = unpad(cipher.decrypt(ct), AES.block_size)
				print(pt)
				#Overwrite file
				f.seek(0)
				pt = pt.decode('utf-8')
				f.write(pt)
				f.truncate()
				#Change file extension
				pre, _ = os.path.splitext(efile)
				os.rename(efile, pre + '.txt')
			except ValueError:
				print("Incorrect decryption")
			except KeyError:
				print("Incorrect Key")

keyExists = os.path.exists("ransomkey.txt")	#Check if file exists

#Get all .enc files in the Victim file
myfilespath = glob.glob(r'./*.enc')
n = len(myfilespath)

if keyExists and n > 0:
	myfilespath.sort()
	key_in = open("ransomkey.txt", "rb")
	key, iv = pickle.load(key_in)
	key_in.close()
	iv = b64decode(iv)
	decryptFile(myfilespath, key, iv)
elif keyExists == False:
	print("ransomkey.txt is not found in this directory")
elif n <= 0:
	print("No encrypted file is found")


