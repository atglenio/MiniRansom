from Crypto.PublicKey import RSA

#Generating private key
key = RSA.generate(2048)
private_key = key.export_key()
file_out = open("ransomprvkey.pem", "wb")
file_out.write(private_key)
file_out.close()

#Generating public key
public_key = key.publickey().export_key()
file_out = open("receiver.pem", "wb")
file_out.write(public_key)
file_out.close()
print("Keys created")
