import wx
from threading import Thread
import time

EVT_UPDATE_ID = wx.NewId()


def EVT_UPDATE(win, func):
    win.Connect(-1, -1, EVT_UPDATE_ID, func)


class ResultEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_UPDATE_ID)
        self.data = data


class PluginThread(Thread):
    def __init__(self, wxObject):
        Thread.__init__(self)
        self.wxObject = wxObject
        self.stopThread = False
        self.start()

    def run(self):
        i = 0
        while (not self.stopThread):
            time.sleep(1)
            i = i+1
            self.report(str(i))

    def report(self, status):
        wx.PostEvent(self.wxObject, ResultEvent(status))
