import wx
import socket
import sys

app = wx.App()
win = wx.Frame(None, title="Information Account", size=(410, 200))
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
	
	if not username :
		wx.MessageBox('Please Enter Username', 'ERROR',wx.OK | wx.ICON_ERROR)

	else:
		message_input = "2,"+username
		s.send(message_input.encode())
		
		server_msg = s.recv(1024)
		server_msg = server_msg.decode()
		wx.MessageBox(server_msg, 'Notification',wx.OK | wx.ICON_INFORMATION)
		sys.exit()

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

vbox.Add((-1,20))

hbox2 = wx.BoxSizer(wx.HORIZONTAL)

acc_info = wx.Button(win, label = 'Account Information', size = (150,30))
hbox2.Add(acc_info)
acc_info.Bind(wx.EVT_BUTTON, account_info)
vbox.Add(hbox2, flag = wx.CENTER)

win.SetSizer(vbox)

win.Show()
app.MainLoop()