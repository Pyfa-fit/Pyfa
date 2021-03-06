# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

# noinspection PyPackageRequirements
import wx
from gui.preferenceView import PreferenceView
from gui.bitmapLoader import BitmapLoader
from service.settings import SettingsProvider, GeneralSettings
from logbook import Logger
from gui.utils.helpers_wxPython import Fonts, Frame

pyfalog = Logger(__name__)


class PreferenceDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.SetTitle("Pyfa.fit - Preferences")
        i = wx.IconFromBitmap(BitmapLoader.getBitmap("preferences_small", "gui"))
        self.SetIcon(i)
        self.SetFont(Fonts.getFont("font_standard"))
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.listbook = wx.Listbook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LB_DEFAULT)
        self.listbook.SetBackgroundColour(Frame.getBackgroundColor())

        preferences_listview = self.listbook.Children[0]

        preferences_listview.SetBackgroundColour(Frame.getBackgroundColorOffset())
        preferences_listview.SetForegroundColour(Frame.getForegroundColor())
        preferences_listview.Size.x = self.listbook.GetTextExtent("Statistics Panels")[0]
        # preferences_listview.SetSize((self.listbook.GetTextExtent("Statistics Panels")[0], -1))

        '''
        self.listbook.Children[0].SetBackgroundColour(Frame.getBackgroundColorOffset())
        self.listbook.Children[0].SetForegroundColour(Frame.getForegroundColor())
        self.listbook.Children[0].SetSize((self.listbook.GetTextExtent("Statistics Panels")[0], -1))
        test = self.listbook.Children[0]
        '''

        self.imageList = wx.ImageList(32, 32)
        self.listbook.SetImageList(self.imageList)

        mainSizer.Add(self.listbook, 1, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 5)

        self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline2, 0, wx.EXPAND, 5)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        self.btnOK = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer.Add(self.btnOK, 0, wx.ALL, 5)
        mainSizer.Add(btnSizer, 0, wx.EXPAND, 5)
        self.SetSizer(mainSizer)

        self.Centre(wx.BOTH)

        for prefView in PreferenceView.views:
            page = wx.Panel(self.listbook)
            page.SetForegroundColour(Frame.getForegroundColor())
            bmp = prefView.getImage()
            if bmp:
                imgID = self.imageList.Add(bmp)
            else:
                imgID = -1
            prefView.populatePrefPanel(page)
            self.listbook.AddPage(page, prefView.title, imageId=imgID)

        self.generalSettings = GeneralSettings.getInstance()
        fontSize = self.generalSettings.get("fontSize")

        window_x = 900
        window_y = 450

        # Set the height based on a condition. Can all the panels fit in the current height?
        # If not, use the .GetBestVirtualSize() to ensure that all content is available.
        bestFit = self.GetBestVirtualSize()
        if window_y < bestFit[1]:
            window_y = bestFit[1]

        if fontSize > 9:
            window_x *= 1.25

        self.SetSizeWH(window_x, window_y)

        self.Layout()

        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOK)

    def OnBtnOK(self, event):
        pyfalog.debug("Saving preferences.")
        self.Close()
        SettingsProvider.getInstance().saveAll()
