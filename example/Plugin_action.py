import pcbnew
import os
import wx
import time

if __name__ == "__main__":
    from Plugin_gui import MyDialog
    from Plugin_event import *
else:
    from .Plugin_gui import MyDialog
    from .Plugin_event import *


class KiCadPlugin(MyDialog):

    def __init__(self, board, action):
        super(KiCadPlugin, self).__init__(None)
        self.board = board
        self.action = action
        self.config = {}
        EVT_UPDATE(self, self.updateDisplay)
        self.Thread = PluginThread(self)

    def run(self, event):  # Button in GUI
        self.m_checkBox.SetLabelText("Working...")
        time.sleep(1)
        wx.MessageBox("Done", parent=self)
        self.m_checkBox.SetLabelText("Done")

    def on_close(self, event):
        self.Thread.stopThread = True
        self.EndModal(wx.ID_OK)

    def updateDisplay(self, status):
        # pcbnew.Refresh()
        temp = status.data
        self.m_staticText.SetLabelText(temp)


class ActionKiCadPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "name"
        self.category = "category"
        self.description = "description"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(
            os.path.dirname(__file__), "icon.png")
        self.dark_icon_file_name = os.path.join(
            os.path.dirname(__file__), "icon.png")

    def Run(self):
        board = pcbnew.GetBoard()
        Plugin_h = KiCadPlugin(board, self)
        Plugin_h.ShowModal()
        Plugin_h.Destroy()
        pcbnew.Refresh()


if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, title="KiCad Plugin")
    KiCadPlugin_t = KiCadPlugin(None, None)
    KiCadPlugin_t.ShowModal()
    KiCadPlugin_t.Destroy()
