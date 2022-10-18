from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

import pickle

filesComplete = True
try:
	open("ransomkey.bin")
	open("ransomprvkey.pem")
except IOError:
	print("ransomkey.bin or ransomprvkey.pem not found")
	filesComplete = False

if filesComplete:
	#Get variables in file
	file_in = open("ransomkey.bin", "rb")
	enc_key, iv_byte = pickle.load(file_in)

	#Get private key
	private_key = RSA.import_key(open("ransomprvkey.pem").read())
	cipher_rsa = PKCS1_OAEP.new(private_key)

	#Decrypt encryted data
	symKey = cipher_rsa.decrypt(enc_key)
	file_in.close()

	#Store symkey and iv_byte in a file
	file_out = open("ransomkey.txt", "wb")
	pickle.dump([symKey, iv_byte], file_out)
	file_out.close()
	print('Decryption succeeded')

