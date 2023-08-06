import wx
from TimesheetExcelEditor.MyPanel import MyPanel


class MyFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, title="Editor", size=(640, 480),
                         style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.CenterOnScreen()
        self.EnableMaximizeButton(False)
        self.panel = MyPanel(self)
        super().Show()


def main():
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
