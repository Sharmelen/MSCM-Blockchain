import time, socket
import binascii
import random
import hashlib, hmac

import mysql.connector
from xpxchain import models
from xpxchain import client
from xpxchain import errors

import requests
import asyncio
import sys

from datetime import datetime
from datetime import date as datetoday


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="sharmelen",
  database = "key_table"
)

mycursor = mydb.cursor()
  
def server():

	# take the server name and port name
	host = '127.0.0.1'
	port = 5000
	   
	# create a socket at server side
	# using TCP / IP protocol
	s = socket.socket(socket.AF_INET, 
					  socket.SOCK_STREAM)
	   
	# bind the socket with server
	# and port number
	s.bind(('', port))
	   
	# allow maximum 1 connection to
	# the socket
	s.listen(1)
	   
	# wait till a client accept
	# connection
	c, addr = s.accept()
	   
	# display client address
	print("CONNECTION FROM:", str(addr))

	received_message = c.recv(1024)
	received_message = received_message.decode()
	
	
	split_message = received_message.split(",")
	
	
	
	if split_message[0] == "1":
		try:
			sql_token = "SELECT name FROM token WHERE token_id = '"+split_message[2]+"'"
			mycursor.execute(sql_token)
			result = mycursor.fetchall()
			
			if len(result) == 0:
				warn_msg = "Please enter a valid token"
				c.send(warn_msg.encode())
	
			else:
			
				try:
					sql_name = "SELECT public_key FROM pub_key WHERE username ='"+split_message[1]+"'"
					mycursor.execute(sql_name)
					result = mycursor.fetchall()
					
					if len(result) > 0 :
						warn_msg = "The username exists in database.\nPlease pick another name"
						c.send(warn_msg.encode())
						
					else:
						account = models.Account.generate_new_account(models.NetworkType.TEST_NET)
						public_key = account.public_key
						private_key = account.private_key
						hash_object = hashlib.sha256(private_key.encode())
						hash_pk = hash_object.hexdigest()

						
						account = models.PublicAccount.create_from_public_key(public_key, models.NetworkType.TEST_NET)
						account_address = account.address.address
						network_type = str(account.address.network_type)
						
						sql_info = "INSERT INTO pub_key (username, public_key, private_key, address, network) VALUES (%s, %s, %s, %s, %s)"
						val = [(split_message[1], public_key, str(hash_pk), account_address, network_type)] 
						mycursor.executemany(sql_info, val)
						
						mydb.commit()
						
						sql_del_token = "DELETE FROM token WHERE token_id = '"+split_message[2]+"'"
						mycursor.execute(sql_del_token)
						mydb.commit()
						
						account = models.Account.create_from_private_key(private_key, models.NetworkType.TEST_NET)
						requests.get(f"https://bctestnetfaucet.xpxsirius.io/api/faucet/GetXpx/{account.address.address}").json()
						
						sucess_msg = "Account Has Been Generated\n\n"
						name = "Your Username: "+split_message[1]+"\n\n"
						priv_key = "Your Private Key: "+private_key+"\n\n"
						pub_key = "Your Public Key: "+public_key+"\n\n"
						account_address = "Account Address: "+account_address+"\n\n"
						reminder = "REMINDER: Please keep your Private Key as it wont be \nstored in the database"
						
						total_msg = sucess_msg+name+priv_key+pub_key+account_address
						f = open("account_cred.txt","w")
						f.write(total_msg)
						f.close()
						c.send(total_msg.encode())
						
				except:
					warn_msg = "Something went wrong. Please try again"
					c.send(warn_msg.encode())
		except:
			warn_msg = "Something went wrong. Please try again"
			c.send(warn_msg.encode())
			
###############################################################################################################################			
	elif split_message[0] == "2":
		try:
			sql_name = "SELECT public_key FROM pub_key WHERE username = '"+split_message[1]+"'"
			mycursor.execute(sql_name)
			
			result = mycursor.fetchall()
			public_key = str(result[0]).strip("(),'")
			print(public_key)
			
			ENDPOINT = "https://bctestnet2.brimstone.xpxsirius.io"
			account = models.PublicAccount.create_from_public_key(public_key, models.NetworkType.TEST_NET)
			
			with client.AccountHTTP(ENDPOINT) as http:
				account = http.get_account_info(account.address)
				acc_info_str = str(account)
				acc_info_array = acc_info_str.split(",")
				acc_address = acc_info_array[1].strip("address=Address(address=' '")
				network_type = acc_info_array[2].strip(" network_type=< : 168>)")
				xpx_amount = acc_info_array[9].strip(" amount= )]")
				add_comma = xpx_amount[:(len(xpx_amount)-6)]+"."+xpx_amount[6:]
				
				name = split_message[1]+"'s Account Information\n\n"
				remaining_xpx = "Remaining XPX amount: "+add_comma+"\n"
				acc_address = "Account address: "+acc_address+"\n"
				network_type = "Network type: "+network_type+"\n"
				key = "Public key: "+public_key+"\n"
				
				total_message = name +remaining_xpx+acc_address+network_type+key
				c.send(total_message.encode())
		except:
			warn_msg = "Something went wrong. The name you entered is not in the database"
			c.send(warn_msg.encode())
			
			
##################################################################################################################################
	elif split_message[0] == "3":
		#try:
		hash_split = received_message.split("#")
		
		private_key = hash_split[2]
		
		ENDPOINT = "https://bctestnet2.brimstone.xpxsirius.io"
		account = models.Account.create_from_private_key(private_key, models.NetworkType.TEST_NET)
		
		with client.AccountHTTP(ENDPOINT) as http:
	
			account = http.get_account_info(account.address)
			acc_info_str = str(account)
			acc_info_array = acc_info_str.split(",")
			acc_address = acc_info_array[1].strip("address=Address(address=' '")

		sql_addr = "SELECT username FROM pub_key WHERE address = '"+acc_address+"'"
		mycursor.execute(sql_addr)
		
		result = mycursor.fetchall()
		username = str(result[0]).strip("(),'")
			
		# except:
			# warn_msg = "Wrong Private Key Please Try Again"
			# c.send(warn_msg.encode())
			
		
		if username == hash_split[1]:
			try:
				
				verified_ammount = float(hash_split[4])
				NETWORK_TYPE = models.NetworkType.TEST_NET
				
				try:
				
					sql_name = "SELECT public_key FROM pub_key WHERE username = '"+hash_split[3]+"'"
					mycursor.execute(sql_name)
					result = mycursor.fetchall()
					receiver_public_key = str(result[0]).strip("(),'")
					print(receiver_public_key)

					nodes = [
						"bctestnet1.brimstone.xpxsirius.io:3000",
						"bctestnet2.brimstone.xpxsirius.io:3000",
						"bctestnet3.brimstone.xpxsirius.io:3000",
					]

					# Choosing one of the endpoints
					endpoint = nodes[1]    
					async def announce(tx):
						address = models.PublicAccount.create_from_public_key(tx.signer, tx.network_type).address

						# Create listener and subscribe to confirmed / unconfirmed transactions and error status
						# Subscription should occur prior to announcing the transaction
						async with client.Listener(f'{endpoint}/ws') as listener:
							await listener.confirmed(address)
							await listener.status(address)
							await listener.unconfirmed_added(address)

							# Announce the transaction to the network
							print(f"Sending {amount} XPX to {bob.address.address}\n")
							with client.TransactionHTTP(endpoint) as http:
								http.announce(tx)

							# Listener gets all messages regarding the address given but we care only
							# about our transaciton
							async for m in listener:
								if ((m.channel_name == 'status') and (m.message.hash == tx.hash.upper())):
									# An error occured and the transaction was rejected by the node
									raise errors.TransactionError(m.message)
								elif ((m.channel_name == 'unconfirmedAdded') and (m.message.transaction_info.hash == tx.hash.upper())):
									# The transaction was accepted by the node and is about to be included in a block
									print(f"Unconfirmed transaction {m.message.transaction_info.hash}")
									print("Waiting for confirmation\n")
								elif ((m.channel_name == 'confirmedAdded') and (m.message.transaction_info.hash == tx.hash.upper())):
									# The transaction was included in a block
									return m.message


					def print_account_info(account): 
						print(f"    Address: {account.address.address}")
						print(f"Private key: {account.private_key}")
						print(f" Public key: {account.public_key}")
						print()


					def print_account_mosaics(account):
						print(f"Address: {account.address.address}")

						# Get the account info
						with client.AccountHTTP(endpoint) as http:
							account_info = http.get_account_info(account.address)
						
						# Get names and divisibility of all mosaics on the account
						for mosaic in account_info.mosaics:
							with client.MosaicHTTP(endpoint) as http:
								mosaic_info = http.get_mosaic(mosaic.id)
								mosaic_names = http.get_mosaic_names([mosaic.id])
						
							divisibility = 10**mosaic_info.properties.divisibility
							name = mosaic_names[0].names[0]
							
							try:
								print(f" Mosaic: {name} {mosaic.amount / divisibility}")
							except:
								print()
						print()

					# Get network type
					with client.NodeHTTP(endpoint) as http:
						node_info = http.get_node_info()
						network_type = node_info.network_identifier

					# Get generation hash of this blockchain
					with client.BlockchainHTTP(endpoint) as http:
						block_info = http.get_block_by_height(1)

					# Get the XPX mosaic by its namespace alias. Mosaics don't have names, you can only asign an alias to them.
					# Namespace will give us the mosaic id.
					with client.NamespaceHTTP(endpoint) as http:
						namespace_info = http.get_namespace(models.NamespaceId('prx.xpx'))

					# Get mosaic info by its id.
					with client.MosaicHTTP(endpoint) as http:
						xpx = http.get_mosaic(namespace_info.alias.value)

						

					# Generate Alice's account. If we have a private key, use it. Otherwise generate a new account and ask
					# the faucet for test XPX
					alice = models.Account.create_from_private_key(private_key, network_type)

					# Generate Bob's account
					bob = models.PublicAccount.create_from_public_key(receiver_public_key, models.NetworkType.TEST_NET)
					#bob = models.Account.generate_new_account(network_type)



					# Print their addresses, private and public keys
					print_account_info(alice)



					amount = int(hash_split[4])
					
					msg = str(hash_split[5])
					message = models.PlainMessage(b'%s'%msg.encode())

					# Create transfer transactions of 1 XPX to Bob
					tx = models.TransferTransaction.create(
						deadline=models.Deadline.create(),
						recipient=bob.address,
						mosaics=[models.Mosaic(xpx.mosaic_id, amount * 10**xpx.properties.divisibility)],
						message = message,
						network_type=network_type,
					)

					# Sign the transaction with Alice's account
					signed_tx = tx.sign_with(
						account=alice, 
						gen_hash=block_info.generation_hash
					)

					# We run announce() as an asynchronous function because it uses Listener that comes
					# only in async implementation
					result = asyncio.run(announce(signed_tx))

					print(f"Confirmed transaction {result.transaction_info.hash}\n")

					# Print resulting account balances
					
					
					confirmed_msg = "A Transaction Has Been Confirmed"
					c.send(confirmed_msg.encode())

						
				except:
					warn_msg = "The recipient name is not in the databased"
					c.send(warn_msg.encode())
				
			except:
				warn_msg = "Something went wrong. Please Enter Integer For Amount"
				c.send(warn_msg.encode())
		else:
			warn_msg = "Something went wrong. Please try again later"
			c.send(warn_msg.encode())
		


##################################################################################################################################

	elif split_message[0] == "4":
		
		split_hash = received_message.split("#")
		
		try:
			private_key = str(split_hash[2])
			
			ENDPOINT = "https://bctestnet2.brimstone.xpxsirius.io"
			account = models.Account.create_from_private_key(private_key, models.NetworkType.TEST_NET)
			
			with client.AccountHTTP(ENDPOINT) as http:
		
				account = http.get_account_info(account.address)
				acc_info_str = str(account)
				acc_info_array = acc_info_str.split(",")
				acc_address = acc_info_array[1].strip("address=Address(address=' '")

			sql_addr = "SELECT username FROM pub_key WHERE address = '"+acc_address+"'"
			mycursor.execute(sql_addr)
			
			result = mycursor.fetchall()
			username = str(result[0]).strip("(),'")
			
			if username == split_hash[1]:
			
				try:
					sql_receiver = "SELECT public_key FROM pub_key WHERE username = '"+split_hash[3]+"'"
					mycursor.execute(sql_receiver)
					result = mycursor.fetchall()
					receiver_public_key = str(result[0]).strip("(),'")
					
					try:
						
						while True:
						
							number = random.randint(1000,9999)
							
							sql_nonce = "SELECT mosaic_id FROM mosaic_info WHERE nonce = '"+str(number)+"'"
							mycursor.execute(sql_nonce)
							result = mycursor.fetchall()
							
							
							if len(result) == 0:
								break
									
								
						print(number)
						
						endpoint = "bctestnet2.brimstone.xpxsirius.io:3000"
						
						async def announce(tx):
							address = models.PublicAccount.create_from_public_key(tx.signer, tx.network_type).address

							# Create listener and subscribe to confirmed / unconfirmed transactions and error status
							# Subscription should occur prior to announcing the transaction
							async with client.Listener(f'{endpoint}/ws') as listener:
								await listener.confirmed(address)
								await listener.status(address)
								await listener.unconfirmed_added(address)

								# Announce the transaction to the network
								print(f"Sending {amount} XPX to {bob.address.address}\n")
								with client.TransactionHTTP(endpoint) as http:
									http.announce(tx)

								# Listener gets all messages regarding the address given but we care only
								# about our transaciton
								async for m in listener:
									if ((m.channel_name == 'status') and (m.message.hash == tx.hash.upper())):
										# An error occured and the transaction was rejected by the node
										raise errors.TransactionError(m.message)
									elif ((m.channel_name == 'unconfirmedAdded') and (m.message.transaction_info.hash == tx.hash.upper())):
										# The transaction was accepted by the node and is about to be included in a block
										print(f"Unconfirmed transaction {m.message.transaction_info.hash}")
										print("Waiting for confirmation\n")
									elif ((m.channel_name == 'confirmedAdded') and (m.message.transaction_info.hash == tx.hash.upper())):
										# The transaction was included in a block
										return m.message


						def print_account_info(account): 
							print(f"    Address: {account.address.address}")
							print(f"Private key: {account.private_key}")
							print(f" Public key: {account.public_key}")
							print()


						def print_account_mosaics(account):
							print(f"Address: {account.address.address}")

							# Get the account info
							with client.AccountHTTP(endpoint) as http:
								account_info = http.get_account_info(account.address)
							
							# Get names and divisibility of all mosaics on the account
							for mosaic in account_info.mosaics:
								with client.MosaicHTTP(endpoint) as http:
									mosaic_info = http.get_mosaic(mosaic.id)
									mosaic_names = http.get_mosaic_names([mosaic.id])
							
								divisibility = 10**mosaic_info.properties.divisibility
								name = mosaic_names[0].names[0]

								print(f" Mosaic: {name} {mosaic.amount / divisibility}")
							print()

						# Get network type
						with client.NodeHTTP(endpoint) as http:
							node_info = http.get_node_info()
							network_type = node_info.network_identifier

						# Get generation hash of this blockchain
						with client.BlockchainHTTP(endpoint) as http:
							block_info = http.get_block_by_height(1)

						# Get the XPX mosaic by its namespace alias. Mosaics don't have names, you can only asign an alias to them.
						# Namespace will give us the mosaic id.
						with client.NamespaceHTTP(endpoint) as http:
							namespace_info = http.get_namespace(models.NamespaceId('prx.xpx'))

						# Get mosaic info by its id.
						with client.MosaicHTTP(endpoint) as http:
							xpx = http.get_mosaic(namespace_info.alias.value)


						# Generate Alice's account. If we have a private key, use it. Otherwise generate a new account and ask
						# the faucet for test XPX
						alice = models.Account.create_from_private_key(private_key, network_type)

						# Generate Bob's account
						bob = models.PublicAccount.create_from_public_key(receiver_public_key, models.NetworkType.TEST_NET)
						#bob = models.Account.generate_new_account(network_type)

						# Print their addresses, private and public keys
						print_account_info(alice)
						#print_account_info(bob)

						amount = 1
						
						mosaic_payload = split_hash[5]
						
						message = models.PlainMessage(mosaic_payload.encode())

						nonce = models.MosaicNonce(number)
						mosaic_id = models.MosaicId.create_from_nonce(nonce, alice)


						tx = models.MosaicDefinitionTransaction.create(
							deadline=models.Deadline.create(),
							network_type=network_type,
							nonce=nonce,
							mosaic_id=mosaic_id,
							mosaic_properties=models.MosaicProperties(0x1, 0), #1. Transfer 2. Supply Mutable 3. Both || Divisiblity Amount 
						)
						signed_tx = tx.sign_with(
							account=alice, 
							gen_hash=block_info.generation_hash
						)
						result = asyncio.run(announce(signed_tx))
						print(f"Confirmed transaction {result.transaction_info.hash}\n")

						tx = models.MosaicSupplyChangeTransaction.create(
							deadline=models.Deadline.create(),
							network_type=network_type,
							mosaic_id=mosaic_id,
							direction=models.MosaicSupplyType.INCREASE,
							delta=10,
						)
						signed_tx = tx.sign_with(
							account=alice, 
							gen_hash=block_info.generation_hash
						)
						result = asyncio.run(announce(signed_tx))
						print(f"Confirmed transaction {result.transaction_info.hash}\n")

						mosaic_name = split_hash[4].lower()

						tx = models.RegisterNamespaceTransaction.create_root_namespace(
							deadline=models.Deadline.create(),
							network_type=network_type,
							namespace_name=mosaic_name,
							duration=10
						)

						signed_tx = tx.sign_with(
							account=alice, 
							gen_hash=block_info.generation_hash
						)

						result = asyncio.run(announce(signed_tx))

						print(f"Confirmed transaction {result.transaction_info.hash}\n")


						namespace_id = tx.namespace_id
						tx = models.MosaicAliasTransaction.create(
							deadline=models.Deadline.create(),
							network_type=network_type,
							max_fee=1,
							action_type=models.AliasActionType.LINK,
							mosaic_id=mosaic_id,
							namespace_id=namespace_id,
						)

						signed_tx = tx.sign_with(
							account=alice, 
							gen_hash=block_info.generation_hash
						)

						result = asyncio.run(announce(signed_tx))

						print(f"Confirmed transaction {result.transaction_info.hash}\n")

						tx = models.TransferTransaction.create(
							deadline=models.Deadline.create(),
							recipient=bob.address,
							#mosaics=[models.Mosaic(xpx.mosaic_id, amount * 10**xpx.properties.divisibility)],
							mosaics=[models.Mosaic(mosaic_id, amount)],
							message = message,
							network_type=network_type,
						)

						# Sign the transaction with Alice's account
						signed_tx = tx.sign_with(
							account=alice, 
							gen_hash=block_info.generation_hash
						)

						# We run announce() as an asynchronous function because it uses Listener that comes
						# only in async implementation
						result = asyncio.run(announce(signed_tx))

						print(f"Confirmed transaction {result.transaction_info.hash}\n")

						
						
						
						confirmed_msg = "A Transaction Has Been Confirmed"
						c.send(confirmed_msg.encode())
						
					except:
						print("Third Try Problem")
						warn_msg = "There seems to be a problem when generating your contract. Plaese check your account balance."
						c.send(warn_msg.encode())
					
					
				except:
					print("Second try problem")
					warn_msg = "It appears to be the username is not registered in out database. Please try again."
					c.send(warn_msg.encode())
			else:
				print("something seems to be fishy here")
				warn_msg = "Incorrect username. Please try again"
				c.send(warn_msg.encode())
		except:
			print("Something is not right")
			warn_msg = "Incorrect private key please try again."
			c.send(warn_msg.encode())
			
			
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		today = datetoday.today()
		current_date = today.strftime("%d/%m/%Y")
		
			
		print(str(mosaic_id))
		print(mosaic_name)
		print(mosaic_payload)
		print(split_hash[3])
		

		sql = "INSERT INTO mosaic_info (mosaic_id,mosaic_name,mosaic_payload,mosaic_creator,mosaic_receiver,nonce,time,date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		val = [(str(mosaic_id), str(mosaic_name), str(mosaic_payload), str(split_hash[1]), str(split_hash[3]), number, str(current_time), str(current_date))] 
		mycursor.executemany(sql, val)
		mydb.commit()
			
		
		
	
#############################################################################################################################	
	elif split_message[0] == "5":
		#print("Five it is")
		
		username = split_message[1]
		priv_key = split_message[2]
		hash_object = hashlib.sha256(priv_key.encode())
		hash_pk = hash_object.hexdigest()
		print(hash_pk)
		
		try:
		
			sql_key = "SELECT username FROM pub_key WHERE private_key = '"+hash_pk+"'"
			mycursor.execute(sql_key)
			result = mycursor.fetchall()
			db_name = str(result[0]).strip("(),'")
		
			if db_name == username: 
			
				try:
				
					sql_name = "SELECT public_key FROM pub_key WHERE username = '"+username+"'"
					mycursor.execute(sql_name)
					
					result = mycursor.fetchall()
					public_key = str(result[0]).strip("(),'")
					print(public_key)
					
					ENDPOINT = "https://bctestnet1.brimstone.xpxsirius.io"
					account = models.PublicAccount.create_from_public_key(public_key, models.NetworkType.TEST_NET)
					tx_list = []
					
					f = open("server_side_tx_receipt.txt","w")
					
					with client.AccountHTTP(ENDPOINT) as http:
						txns = http.transactions(account)
						
						decor1 = "######################################################\n"
						
						title = "This is a list of all transaction that has occured\n"
						
						decor2 = "######################################################\n\n"
						
						first_tot_msg = decor1+title+decor2
						f.write(first_tot_msg)
						
						c.send(first_tot_msg.encode())
						
						
						for x in range (len(txns)):
							
							first_strip = str(txns[x]).strip("',")
							transaction_array = first_strip.split("=")
							transaction_hash = transaction_array[17].strip("', merkle_component_hash")
							sender_signature = transaction_array[7].strip("', signer")
							sender_address = transaction_array[10].strip("', network_type")
							
							if str(transaction_array[1]) == "<TransactionType.TRANSFER: 16724>, network_type":
							
								try:
									payload = transaction_array[28].strip("')b'")
								except:
									print("This is a contract transactions")
									
								
								
								try:
									sql = "SELECT username FROM pub_key WHERE address = '"+sender_address+"'"
									mycursor.execute(sql)
									result = mycursor.fetchall()
									username = str(result[0]).strip("()',")
									
								except:
									username = "Unknown"
									
									
								datetime_raw = transaction_array[5].strip("datetime. max_fee ( )),")
								datetime_array = datetime_raw.split(",")
								date = datetime_array[2]+"/"+datetime_array[1].strip(" ")+"/"+datetime_array[0].strip(" ")
								time = datetime_array[3]+":"+datetime_array[4].strip(" ")
								receipient_address = transaction_array[20].strip("', network_type")
								block_number = transaction_array[14].strip(", index")
								
								try:
									sql = "SELECT username FROM pub_key WHERE address = '"+receipient_address+"'"
									mycursor.execute(sql)
									result = mycursor.fetchall()
									receipient_username = str(result[0]).strip("()',")
									
								except:
									receipient_username = 'Unknown'
									
								tx_date = "Transaction Date: "+date
								
								
								split_time = str(time).split(":")
								
								if len(str(split_time[1])) < 2:
									time = str(time)+"0" 
									
									final_time = "\nTransaction Time: "+time +"\n"

								else:
									
									final_time = "\nTransaction Time: "+time +"\n"
													
								
								recv_username = "\nReceipient Username: "+receipient_username+"\n"
								
								
								block_num = "Block Number: "+block_number+"\n"
								
								content = "Message Content: "+payload+"\n"
								
								tx_hash = "Transaction Hash: "+transaction_hash+"\n"
							
								
								sender_sign = "Sender Signature: "+sender_signature+"\n"
								
								sender_addr = "Sender Address: "+sender_address+"\n"
								
								
								username = "Sender's Username: "+username+"\n"
								
								
								recv_addr = "Receipient Address: "+receipient_address+"\n"
								
								
								recv_username = "Receipient Username: "+receipient_username+"\n"
								
								decor = '***************************************************\n'
								
								
								append_tnxs = tx_date + final_time + username + sender_addr + recv_username + recv_addr + content + tx_hash + sender_sign + block_num + decor
								f.write(append_tnxs)
								c.send(append_tnxs.encode())
								
								
						fin_msg = "---\n"
						f.write(fin_msg)
						f.close()
						c.send(fin_msg.encode())
						
						g = open("server_side_tx_receipt.txt","r")
						read_file = g.read()
						
						key = "sharmelen"
						mac_code = hmac.new(key.encode(), read_file.encode(), hashlib.sha256).hexdigest()
						mac_code = str(mac_code)+" =end="
						
						c.send(mac_code.encode())
						
						

				except:
					warn_msg = "Incorrect private key please try again."
					c.send(warn_msg.encode())
					
			else:
				error_msg = "Wrong Credentials"
				c.send(error_msg.encode())
				
		except:
			
			error_msg = "Wrong Credentials"
			c.send(error_msg.encode())
			
	elif split_message[0] == "6":
	
		try:
		
			username = split_message[1]
			priv_key = split_message[2]
			
			hash_object = hashlib.sha256(priv_key.encode())
			hash_pk = hash_object.hexdigest()
			
			sql_key = "SELECT username FROM pub_key WHERE private_key = '"+hash_pk+"'"
			mycursor.execute(sql_key)
			result_0 = mycursor.fetchall()
			db_name = str(result_0[0]).strip("(),'")
			
			if db_name == username:
				
				#try:
				
				
				sql_all_name = "SELECT public_key FROM pub_key"
				mycursor.execute(sql_all_name)

				result_1 = mycursor.fetchall()
				#print(str(result[2]).strip("(),'"))

				ENDPOINT = "https://bctestnet1.brimstone.xpxsirius.io"
				
				for x in range (len(result_1)):

					public_keys = str(result_1[x]).strip("(),'")
					#print(public_keys)

					account = models.PublicAccount.create_from_public_key(public_keys, models.NetworkType.TEST_NET)
					
					with client.AccountHTTP(ENDPOINT) as http:
						
						txns = http.transactions(account)
						
						for x in range (len(txns)):
												
							first_strip = str(txns[x]).strip("',")
							transaction_array = first_strip.split("=")
							transaction_hash = transaction_array[17].strip("', merkle_component_hash")
							sender_signature = transaction_array[7].strip("', signer")
							sender_address = transaction_array[10].strip("', network_type")
							
							if str(transaction_array[1]) == "<TransactionType.TRANSFER: 16724>, network_type":
							
								try:
									payload = transaction_array[28].strip("')b'")
								except:
									print("This is a contract transaction")
												
								try:
									sql = "SELECT username FROM pub_key WHERE address = '"+sender_address+"'"
									mycursor.execute(sql)
									result = mycursor.fetchall()
									username = str(result[0]).strip("()',")
									
								except:
									username = "Unknown"
									
									
								datetime_raw = transaction_array[5].strip("datetime. max_fee ( )),")
								datetime_array = datetime_raw.split(",")
								date = datetime_array[2]+"/"+datetime_array[1].strip(" ")+"/"+datetime_array[0].strip(" ")
								time = datetime_array[3]+":"+datetime_array[4].strip(" ")
								receipient_address = transaction_array[20].strip("', network_type")
								block_number = transaction_array[14].strip(", index")
								
								try:
									sql = "SELECT username FROM pub_key WHERE address = '"+receipient_address+"'"
									mycursor.execute(sql)
									result = mycursor.fetchall()
									receipient_username = str(result[0]).strip("()',")
									
								except:
									receipient_username = 'Unknown'
									
								tx_date = "Transaction Date: "+date
								
								
								split_time = str(time).split(":")
								
								if len(str(split_time[1])) < 2:
									time = str(time)+"0" 
									
									final_time = "\nTransaction Time: "+time +"\n"

								else:
									
									final_time = "\nTransaction Time: "+time +"\n"
									
								
								#print(final_time)
								
								
								sql_check = "SELECT sender_address FROM transaction_info WHERE tx_hash = '"+transaction_hash+"'"
								mycursor.execute(sql_check)
								result = mycursor.fetchall()
								
								if len(result) > 0 :
									print(result[0])
									print("NOT RECORDED")
								
								else:
									sql_insert = "INSERT INTO transaction_info (tx_hash, sender_signature, sender_address, sender_username, receiver_address, receiver_username, payload, date, time, block_num) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
									
									val = [(transaction_hash, sender_signature, sender_address, username, receipient_address,receipient_username, payload, date, time, block_number)] 
									mycursor.executemany(sql_insert, val)
									mydb.commit()
								
						
				keywords = ['tx_hash','sender_signature','sender_address','sender_username','receiver_address','receiver_username','payload','date','time','block_num']

				tx_array = []
							
				for x in range (len(keywords)):		
							
					sql_txinfo = "SELECT "+keywords[x]+" FROM transaction_info ORDER BY block_num DESC"
					mycursor.execute(sql_txinfo)
					result = mycursor.fetchall()
					
					for x in range (len(result)):
						single_tx = str(result[x]).strip("(),'")
						tx_array.append(single_tx)
				
				f = open("transaction_ledger_server_side.txt", "w")	
				
				decor_msg = "\n####################################################################\n"
				msg1 = "Transaction Ledger"
				total_msg = decor_msg+msg1+decor_msg
				c.send(total_msg.encode())
				
				f.write(total_msg)
				
				for x in range (len(result)):

					len_info = len(result) 
					
					msg2 = "Transaction Hash: "+tx_array[x]+"\n"
					msg3 = "Sender Signature: "+tx_array[x+len_info]+"\n"
					msg4 = "Sender Address: "+tx_array[x+len_info * 2]+"\n"
					msg5 = "Sender Username: "+tx_array[x+len_info * 3]+"\n"
					msg6 = "Receiver Address: "+tx_array[x+len_info * 4]+"\n"
					msg7 = "Receiver Username: "+ tx_array[x+len_info * 5]+"\n"
					msg8 = "Content: "+ tx_array[x+len_info * 6]+"\n"
					msg9 = "Date: "+ tx_array[x+len_info * 7]+"\n"
					msg10 = "Time: "+tx_array[x+len_info * 8]+"\n"
					msg11 = "Block Number: "+tx_array[x+len_info * 9]+"\n"
					msg12 = '*****************************************************\n'
					

					total_msg2 = msg2+msg3+msg4+msg5+msg6+msg7+msg8+msg9+msg10+msg11+msg12
					c.send(total_msg2.encode())
					f.write(total_msg2)

				
				fin_msg = "---\n"
				c.send(fin_msg.encode())
				f.write(fin_msg)
				
				f.close()
				
				f = open("transaction_ledger_server_side.txt", "r")
				text = f.read()
				print(text)
				
				key = "sharmelen"
				mac_code = hmac.new(key.encode(), text.encode(), hashlib.sha256).hexdigest()
				mac_code = str(mac_code)+" =end="
				c.send(mac_code.encode())
				
				# mac_title = "\n\nTHIS IS MESSAGE AUTHENTICATION CODE\n\n"
				# f.write(mac_title)
				# c.send(mac_title.encode())
			


				# except:
					# warn_msg = "Incorrect username please try again"
					# c.send(warn_msg.encode())
				
			else:
				error_msg = "Wrong Credentials"
				c.send(error_msg.encode())
				
		except:
			
			error_msg = "Wrong Credentials"
			c.send(error_msg.encode())
			
	elif split_message[0] == '7':
	
		username = split_message[1]
		priv_key = split_message[2]
		
		hash_object = hashlib.sha256(priv_key.encode())
		hash_pk = hash_object.hexdigest()
		
		sql_key = "SELECT username FROM pub_key WHERE private_key = '"+hash_pk+"'"
		mycursor.execute(sql_key)
		result_0 = mycursor.fetchall()
		db_name = str(result_0[0]).strip("(),'")
		
		if username == db_name:
			sql_mosaic = "SELECT * FROM mosaic_info WHERE mosaic_creator = '"+username+"'"
			mycursor.execute(sql_mosaic)
			mosaic_result = mycursor.fetchall()
			
			f = open("transaction_contract_server_side.txt", "w")
			decor_msg = "*************************************\n"
			title_contract = "LIST OF CONTRACTS\n"
			f.write(decor_msg+title_contract+decor_msg)
			
			title_msg = decor_msg+title_contract+decor_msg
			c.send(title_msg.encode())
			
			
			
			for x in range (len(mosaic_result)):
			
				single_mosaic = mosaic_result[x] 
				
				mosaic_id = "Mosaic ID: " + single_mosaic[0].strip("MosaicId(id=(),'")+"\n"
				mosaic_name = "Mosaic Name: " +single_mosaic[1].strip("(),'")+"\n"
				mosaic_payload = "Mosaic Payload: "+single_mosaic[2].strip("(),'")+"\n"
				mosaic_creator = "Mosaic Creator: " +single_mosaic[3].strip("(),'")+"\n"
				mosaic_receiver = "Mosaic Receiver: "+single_mosaic[4].strip("(),'")+"\n"
				mosaic_time = "Mosaic Time: "+single_mosaic[6].strip("(),'")+"\n"
				mosaic_date = "Mosaic Date: "+single_mosaic[7].strip("(),'")+"\n"
				decor_msg2 = "***************************************************\n"
				
				total_msg = mosaic_id+mosaic_name+mosaic_payload+mosaic_creator+mosaic_receiver+mosaic_time+mosaic_date+decor_msg2
				f.write(total_msg)
				
				c.send(total_msg.encode())
			
			fin_msg = "---\n"
			f.write(fin_msg)
			f.close()
			
			c.send(fin_msg.encode())
			
			f = open("transaction_contract_server_side.txt", "r")
			read_contract = f.read()
			
			key = "sharmelen"
			mac_code = hmac.new(key.encode(), read_contract.encode(), hashlib.sha256).hexdigest()
			mac_code = str(mac_code)+" =end="
			
			c.send(mac_code.encode())
			print(mac_code)
				
				
	
	
	elif split_message[0] == "8":
		
		split_hash = received_message.split("#")
		
		#try:
		private_key = str(split_hash[2])
		
		ENDPOINT = "https://bctestnet2.brimstone.xpxsirius.io"
		account = models.Account.create_from_private_key(private_key, models.NetworkType.TEST_NET)
		
		with client.AccountHTTP(ENDPOINT) as http:
	
			account = http.get_account_info(account.address)
			acc_info_str = str(account)
			acc_info_array = acc_info_str.split(",")
			acc_address = acc_info_array[1].strip("address=Address(address=' '")

		sql_addr = "SELECT username FROM pub_key WHERE address = '"+acc_address+"'"
		mycursor.execute(sql_addr)
		
		result = mycursor.fetchall()
		username = str(result[0]).strip("(),'")
			
		if username == split_hash[1]:
		
			#try:
			sql_receiver = "SELECT public_key FROM pub_key WHERE username = '"+split_hash[3]+"'"
			mycursor.execute(sql_receiver)
			result = mycursor.fetchall()
			receiver_public_key = str(result[0]).strip("(),'")
			
			number = split_hash[4]
			sql_nonce = "SELECT mosaic_name FROM mosaic_info WHERE nonce = '"+str(number)+"'"
			mycursor.execute(sql_nonce)
			result = mycursor.fetchall()
			contract_name = str(result[0]).strip("(),'")
			
			#try:
				
			endpoint = "bctestnet2.brimstone.xpxsirius.io:3000"
			
			async def announce(tx):
				address = models.PublicAccount.create_from_public_key(tx.signer, tx.network_type).address

				# Create listener and subscribe to confirmed / unconfirmed transactions and error status
				# Subscription should occur prior to announcing the transaction
				async with client.Listener(f'{endpoint}/ws') as listener:
					await listener.confirmed(address)
					await listener.status(address)
					await listener.unconfirmed_added(address)

					# Announce the transaction to the network
					print(f"Sending {amount} XPX to {bob.address.address}\n")
					with client.TransactionHTTP(endpoint) as http:
						http.announce(tx)

					# Listener gets all messages regarding the address given but we care only
					# about our transaciton
					async for m in listener:
						if ((m.channel_name == 'status') and (m.message.hash == tx.hash.upper())):
							# An error occured and the transaction was rejected by the node
							raise errors.TransactionError(m.message)
						elif ((m.channel_name == 'unconfirmedAdded') and (m.message.transaction_info.hash == tx.hash.upper())):
							# The transaction was accepted by the node and is about to be included in a block
							print(f"Unconfirmed transaction {m.message.transaction_info.hash}")
							print("Waiting for confirmation\n")
						elif ((m.channel_name == 'confirmedAdded') and (m.message.transaction_info.hash == tx.hash.upper())):
							# The transaction was included in a block
							return m.message


			def print_account_info(account): 
				print(f"    Address: {account.address.address}")
				print(f"Private key: {account.private_key}")
				print(f" Public key: {account.public_key}")
				print()


			def print_account_mosaics(account):
				print(f"Address: {account.address.address}")

				# Get the account info
				with client.AccountHTTP(endpoint) as http:
					account_info = http.get_account_info(account.address)
				
				# Get names and divisibility of all mosaics on the account
				for mosaic in account_info.mosaics:
					with client.MosaicHTTP(endpoint) as http:
						mosaic_info = http.get_mosaic(mosaic.id)
						mosaic_names = http.get_mosaic_names([mosaic.id])
				
					divisibility = 10**mosaic_info.properties.divisibility
					name = mosaic_names[0].names[0]

					print(f" Mosaic: {name} {mosaic.amount / divisibility}")
				print()

			# Get network type
			with client.NodeHTTP(endpoint) as http:
				node_info = http.get_node_info()
				network_type = node_info.network_identifier

			# Get generation hash of this blockchain
			with client.BlockchainHTTP(endpoint) as http:
				block_info = http.get_block_by_height(1)

			# Get the XPX mosaic by its namespace alias. Mosaics don't have names, you can only asign an alias to them.
			# Namespace will give us the mosaic id.
			with client.NamespaceHTTP(endpoint) as http:
				namespace_info = http.get_namespace(models.NamespaceId('prx.xpx'))

			# Get mosaic info by its id.
			with client.MosaicHTTP(endpoint) as http:
				xpx = http.get_mosaic(namespace_info.alias.value)


			# Generate Alice's account. If we have a private key, use it. Otherwise generate a new account and ask
			# the faucet for test XPX
			alice = models.Account.create_from_private_key(private_key, network_type)

			# Generate Bob's account
			bob = models.PublicAccount.create_from_public_key(receiver_public_key, models.NetworkType.TEST_NET)
			#bob = models.Account.generate_new_account(network_type)

			# Print their addresses, private and public keys
			print_account_info(alice)
			#print_account_info(bob)

			amount = 1
			
			mosaic_payload = split_hash[5]
			
			message = models.PlainMessage(mosaic_payload.encode())
			
			numbers = int(number)
			nonce = models.MosaicNonce(numbers)
			mosaic_id = models.MosaicId.create_from_nonce(nonce, alice)



			tx = models.TransferTransaction.create(
				deadline=models.Deadline.create(),
				recipient=bob.address,
				#mosaics=[models.Mosaic(xpx.mosaic_id, amount * 10**xpx.properties.divisibility)],
				mosaics=[models.Mosaic(mosaic_id, amount)],
				message = message,
				network_type=network_type,
			)

			# Sign the transaction with Alice's account
			signed_tx = tx.sign_with(
				account=alice, 
				gen_hash=block_info.generation_hash
			)

			# We run announce() as an asynchronous function because it uses Listener that comes
			# only in async implementation
			result = asyncio.run(announce(signed_tx))

			print(f"Confirmed transaction {result.transaction_info.hash}\n")

			
			sql_del_contract = "DELETE FROM mosaic_info WHERE nonce = '"+str(number)+"'"
			mycursor.execute(sql_del_contract)
			mydb.commit()
			
			
			confirmed_msg = "A Transaction Has Been Confirmed"
			c.send(confirmed_msg.encode())
				
			
		else:
			print("something seems to be fishy here")
			warn_msg = "Incorrect username. Please try again"
			c.send(warn_msg.encode())
	
		
		
while True:
	server()

