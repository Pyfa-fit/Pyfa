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

from service.fit import Fit
from service.settings import StatViewSettings, GeneralSettings
import gui.mainFrame
import gui.builtinStatsViews
import gui.globalEvents as GE
from gui.statsView import StatsView
from gui.contextMenu import ContextMenu
from gui.pyfatogglepanel import TogglePanel
from logbook import Logger

pyfalog = Logger(__name__)


class StatsPane(wx.Panel):
    AVAILIBLE_VIEWS = [
        "resources",
        "resistances",
        "recharge",
        "firepower",
        "outgoing",
        "capacitor",
        "targetingMisc",
        "price",
        "drone"
    ]

    # Don't have these....yet....
    '''
    "miningyield", "drones"
    ]
    '''

    DEFAULT_VIEWS = []

    settings = StatViewSettings.getInstance()

    for aView in AVAILIBLE_VIEWS:
        if settings.get(aView) == 2:
            DEFAULT_VIEWS.extend(["%sViewFull" % aView])
            pyfalog.debug("Setting full view for: {0}", aView)
        elif settings.get(aView) == 1:
            DEFAULT_VIEWS.extend(["%sViewMinimal" % aView])
            pyfalog.debug("Setting minimal view for: {0}", aView)
        elif settings.get(aView) == 0:
            pyfalog.debug("Setting disabled view for: {0}", aView)
        else:
            pyfalog.error("Unknown setting for view: {0}", aView)

    test = True

    def fitChanged(self, event):
        sFit = Fit.getInstance()
        fit = sFit.getFit(event.fitID)
        for view in self.views:
            view.refreshPanel(fit)
        event.Skip()

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        general_settings = GeneralSettings.getInstance()

        # Set the font size used on the stats pane
        font = wx.Font(
                general_settings.get('fontSize'),
                getattr(wx, 'FONTFAMILY_' + general_settings.get('fontType'), wx.FONTFAMILY_DEFAULT),
                getattr(wx, 'FONTSTYLE_' + general_settings.get('fontStyle'), wx.FONTSTYLE_NORMAL),
                getattr(wx, 'FONTWEIGHT_' + general_settings.get('fontWeight'), wx.FONTWEIGHT_NORMAL),
        )
        self.SetFont(font)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        self.views = []
        self.nameViewMap = {}
        maxviews = len(self.DEFAULT_VIEWS)
        i = 0
        for viewName in self.DEFAULT_VIEWS:
            tp = TogglePanel(self)
            contentPanel = tp.GetContentPane()
            contentPanel.viewName = viewName

            try:
                view = StatsView.getView(viewName)(self)
                pyfalog.debug("Load view: {0}", viewName)
            except KeyError:
                pyfalog.error("Attempted to load an invalid view: {0}", viewName)

            self.nameViewMap[viewName] = view
            self.views.append(view)

            headerPanel = tp.GetHeaderPanel()

            view.populatePanel(contentPanel, headerPanel)
            tp.SetLabel(view.getHeaderText(None))
            view.refreshPanel(None)

            contentPanel.Bind(wx.EVT_RIGHT_DOWN, self.contextHandler(contentPanel))
            for child in contentPanel.GetChildren():
                child.Bind(wx.EVT_RIGHT_DOWN, self.contextHandler(contentPanel))

            mainSizer.Add(tp, 0, wx.EXPAND | wx.LEFT, 3)
            if i < maxviews - 1:
                mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, style=wx.HORIZONTAL), 0,
                              wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 2)
            i += 1
            tp.OnStateChange(tp.GetBestSize())

        width, height = self.GetSize()
        self.SetMinSize((width + 9, -1))

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)

    @staticmethod
    def contextHandler(contentPanel):
        viewName = contentPanel.viewName

        def handler(event):
            menu = ContextMenu.getMenu(None, (viewName,))
            if menu is not None:
                contentPanel.PopupMenu(menu)

            event.Skip()

        return handler
