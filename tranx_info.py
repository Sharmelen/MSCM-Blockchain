import wx
import socket
import sys
import hashlib, hmac, binascii

app = wx.App()
win = wx.Frame(None, title="Information Account", size=(470, 200))
win.SetBackgroundColour('white')

vbox = wx.BoxSizer(wx.VERTICAL)
font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
font.SetPointSize(9)
##############################################################################################################

server_ip = "127.0.0.1"
server_port = 5000

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
	s.connect(("127.0.0.1", server_port))
	
	
except:
	wx.MessageBox('It seems the server to be down.\nPlease try again later', 'ERROR',wx.OK | wx.ICON_ERROR)
	sys.exit()
	
def account_info(event):
	
	username = input_text1.GetValue()
	priv_key = input_text1_2.GetValue()
	
	if not username :
		wx.MessageBox('Please Enter Username', 'ERROR',wx.OK | wx.ICON_ERROR)
	
		
	else:
		message_input = "5,"+username+","+priv_key
		s.send(message_input.encode())
		f = open("transaction_receipt.txt", "w")
		while True:
			server_msg = s.recv(1024)
			server_msg = server_msg.decode()
			print(server_msg)
			
			
			f.write(server_msg)
			
			
			if "=end=" in server_msg:
				f.close()
				break
				
			elif "Wrong Credentials" in server_msg:
				wx.MessageBox('You have entered wrong credentials','ERROR',wx.OK | wx.ICON_INFORMATION)
				break
		try:		
			check_mac("transaction_receipt.txt")
		except:
			print()
		#wx.MessageBox(server_msg, 'Notification',wx.OK | wx.ICON_INFORMATION)
		#print(server_msg)
		sys.exit()
		
def tranx_ledger(event):

	username = input_text1.GetValue()
	priv_key = input_text1_2.GetValue()
	
	if not username :
		wx.MessageBox('Please Enter Username', 'ERROR',wx.OK | wx.ICON_ERROR)
	
		
	else:
		message_input = "6,"+username+","+priv_key
		s.send(message_input.encode())
		f = open("transaction_ledger.txt", "w")

		
		while True:
			server_msg = s.recv(1024)
			server_msg = server_msg.decode()
			print(server_msg)
			
			
			f.write(server_msg)
			
			
			if "=end=" in server_msg:
				f.close()
			
				break
				
			if "Wrong Credentials" in server_msg:
				
				wx.MessageBox('You have entered wrong credentials','ERROR',wx.OK | wx.ICON_INFORMATION)
				break
		try:	
			check_mac("transaction_ledger.txt")
			
		except:
			print()
		#print(server_msg)
		sys.exit()
		
def tranx_contract(event):
	
	username = input_text1.GetValue()
	priv_key = input_text1_2.GetValue()
	
	if not username :
		wx.MessageBox('Please Enter Username', 'ERROR',wx.OK | wx.ICON_ERROR)
	
		
	else:
		message_input = "7,"+username+","+priv_key
		s.send(message_input.encode())
		f = open("transaction_contract.txt", "w")

		
		while True:
			server_msg = s.recv(1024)
			server_msg = server_msg.decode()
			print(server_msg)
			
			
			f.write(server_msg)
			
			
			if "=end=" in server_msg:
				f.close()
			
				break
				
			if "Wrong Credentials" in server_msg:
				
				wx.MessageBox('You have entered wrong credentials','ERROR',wx.OK | wx.ICON_INFORMATION)
				break
		try:	
			check_mac("transaction_ledger.txt")
			
		except:
			print()
		#print(server_msg)
		sys.exit()
		
		
def check_mac(filename):

	f = open(filename,"r")
	read_text = f.read()

	split_text = read_text.split("---")

	g = open("newtest.txt","w")
	g.write(split_text[0])
	g.write("---\n")
	g.close()

	v = open("newtest.txt","r")
	read_file = v.read()
	key = "sharmelen"
	mac_code = hmac.new(key.encode(), read_file.encode(), hashlib.sha256).hexdigest()

	if str(mac_code) in split_text[1]:
		print("The mac code is equal")	
		
		wx.MessageBox('This is a valid ledger!!','Notification',wx.OK | wx.ICON_INFORMATION)
		
	else:
		wx.MessageBox('This is a invalid ledger!!','Notification',wx.OK | wx.ICON_INFORMATION)

##############################################################################################################
hbox1 = wx.BoxSizer(wx.HORIZONTAL)
st1 = wx.StaticText(win, label = "Username: ")

st1.SetFont(font)
hbox1.Add(st1, flag = wx.RIGHT, border = 8)

try:

	f = open("account_cred.txt","r")
	read = f.read()
	split = read.split("\n")
	your_name = split[2].replace("Your Username: ","")
	
except:
	your_name = ""
	#wx.MessageBox('Please Generate An Account First', 'ERROR',wx.OK | wx.ICON_ERROR)


input_text1 = wx.TextCtrl(win, value = str(your_name))
hbox1.Add(input_text1, proportion = 1)

vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
##############################################################################################################
hbox1_2 = wx.BoxSizer(wx.HORIZONTAL)
st1_2 = wx.StaticText(win, label = "Private Key: ")

st1_2.SetFont(font)
hbox1_2.Add(st1_2,flag = wx.RIGHT, border = 8)

try:
	f = open("account_cred.txt","r")

	your_key = split[4].replace("Your Private Key: ","")
	
except:
	your_key = ""

input_text1_2 = wx.TextCtrl(win, value = str(your_key), style = wx.TE_PASSWORD)
hbox1_2.Add(input_text1_2, proportion = 1)

vbox.Add(hbox1_2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
##############################################################################################################

vbox.Add((-1,20))

hbox2 = wx.BoxSizer(wx.HORIZONTAL)

acc_info = wx.Button(win, label = 'Transaction Information', size = (150,30))
hbox2.Add(acc_info)
acc_info.Bind(wx.EVT_BUTTON, account_info)

tx_ledger = wx.Button(win, label = 'Transaction Ledger', size = (150, 30))
hbox2.Add(tx_ledger, flag = wx.LEFT, border = 10)
tx_ledger.Bind(wx.EVT_BUTTON, tranx_ledger)

tx_contract = wx.Button(win, label = "Contract Receipts", size = (150,30))
hbox2.Add(tx_contract, flag = wx.LEFT, border = 10)
tx_contract.Bind(wx.EVT_BUTTON, tranx_contract)

vbox.Add(hbox2, flag = wx.CENTER, border = 10)

win.SetSizer(vbox)

win.Show()
app.MainLoop()