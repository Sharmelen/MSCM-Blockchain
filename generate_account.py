import wx
import socket
import sys

app = wx.App()
win = wx.Frame(None, title="Generate Account", size=(410, 200))
win.SetBackgroundColour('white')

vbox = wx.BoxSizer(wx.VERTICAL)

font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
font.SetPointSize(9)
##################################################################################

server_ip = "127.0.0.1"
server_port = 5000

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
	s.connect(("127.0.0.1", server_port))
	
	
except:
	wx.MessageBox('It seems the server to be down.\nPlease try again later', 'ERROR',wx.OK | wx.ICON_ERROR)
	sys.exit()

def generate_account(event):
	token = input_text1.GetValue()
	username = input_text2.GetValue()
	
	if not (username and token) :
		wx.MessageBox('Incomplete Information', 'ERROR',wx.OK | wx.ICON_ERROR)	
		
	else:
		#print(username+" and "+token)
		message_input = "1,"+username+","+token
		s.send(message_input.encode())
		
		server_msg = s.recv(1024)
		server_msg = server_msg.decode()
		wx.MessageBox(server_msg, 'Notification',wx.OK | wx.ICON_INFORMATION)
		
		sys.exit()
		
def generate_cache(event):
	token = input_text1.GetValue()
	username = input_text2.GetValue()
	
	if not (username and token) :
		wx.MessageBox('Incomplete Information', 'ERROR',wx.OK | wx.ICON_ERROR)	
		
	else:
		#print(username+" and "+token)
		message_input = "1,"+username+","+token
		s.send(message_input.encode())
		
		server_msg = s.recv(1024)
		server_msg = server_msg.decode()
		f = open("account_cred.txt", "w")
		f.write(server_msg)
		f.close()
		wx.MessageBox(server_msg, 'Notification',wx.OK | wx.ICON_INFORMATION)
		
		sys.exit()


#############################################################################
hbox1 = wx.BoxSizer(wx.HORIZONTAL)
st1 = wx.StaticText(win, label = "Token: ")

st1.SetFont(font)
hbox1.Add(st1, flag = wx.RIGHT, border = 8)

input_text1 = wx.TextCtrl(win)
hbox1.Add(input_text1, proportion = 1)

vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

#############################################################################
vbox.Add((-1,20))

hbox2 = wx.BoxSizer(wx.HORIZONTAL)
st2 = wx.StaticText(win, label = "Username: ")
st2.SetFont(font)
hbox2.Add(st2, flag = wx.RIGHT, border = 8)

input_text2 = wx.TextCtrl(win)
hbox2.Add(input_text2,proportion = 1)
vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

###############################################################################
vbox.Add((-1,20))

hbox3 = wx.BoxSizer(wx.HORIZONTAL)

gen_acc = wx.Button(win, label = 'Generate', size = (150,30))
hbox3.Add(gen_acc)
gen_acc.Bind(wx.EVT_BUTTON, generate_account)

gen_cache = wx.Button(win, label = 'Generate and Cache', size = (150,30))
hbox3.Add(gen_cache, flag = wx.LEFT, border = 10)
gen_cache.Bind(wx.EVT_BUTTON, generate_cache)
vbox.Add(hbox3, flag = wx.CENTER)

win.SetSizer(vbox)
win.Show()

app.MainLoop()

