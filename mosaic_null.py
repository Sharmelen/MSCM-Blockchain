import wx
import socket
import sys

app = wx.App()
win = wx.Frame(None, title="Transaction", size=(410, 450))
win.SetBackgroundColour('white')

vbox = wx.BoxSizer(wx.VERTICAL)

font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
font.SetPointSize(9)

vbox = wx.BoxSizer(wx.VERTICAL)
font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
font.SetPointSize(9)
##############################################################################

server_ip = "127.0.0.1"
server_port = 5000

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
	s.connect(("127.0.0.1", server_port))
	
	
except:
	wx.MessageBox('It seems the server to be down.\nPlease try again later', 'ERROR',wx.OK | wx.ICON_ERROR)
	sys.exit()
	
	
def mosaic_tranx(event):
	
	username = input_text1.GetValue()
	private_key = input_text2.GetValue()
	receiver = input_text3.GetValue()
	mosaic_id = input_text4.GetValue()
	mosaic_payload = input_text6.GetValue()
	
	if not (username and private_key and receiver and mosaic_id and mosaic_payload):
		wx.MessageBox('Please Fill In All Required Information', 'ERROR',wx.OK | wx.ICON_ERROR)
		sys.exit()
	else:
			
		try:
			msg_len = len(mosaic_payload)
			if msg_len > 1025:
				print("Message length exceeds 1024 bytes")
			
			else:
				total_message = "8,#"+username+"#"+private_key+"#"+receiver+"#"+mosaic_id+"#"+mosaic_payload
				s.send(total_message.encode())
				
				server_msg = s.recv(1024)
				server_msg = server_msg.decode()
				wx.MessageBox(server_msg, 'Notification',wx.OK | wx.ICON_INFORMATION)
				
		except:
			print("something went wrong at client side")
				
			
			

		
	sys.exit()	

##############################################################################
hbox1 = wx.BoxSizer(wx.HORIZONTAL)
st1 = wx.StaticText(win, label = "Username: ")

st1.SetFont(font)
hbox1.Add(st1, flag = wx.RIGHT, border = 8)

try:

	f = open("account_cred.txt","r")
	read = f.read()
	split = read.split("\n")
	your_name = split[2].replace("Your Username: ","")
	your_key = split[4].replace("Your Private Key: ","")
except:
	your_name = ""
	your_key = ""
	#wx.MessageBox('Please Generate An Account First', 'ERROR',wx.OK | wx.ICON_ERROR)


input_text1 = wx.TextCtrl(win, value = str(your_name))
hbox1.Add(input_text1, proportion = 1)

vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

#############################################################################
vbox.Add((-1,20))

hbox2 = wx.BoxSizer(wx.HORIZONTAL)
st2 = wx.StaticText(win, label = "Private Key: ")
st2.SetFont(font)
hbox2.Add(st2, flag = wx.RIGHT, border = 8)



input_text2 = wx.TextCtrl(win, value = str(your_key) ,style = wx.TE_PASSWORD)
hbox2.Add(input_text2,proportion = 1)
vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

###############################################################################

vbox.Add((-1,20))

hbox3 = wx.BoxSizer(wx.HORIZONTAL)
st3 = wx.StaticText(win, label = "Recipient Name: ")
st3.SetFont(font)
hbox3.Add(st3, flag = wx.RIGHT, border = 8)

input_text3 = wx.TextCtrl(win)
hbox3.Add(input_text3,proportion = 1)
vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

###############################################################################

vbox.Add((-1,20))

hbox4 = wx.BoxSizer(wx.HORIZONTAL)
st4 = wx.StaticText(win, label = "Contract ID: ")
st4.SetFont(font)
hbox4.Add(st4, flag = wx.RIGHT, border = 8)

input_text4 = wx.TextCtrl(win)
hbox4.Add(input_text4,proportion = 1)
vbox.Add(hbox4, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

################################################################################

vbox.Add((-1,20))

hbox5 = wx.BoxSizer(wx.HORIZONTAL)
st5 = wx.StaticText(win, label = "Reasons For Return: ")
st5.SetFont(font)
hbox5.Add(st5)
vbox.Add(hbox5, flag=wx.LEFT | wx.TOP, border=10)

##############################################################################
vbox.Add((-1,10))

hbox6 = wx.BoxSizer(wx.HORIZONTAL)
input_text6 = wx.TextCtrl(win,style=wx.TE_MULTILINE)
input_text6.SetHint("Reasons:")
hbox6.Add(input_text6, proportion=1, flag=wx.EXPAND)
vbox.Add(hbox6, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND,border=10)

##############################################################################

vbox.Add((-1,20))

hbox7 = wx.BoxSizer(wx.HORIZONTAL)

mosaic_tx = wx.Button(win, label = 'Make Transaction', size = (150,30))
hbox7.Add(mosaic_tx)
mosaic_tx.Bind(wx.EVT_BUTTON, mosaic_tranx)
vbox.Add(hbox7, flag = wx.CENTER)

win.SetSizer(vbox)

win.Show()
app.MainLoop()
