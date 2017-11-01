import wx
from wx.lib.intctrl import IntCtrl

from gui.preferenceView import PreferenceView
from gui.bitmapLoader import BitmapLoader
from gui.utils import helpers_wxPython as wxHelpers
import config
from eos.db.saveddata.queries import clearPrices, clearDamagePatterns, clearTargetResists
from eos.db.saveddata.loadDefaultDatabaseValues import DefaultDatabaseValues
from service.settings import DatabaseSettings
from service.esi import esiItems, esiDogma
import sys
from gui.utils.helpers_wxPython import Fonts

import logging

logger = logging.getLogger(__name__)


class PFDatabasePref(PreferenceView):
    def refreshPanel(self, fit):
        pass

    title = "Database"

    def __init__(self):
        self.databaseSettings = DatabaseSettings.getInstance()

    def populatePrefPanel(self, panel):
        self.dirtySettings = False

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(Fonts.getFont("font_title_plus_one"))
        mainSizer.Add(self.stTitle, 0, wx.ALL, 5)

        self.stSubTitle = wx.StaticText(panel, wx.ID_ANY, u"Cannot be changed while pyfa is running. Set via command line switches.",
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.stSubTitle.Wrap(-1)
        mainSizer.Add(self.stSubTitle, 0, wx.ALL, 3)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        # Save in Root
        self.cbsaveInRoot = wx.CheckBox(panel, wx.ID_ANY, u"Using Executable Path for Saved Fit Database and Settings", wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbsaveInRoot, 0, wx.ALL | wx.EXPAND, 5)

        # Database path
        self.stSetUserPath = wx.StaticText(panel, wx.ID_ANY, u"pyfa User Path:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stSetUserPath.Wrap(-1)
        mainSizer.Add(self.stSetUserPath, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.inputUserPath = wx.TextCtrl(panel, wx.ID_ANY, config.savePath, wx.DefaultPosition, wx.DefaultSize, 0)
        self.inputUserPath.SetEditable(False)
        self.inputUserPath.SetBackgroundColour((200, 200, 200))
        mainSizer.Add(self.inputUserPath, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        # Save DB
        self.stFitDB = wx.StaticText(panel, wx.ID_ANY, u"Fitting Database:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stFitDB.Wrap(-1)
        mainSizer.Add(self.stFitDB, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.inputFitDB = wx.TextCtrl(panel, wx.ID_ANY, config.saveDB, wx.DefaultPosition, wx.DefaultSize, 0)
        self.inputFitDB.SetEditable(False)
        self.inputFitDB.SetBackgroundColour((200, 200, 200))
        mainSizer.Add(self.inputFitDB, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        # Game Data DB
        self.stGameDB = wx.StaticText(panel, wx.ID_ANY, u"Game Database:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stGameDB.Wrap(-1)
        mainSizer.Add(self.stGameDB, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.inputGameDB = wx.TextCtrl(panel, wx.ID_ANY, config.gameDB, wx.DefaultPosition, wx.DefaultSize, 0)
        self.inputGameDB.SetEditable(False)
        self.inputGameDB.SetBackgroundColour((200, 200, 200))
        mainSizer.Add(self.inputGameDB, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.cbsaveInRoot.SetValue(config.saveInRoot)
        self.cbsaveInRoot.Bind(wx.EVT_CHECKBOX, self.onCBsaveInRoot)

        # self.inputUserPath.Bind(wx.EVT_LEAVE_WINDOW, self.OnWindowLeave)
        # self.inputFitDB.Bind(wx.EVT_LEAVE_WINDOW, self.OnWindowLeave)
        # self.inputGameDB.Bind(wx.EVT_LEAVE_WINDOW, self.OnWindowLeave)

        self.m_staticline2 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline2, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.stSubTitleTwo = wx.StaticText(panel, wx.ID_ANY, u"DANGER ZONE!\nUsing these options will permanantly delete data out of the database.",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.stSubTitleTwo.Wrap(-1)
        mainSizer.Add(self.stSubTitleTwo, 0, wx.ALL, 3)

        self.m_staticline3 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline3, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL | wx.ALIGN_LEFT)

        self.btnDeleteDamagePatterns = wx.Button(panel, wx.ID_ANY, u"Delete All Damage Pattern Profiles", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer.Add(self.btnDeleteDamagePatterns, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        self.btnDeleteTargetResists = wx.Button(panel, wx.ID_ANY, u"Delete All Target Resist Profiles", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer.Add(self.btnDeleteTargetResists, 0, wx.ALL, 5)

        self.btnPrices = wx.Button(panel, wx.ID_ANY, u"Delete All Prices", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer.Add(self.btnPrices, 0, wx.ALL, 5)

        mainSizer.Add(btnSizer, 0, wx.EXPAND | wx.ALIGN_LEFT, 5)

        self.btnDeleteDamagePatterns.Bind(wx.EVT_BUTTON, self.DeleteDamagePatterns)
        self.btnDeleteTargetResists.Bind(wx.EVT_BUTTON, self.DeleteTargetResists)
        self.btnPrices.Bind(wx.EVT_BUTTON, self.DeletePrices)

        self.m_staticline4 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline4, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.stSubTitleTwo = wx.StaticText(panel, wx.ID_ANY, u"Update Game Data Database\n"
                                                             u"Enabling these options will increase the length of time it takes to update.",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.stSubTitleTwo.Wrap(-1)
        mainSizer.Add(self.stSubTitleTwo, 0, wx.ALL, 3)

        self.m_staticline5 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline5, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.btnUpdateDatabase = wx.Button(panel, wx.ID_ANY, u"Update Database", wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.btnUpdateDatabase, 0, wx.ALL, 5)

        self.cbImportItemsNotInMarketGroups = wx.CheckBox(panel, wx.ID_ANY, u"Import items not in market groups.",
                                                          wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbImportItemsNotInMarketGroups, 0, wx.ALL | wx.EXPAND, 5)

        self.cbImportItemsNotPublished = wx.CheckBox(panel, wx.ID_ANY, u"Import items that are not published.",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.cbImportItemsNotPublished, 0, wx.ALL | wx.EXPAND, 5)

        delayTimer = wx.BoxSizer(wx.HORIZONTAL)

        self.stUpdateThreads = wx.StaticText(panel, wx.ID_ANY, u"Threads to use when updating the database:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stUpdateThreads.Wrap(-1)
        self.stUpdateThreads.SetToolTip(
                wx.ToolTip('More threads may speed up updating the database, but typically little gain is seen above 25.'))

        delayTimer.Add(self.stUpdateThreads, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.intDelay = IntCtrl(panel, max=100, limited=True)
        delayTimer.Add(self.intDelay, 0, wx.ALL, 5)

        mainSizer.Add(delayTimer, 0, wx.ALL | wx.EXPAND, 0)

        self.intDelay.SetValue(self.databaseSettings.get("UpdateThreads"))
        self.cbImportItemsNotInMarketGroups.SetValue(self.databaseSettings.get("ImportItemsNotInMarketGroups"))
        self.cbImportItemsNotPublished.SetValue(self.databaseSettings.get("ImportItemsNotPublished"))

        self.btnUpdateDatabase.Bind(wx.EVT_BUTTON, self.UpdateDatabase)
        self.intDelay.Bind(wx.lib.intctrl.EVT_INT, self.OnWindowLeave)
        self.cbImportItemsNotInMarketGroups.Bind(wx.EVT_CHECKBOX, self.OnWindowLeave)
        self.cbImportItemsNotPublished.Bind(wx.EVT_LEAVE_WINDOW, self.OnWindowLeave)

        panel.SetSizer(mainSizer)
        panel.Layout()

    @staticmethod
    def DeleteDamagePatterns():
        question = u"This is a destructive action that will delete all damage pattern profiles.\nAre you sure you want to do this?"
        if wxHelpers.YesNoDialog(question, u"Confirm"):
            clearDamagePatterns()
            DefaultDatabaseValues.importRequiredDefaults()

    @staticmethod
    def DeleteTargetResists():
        question = u"This is a destructive action that will delete all target resist profiles.\nAre you sure you want to do this?"
        if wxHelpers.YesNoDialog(question, u"Confirm"):
            clearTargetResists()
            DefaultDatabaseValues.importRequiredDefaults()

    @staticmethod
    def DeletePrices():
        question = u"This is a destructive action that will delete all cached prices out of the database.\nAre you sure you want to do this?"
        if wxHelpers.YesNoDialog(question, u"Confirm"):
            clearPrices()

    @staticmethod
    def UpdateDatabase(test):
        question = u"This will take a significant amount of time.  Once the update is complete, Pyfa will restart.\n" \
                   u"Pyfa will become unresponsive until the update is complete.  Would you like to proceed?"
        if wxHelpers.YesNoDialog(question, u"Confirm"):
            loadDlg = wxHelpers.PopupDialog(None, "Updating... (1/2)", "Updating item types.\n\nPlease wait....")
            sESI = esiItems.getInstance()
            sESI.updateTypes()

            loadDlg.Destroy()
            loadDlg = wxHelpers.PopupDialog(None, "Updating... (2/2)", "Updating dogma stats.\n\nPlease wait....")
            sDogma = esiDogma.getInstance()
            sDogma.updateAllDogmaTables()

            loadDlg.Destroy()
            wxHelpers.OKDialog(u"Database upgrade completed successfully.\nPlease restart Pyfa.", u"Database Upgrade")
            sys.exit()

    def onCBsaveInRoot(self, event):
        # We don't want users to be able to actually change this,
        # so if they try and change it, set it back to the current setting
        self.cbsaveInRoot.SetValue(config.saveInRoot)

    def getImage(self):
        return BitmapLoader.getBitmap("settings_database", "gui")

    def OnWindowLeave(self, event):
        self.databaseSettings.set('UpdateThreads', int(self.intDelay.GetValue()))
        self.databaseSettings.set('ImportItemsNotInMarketGroups', int(self.cbImportItemsNotInMarketGroups.GetValue()))
        self.databaseSettings.set("ImportItemsNotPublished", self.cbImportItemsNotPublished.GetValue())


PFDatabasePref.register()
