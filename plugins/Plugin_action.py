import os
import wx
from kipy import KiCad


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


class ActionKiCadPlugin:

    def __init__(self, kicad: KiCad = None):
        self.kicad = kicad
        print("init")

    def defaults(self):
        print("defaults(self):")
        self.name = "Minimal KiCad Plugin"
        self.category = "Example"
        self.description = "Minimal example of a KiCad plugin"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "icon.png")
        self.dark_icon_file_name = os.path.join(os.path.dirname(__file__), "icon.png")

    def Run(self):
        print("Run(self):")
        # kicad = KiCad()
        board = self.kicad.get_board()
        plugin_dialog = KiCadPlugin(board, self)
        plugin_dialog.ShowModal()
        plugin_dialog.Destroy()


if __name__ == "__main__":
    try:
        kicad = KiCad()
        plugin = ActionKiCadPlugin(kicad)
        plugin.Run()
        print(f"Connected to KiCad {kicad.get_version()}")
    except BaseException as e:
        print(f"Not connected to KiCad: {e}")
