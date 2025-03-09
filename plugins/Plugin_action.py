import os
import sys
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s",
    filename="plugin.log",
    filemode="w",
)

try:
    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        version = "python{}.{}".format(sys.version_info.major, sys.version_info.minor)
        venv_site_packages = os.path.join(venv, "lib", version, "site-packages")

        if venv_site_packages in sys.path:
            sys.path.remove(venv_site_packages)

        sys.path.insert(0, venv_site_packages)

    import wx
    from kipy import KiCad
except Exception as e:
    logging.exception("Import Module")


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

    def __init__(self, kicad: KiCad, board):
        super(KiCadPlugin, self).__init__(None)
        self.board = board
        self.kicad = kicad

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)
        self.timer.Start(1000)

    def onTimer(self, event):
        try:
            self.kicad.ping()  # always returns zero
        except:
            logging.debug("ping failed.")
            self.timer.Stop()
            self.Close()
        pass

    def run(self, event):
        self.m_staticText.SetLabel("Working...")
        wx.MessageBox("Done", parent=self)
        self.m_staticText.SetLabel("Done")


class ActionKiCadPlugin:

    def __init__(self, kicad: KiCad):
        self.kicad = kicad
        self.Run()

    def Run(self):
        logging.debug("run()")
        logging.debug(f"Connected to KiCad {self.kicad.get_version()}")
        try:
            board = self.kicad.get_board()
        except:
            board = None
            logging.ERROR("Open board.")

        plugin_dialog = KiCadPlugin(self.kicad, board)
        plugin_dialog.ShowModal()
        plugin_dialog.Destroy()
        logging.debug("stop plugin")


if __name__ == "__main__":
    logging.debug("Start main()")
    app = wx.App(False)

    try:
        kicad = KiCad()
        plugin = ActionKiCadPlugin(kicad)
    except Exception as e:
        logging.exception("__main__")

    app.MainLoop()
