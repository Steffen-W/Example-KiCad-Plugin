import pcbnew
import os
import wx


class MyDialog(wx.Dialog):
    def __init__(self, parent):
        super(MyDialog, self).__init__(parent, title="Minimal", size=(300, 150))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText = wx.StaticText(panel, label="Text")
        sizer.Add(self.m_staticText, 0, wx.ALL | wx.CENTER, 10)

        self.m_runButton = wx.Button(panel, wx.ID_ANY, label="Run")
        sizer.Add(self.m_runButton, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.run, self.m_runButton)

    def run(self, event):
        pass


class KiCadPlugin(MyDialog):
    def __init__(self, board, action):
        super(KiCadPlugin, self).__init__(None)
        self.board = board
        self.action = action

    def run(self, event):
        self.m_staticText.SetLabel("Working...")
        wx.MessageBox("Done", parent=self)
        self.m_staticText.SetLabel("Done")


class ActionKiCadPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Minimal KiCad Plugin"
        self.category = "Example"
        self.description = "Minimalbeispiel eines KiCad Plugins"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "icon.png")
        self.dark_icon_file_name = os.path.join(os.path.dirname(__file__), "icon.png")

    def Run(self):
        board = pcbnew.GetBoard()
        plugin_dialog = KiCadPlugin(board, self)
        plugin_dialog.ShowModal()
        plugin_dialog.Destroy()
        pcbnew.Refresh()
