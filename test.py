# import time, socket
# import binascii
# import random

# import mysql.connector
# from xpxchain import models
# from xpxchain import client
# from xpxchain import errors

# import requests
# import asyncio
# import sys

from datetime import datetime
from datetime import date


# mydb = mysql.connector.connect(
  # host="localhost",
  # user="root",
  # password="sharmelen",
  # database = "key_table"
# )

# mycursor = mydb.cursor()

# sql_all_name = "SELECT public_key FROM pub_key"
# mycursor.execute(sql_all_name)

# result_1 = mycursor.fetchall()
# #print(str(result[2]).strip("(),'"))

# ENDPOINT = "https://bctestnet1.brimstone.xpxsirius.io"

# for x in range (len(result_1)):

	# public_keys = str(result_1[x]).strip("(),'")
	# #print(public_keys)

	# account = models.PublicAccount.create_from_public_key(public_keys, models.NetworkType.TEST_NET)
	
	# with client.AccountHTTP(ENDPOINT) as http:
		
		# txns = http.transactions(account)
		
		# for x in range (len(txns)):
								
			# first_strip = str(txns[x]).strip("',")
			# transaction_array = first_strip.split("=")
			# transaction_hash = transaction_array[17].strip("', merkle_component_hash")
			# sender_signature = transaction_array[7].strip("', signer")
			# sender_address = transaction_array[10].strip("', network_type")
			
			# if str(transaction_array[1]) == "<TransactionType.TRANSFER: 16724>, network_type":
			
				# try:
					# payload = transaction_array[28].strip("')b'")
				# except:
					# print("This is a contract transaction")
								
				# try:
					# sql = "SELECT username FROM pub_key WHERE address = '"+sender_address+"'"
					# mycursor.execute(sql)
					# result = mycursor.fetchall()
					# username = str(result[0]).strip("()',")
					
				# except:
					# username = "Unknown"
					
					
				# datetime_raw = transaction_array[5].strip("datetime. max_fee ( )),")
				# datetime_array = datetime_raw.split(",")
				# date = datetime_array[2]+"/"+datetime_array[1].strip(" ")+"/"+datetime_array[0].strip(" ")
				# time = datetime_array[3]+":"+datetime_array[4].strip(" ")
				# receipient_address = transaction_array[20].strip("', network_type")
				# block_number = transaction_array[14].strip(", index")
				
				# try:
					# sql = "SELECT username FROM pub_key WHERE address = '"+receipient_address+"'"
					# mycursor.execute(sql)
					# result = mycursor.fetchall()
					# receipient_username = str(result[0]).strip("()',")
					
				# except:
					# receipient_username = 'Unknown'
					
				# tx_date = "Transaction Date: "+date
				
				
				# split_time = str(time).split(":")
				
				# if len(str(split_time[1])) < 2:
					# time = str(time)+"0" 
					
					# final_time = "\nTransaction Time: "+time +"\n"

				# else:
					
					# final_time = "\nTransaction Time: "+time +"\n"
					
				
				# #print(final_time)
				
				
				# sql_check = "SELECT sender_address FROM transaction_info WHERE tx_hash = '"+transaction_hash+"'"
				# mycursor.execute(sql_check)
				# result = mycursor.fetchall()
				
				# if len(result) > 0 :
					# print(result[0])
					# print("NOT RECORDED")
				
				# else:
					# sql_insert = "INSERT INTO transaction_info (tx_hash, sender_signature, sender_address, sender_username, receiver_address, receiver_username, payload, date, time, block_num) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
					
					# val = [(transaction_hash, sender_signature, sender_address, username, receipient_address,receipient_username, payload, date, time, block_number)] 
					# mycursor.executemany(sql_insert, val)
					# mydb.commit()
				
				
				
				# recv_username = "\nReceipient Username: "+receipient_username+"\n"	
				# block_num = "Block Number: "+block_number+"\n"
				# content = "Message Content: "+payload+"\n"
				# tx_hash = "Transaction Hash: "+transaction_hash+"\n"
				# sender_sign = "Sender Signature: "+sender_signature+"\n"
				# sender_addr = "Sender Address: "+sender_address+"\n"
				# username = "Sender's Username: "+username+"\n"
				# recv_addr = "Receipient Address: "+receipient_address+"\n"
				# recv_username = "Receipient Username: "+receipient_username+"\n"
			


# keywords = ['tx_hash','sender_signature','sender_address','sender_username','receiver_address','receiver_username','payload','date','time','block_num']

# tx_array = []
			
# for x in range (len(keywords)):		
			
	# sql_txinfo = "SELECT "+keywords[x]+" FROM transaction_info ORDER BY block_num DESC"
	# mycursor.execute(sql_txinfo)
	# result = mycursor.fetchall()
	
	# for x in range (len(result)):
		# single_tx = str(result[x]).strip("(),'")
		# tx_array.append(single_tx)
	

# for x in range (len(result)):

	# len_info = len(result) 
	
	# print("Transaction Hash: "+tx_array[x])
	# print("Sender Signature: "+tx_array[x+len_info])
	# print("Sender Address: "+tx_array[x+len_info * 2])
	# print("Sender Username: "+tx_array[x+len_info * 3])
	# print("Receiver Address: "+tx_array[x+len_info * 4])
	# print("Receiver Username: "+ tx_array[x+len_info * 5])
	# print("Content: "+ tx_array[x+len_info * 6])
	# print("Date: "+ tx_array[x+len_info * 7])
	# print("Time: "+tx_array[x+len_info * 8])
	# print("Block Number: "+tx_array[x+len_info * 9])
	# print('*****************************************************')
# #print(len(result))


# use Python 3 print function
# this allows this code to run on python 2.x and 3.x

# from __future__ import print_function
# # Variables Used
# sharedPrime = 23    # p
# sharedBase = 5      # g
 
# aliceSecret = 6     # a
# bobSecret = 15      # b
 
# # Begin
# print( "Publicly Shared Variables:")
# print( "    Publicly Shared Prime: " , sharedPrime )
# print( "    Publicly Shared Base:  " , sharedBase )
 
# # Alice Sends Bob A = g^a mod p
# A = (sharedBase**aliceSecret) % sharedPrime
# print( "\n  Alice Sends Over Public Chanel: " , A )
 
# # Bob Sends Alice B = g^b mod p
# B = (sharedBase ** bobSecret) % sharedPrime
# print( " Bob Sends Over Public Chanel: ", B )
 
# print( "\n------------\n" )
# print( "Privately Calculated Shared Secret:" )
# # Alice Computes Shared Secret: s = B^a mod p
# aliceSharedSecret = (B ** aliceSecret) % sharedPrime
# print( "    Alice Shared Secret: ", aliceSharedSecret )
 
# # Bob Computes Shared Secret: s = A^b mod p
# bobSharedSecret = (A**bobSecret) % sharedPrime
# print( "    Bob Shared Secret: ", bobSharedSecret )


import hashlib, hmac, binascii


# f = open("server_side_tx_receipt.txt", "r")
# text = f.read()


# key = "sharmelen"
# print(hmac.new(key.encode(), text.encode(), hashlib.sha256).hexdigest())
	 # #45d17a73c5e66f58e2c0799d91993c0f1c30490d2585ad5cc5b8ce2a5167b8a3


def file():	
	f = open("transaction_ledger.txt")

	output = []

	for line in f:
		output.append(line)
		
	f.close	
	fa = open("test.txt",'w')
	fa.writelines(output)
	fa.close
	

# f = open("transaction_ledger.txt","r")
# read_text = f.read()

# split_text = read_text.split("---")

# g = open("newtest.txt","w")
# g.write(split_text[0])
# g.write("---\n")
# g.close()

# v = open("newtest.txt","r")
# read_file = v.read()
# key = "sharmelen"
# mac_code = hmac.new(key.encode(), read_file.encode(), hashlib.sha256).hexdigest()

# if str(mac_code) in split_text[1]:
	# print("The mac code is equal")
	
	
# private_key = '7d9453a100ae1e64fa61d57e7fe5154ed8118b428b2ba7adfe4bd42bf4392f73'
# hash_object = hashlib.sha256(private_key.encode())
# hash_pk = hash_object.hexdigest()
# print(hash_pk)


# f = open("account_cred.txt","r")
# read = f.read()
# split = read.split("\n")
# #print(split)
# print(split[2].replace("Your Username: ",""))



	
# from xpxchain import models
# from xpxchain import client

# ENDPOINT = 'https://bctestnet1.brimstone.xpxsirius.io'

# public_key = '247da52733ee271675af71f617c282b3b5fabd4e77f71ed931651b4f7d88d8f9'
# nonce = 7546

# account = models.PublicAccount.create_from_public_key(public_key, models.NetworkType.MIJIN_TEST)
# mosaic_id = models.MosaicId.create_from_nonce(models.MosaicNonce.create_from_int(nonce), account)

# with client.MosaicHTTP(ENDPOINT) as http:
    # mosaic_info = http.get_mosaic(mosaic_id)
    # print(mosaic_info)

today = date.today()
current_date = today.strftime("%d/%m/%Y")
print(current_date)
