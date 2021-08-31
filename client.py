import wx
import os

def generate_account(event):
	print("You Pressed First")
	os.system('python generate_account.py')
	
def account_info(event):
	print("You Pressed Second")
	os.system('python account_information.py')
	
def make_tranx(event):
	print("You Pressed Third")
	os.system('python transaction.py')
	
def mosaic_tranx(event):
	print("You Pressed Fourth")
	os.system('python mosaic_tranx.py')
	
def tranx_info(event):
	print("You Pressed Fifth")
	os.system('python tranx_info.py')
	
def cancel_mosaic(event):
	print("You Pressed Sixth")
	os.system('python mosaic_null.py')

app = wx.App()
win = wx.Frame(None, title="ProximaX Sirius", size=(410, 200))
win.SetBackgroundColour('white')

vbox = wx.BoxSizer(wx.VERTICAL)

################################################################################
hbox1 = wx.BoxSizer(wx.HORIZONTAL)

gen_acc =  wx.Button(win, label = 'Generate Account', size = (150,30))
hbox1.Add(gen_acc)
gen_acc.Bind(wx.EVT_BUTTON, generate_account)

acc_info = wx.Button(win, label = 'Account Info', size = (150,30))
hbox1.Add(acc_info, flag = wx.LEFT, border = 10)
acc_info.Bind(wx.EVT_BUTTON, account_info)

vbox.Add(hbox1, flag = wx.CENTER, border=10)

################################################################################

vbox.Add((-1,20))

hbox2 = wx.BoxSizer(wx.HORIZONTAL)

make_tx = wx.Button(win, label = 'Send a Message',size = (150,30))
hbox2.Add(make_tx)
make_tx.Bind(wx.EVT_BUTTON, make_tranx)

tx_info = wx.Button(win, label = 'Generate A Contract', size = (150, 30))
hbox2.Add(tx_info, flag = wx.LEFT, border = 10)
tx_info.Bind(wx.EVT_BUTTON, mosaic_tranx)

vbox.Add(hbox2, flag = wx.CENTER, border = 10)

################################################################################

vbox.Add((-1,20))

hbox3 = wx.BoxSizer(wx.HORIZONTAL)

transaction_info = wx.Button(win, label = 'Get Transaction Info', size = (150,30))
hbox3.Add(transaction_info)
transaction_info.Bind(wx.EVT_BUTTON, tranx_info)

mosaic_cancel = wx.Button(win, label = 'Cancel A Contract', size = (150, 30))
hbox3.Add(mosaic_cancel, flag = wx.LEFT, border = 10)
mosaic_cancel.Bind(wx.EVT_BUTTON, cancel_mosaic)

vbox.Add(hbox3, flag = wx.CENTER)

###################################################################################


win.SetSizer(vbox)

win.Show()

app.MainLoop()