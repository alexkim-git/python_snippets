
import  sys
import  wx
import  os
from AxVO import *

import win32com.client
stk_app = win32com.client.Dispatch("STKX10.Application")
print "HostID =" + stk_app.HostID
print "RegID  =" + stk_app.RegistrationID
print "Version=" + stk_app.Version


# This is how you pre-establish a file filter so that the dialog
# only shows the extension(s) you want it tstk_app.
wildcard = "STK Scenario (*.sc)|*.sc|"        \
           "All files (*.*)|*.*"


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
    	wx.Frame.__init__(self, parent, -1, 'Python STK/X VO Example',(0,0), (900, 600))
    	self.SetBackgroundColour(wx.Colour(255, 255, 255))
    	#self.SetBackgroundColour(wx.Colour(0, 0, 0))
    	#self.Enable(1)


    	self.stk = None
    	self.stk = AxVO(self, size=(900,500))
    	stk_app.ExecuteCommand("New / Scenario MyScen")

    	# Load scenario
    	buttonLoad = wx.Button(self, 512, "Load Scenario")
    	buttonLoad.SetPosition((10, 505))
    	self.Bind(wx.EVT_BUTTON, self.Load, buttonLoad)

    	# Animation Buttons
    	#RESET
    	gifReset = wx.EmptyBitmap(0,0)
    	gifReset.LoadFile("reset.gif", wx.BITMAP_TYPE_GIF)
    	buttonReset=wx.BitmapButton(self,-1,gifReset)
    	buttonReset.SetPosition((150, 505))
    	self.Bind(wx.EVT_BUTTON, self.Reset, buttonReset)

    	#STEP IN REVERSE
    	gifStepBak = wx.EmptyBitmap(0,0)
    	gifStepBak.LoadFile("stepbak.gif", wx.BITMAP_TYPE_GIF)
    	buttonStepBack=wx.BitmapButton(self,-1,gifStepBak)
    	buttonStepBack.SetPosition((175, 505))
    	self.Bind(wx.EVT_BUTTON, self.StepBack, buttonStepBack)

    	#REVERSE
    	gifReverse = wx.EmptyBitmap(0,0)
    	gifReverse.LoadFile("playbak.GIF", wx.BITMAP_TYPE_GIF)
    	buttonReverse=wx.BitmapButton(self,-1,gifReverse)
    	buttonReverse.SetPosition((200, 505))
    	self.Bind(wx.EVT_BUTTON, self.Reverse, buttonReverse)

    	#PAUSE
    	gifPause = wx.EmptyBitmap(0,0)
    	gifPause.LoadFile("pause.gif", wx.BITMAP_TYPE_GIF)
    	buttonPause=wx.BitmapButton(self,-1,gifPause)
    	buttonPause.SetPosition((225, 505))
    	self.Bind(wx.EVT_BUTTON, self.Pause, buttonPause)

    	#FORWARD
    	gifPlay = wx.EmptyBitmap(0,0)
    	gifPlay.LoadFile("play.gif", wx.BITMAP_TYPE_GIF)
    	buttonPlay=wx.BitmapButton(self,-1,gifPlay)
    	buttonPlay.SetPosition((250, 505))
    	self.Bind(wx.EVT_BUTTON, self.Play, buttonPlay)

    	#STEPFWD
    	gifStepFwd = wx.EmptyBitmap(0,0)
    	gifStepFwd.LoadFile("step.gif", wx.BITMAP_TYPE_GIF)
    	buttonStepFwd=wx.BitmapButton(self,-1,gifStepFwd)
    	buttonStepFwd.SetPosition((275, 505))
    	self.Bind(wx.EVT_BUTTON, self.Step, buttonStepFwd)

    	#SLOWER
    	gifSlower = wx.EmptyBitmap(0,0)
    	gifSlower.LoadFile("slower.gif", wx.BITMAP_TYPE_GIF)
    	buttonSlower=wx.BitmapButton(self,-1,gifSlower)
    	buttonSlower.SetPosition((300, 505))
    	self.Bind(wx.EVT_BUTTON, self.Slower, buttonSlower)

    	#FASTER
        gifFaster = wx.EmptyBitmap(0,0)
        gifFaster.LoadFile("faster.gif", wx.BITMAP_TYPE_GIF)
        buttonFaster=wx.BitmapButton(self,-1,gifFaster)
        buttonFaster.SetPosition((325, 505))
        self.Bind(wx.EVT_BUTTON, self.Faster, buttonFaster)

        '''
        gifAction = wx.EmptyBitmap(0,0)
        gifAction.LoadFile("action.gif", wx.BITMAP_TYPE_GIF)
        buttonAction=wx.BitmapButton(self,-1,gifAction)
        buttonAction.SetPosition((350, 505))
        '''
        self.Bind(EVT_MouseDown, self.OnMouseDown)
        self.Bind(EVT_MouseWheel, self.OnMouseWheel)
        self.Bind(EVT_KeyPress, self.onKeyPress)

    def onKeyPress(self, event):
        print event.KeyAscii

    def OnMouseDown(self, event):
        if event.Shift==2:
            print event.X,event.Y

    def OnMouseWheel(self, event):
        if event.Shift == 2:
            stk_app.ExecuteCommand("Zoom * AllOut")
        print event.Delta


    def OnCloseMe(self, event):
    	self.Close(True)

    def Load(self, event):
    	# Create the dialog. In this case the current directory is forced as the starting
    	# directory for the dialog. This is an 'open' dialog.
    	dlg = wx.FileDialog(
    	    self, message="Choose a file", defaultDir=os.getcwd(),
    	    defaultFile="", wildcard=wildcard, style=wx.OPEN
    	    )

    	# Show the dialog and retrieve the user response. If it is the OK response,
    	# process the data.
    	if dlg.ShowModal() == wx.ID_OK:
    	    # This returns the file that was selected.
    	    path = dlg.GetPath()
    	    stk_app.ExecuteCommand("Unload / *")
    	    path = "\"" + path + "\""
    	    stk_app.ExecuteCommand("Load / Scenario " + path)

    	    returnData = stk_app.ExecuteCommand("AllInstanceNames /")
    	    print "AllInstanceNames=" + returnData[0]

    	    #returnData = stk_app.ExecuteCommand("GetReport */Target/MyTarget \"Access\" Satellite/MySatellite")
    	    #print "Report=" + returnData[0]
    	    #print "Report=" + returnData[1]
    	    #print "Report=" + returnData[2]

    	    #print "-->" + path + "<--"

    	# Destroy the dialog. Don't do this until you are done with it!
    	# BAD things can happen otherwise!
    	dlg.Destroy()

    def Reset(self, event):
    	stk_app.ExecuteCommand("Animate * Reset")
    def StepBack(self, event):
    	stk_app.ExecuteCommand("Animate * Step Reverse")
    def Reverse(self, event):
    	stk_app.ExecuteCommand("Animate * Start Reverse")
    def Pause(self, event):
    	stk_app.ExecuteCommand("Animate * Pause")
    def Play(self, event):
    	stk_app.ExecuteCommand("Animate * Start Forward")
    def Step(self, event):
    	stk_app.ExecuteCommand("Animate * Step Forward")
    def Slower(self, event):
    	stk_app.ExecuteCommand("Animate * Slower")
    def Faster(self, event):
    	stk_app.ExecuteCommand("Animate * Faster")


#---------------------------------------------------------------------------
class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None, 'None')
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

app = MyApp(True)
app.MainLoop()
