import wx
from . import config
from TimesheetExcelEditor.ListPanel import ListPanel
from TimesheetExcelEditor.FormPanel import FormPanel
from TimesheetExcelEditor.CalendarPanel import CalendarPanel
from TimesheetExcelEditor.Excel import Excel


class MyPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        self.vbox = wx.BoxSizer(wx.VERTICAL)

        filebox = wx.BoxSizer(wx.HORIZONTAL)
        excel = wx.StaticText(self, label="File Excel")
        filebox.Add(excel, proportion=0, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=5)
        self.fPath = wx.TextCtrl(self, style=wx.TE_READONLY)
        filebox.Add(self.fPath, proportion=1, flag=wx.ALIGN_TOP | wx.LEFT | wx.RIGHT | wx.TOP, border=5)
        self.loadButton = wx.Button(self, label='Scegli file', size=(80, 25))
        self.loadButton.Bind(wx.EVT_BUTTON, self.__load_button_press)
        filebox.Add(self.loadButton, proportion=0, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=5)
        self.vbox.Add(filebox, proportion=0, flag=wx.EXPAND | wx.TOP, border=5)

        activitybox = wx.BoxSizer(wx.HORIZONTAL)
        acl = wx.StaticText(self, label="Attività")
        activitybox.Add(acl, proportion=0, flag=wx.LEFT, border=15)
        config.acSelect = wx.ComboBox(self, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        activitybox.Add(config.acSelect, proportion=1, flag=wx.LEFT, border=10)
        config.acSelect.Disable()
        ml = wx.StaticText(self, label="Moltiplicatore")
        activitybox.Add(ml, proportion=0, flag=wx.LEFT, border=10)
        config.multiplier = wx.ComboBox(self, size=(150, 25), choices=["1", "1.25", "1.5", "1.75", "2"],
                                        style=wx.CB_DROPDOWN | wx.CB_READONLY)
        activitybox.Add(config.multiplier, proportion=1, flag=wx.LEFT | wx.RIGHT, border=10)
        config.multiplier.SetSelection(0)
        self.vbox.Add(activitybox, proportion=0, flag=wx.TOP, border=10)

        tabox = wx.BoxSizer(wx.HORIZONTAL)
        self.notebook = wx.Notebook(self)
        form = FormPanel(self.notebook)
        listtab = ListPanel(self.notebook)
        caltab = CalendarPanel(self.notebook)
        self.notebook.AddPage(form, "FORM")
        self.notebook.AddPage(listtab, "LISTA")
        self.notebook.AddPage(caltab, "CALENDAR")
        tabox.Add(self.notebook, proportion=1, flag=wx.EXPAND | wx.TOP, border=5)
        self.vbox.Add(tabox, proportion=1, flag=wx.EXPAND | wx.TOP, border=5)

        self.SetSizer(self.vbox)

    def __load_button_press(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "", "Exel files (*.xlsx)|*.xlsx",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        directory, filename = openFileDialog.GetDirectory(), openFileDialog.GetFilename()
        config.file = Excel(directory, filename)
        self.fPath.SetValue(config.file.getPath())
        config.formModifyButton.Enable()
        config.listModifyButton.Enable()
        config.calModifyButton.Enable()
        lis = config.file.getHeaders()
        config.acSelect.Enable()
        for keys in lis:
            config.acSelect.Append(lis[keys])
        config.acSelect.SetSelection(0)
