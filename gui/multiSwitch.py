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

import gui.builtinViews.emptyView
from gui.chromeTabs import PFNotebook
from gui.utils.helpers_wxPython import Frame
import wx


class MultiSwitch(PFNotebook):
    def __init__(self, parent):
        PFNotebook.__init__(self, parent)
        self.SetBackgroundColour(Frame.getBackgroundColor())
        # self.AddPage() # now handled by mainFrame
        self.handlers = handlers = []
        for tab_type in TabSpawner.tabTypes:
            handlers.append(tab_type(self))

    def handleDrag(self, drag_type, info):
        for handler in self.handlers:
            h = getattr(handler, "handleDrag", None)
            if h:
                h(drag_type, info)

    def AddPage(self, tabWnd=None, tabTitle="Empty Tab", tabImage=None, showClose=True):
        if tabWnd is None:
            tabWnd = gui.builtinViews.emptyView.BlankPage(self)
            tabWnd.handleDrag = lambda drag_type, info: self.handleDrag(drag_type, info)

        PFNotebook.AddPage(self, tabWnd, tabTitle, tabImage, True)

    def DeletePage(self, n, *args, **kwargs):
        PFNotebook.DeletePage(self, n, *args, **kwargs)
        if self.GetPageCount() == 0:
            self.AddPage()


class TabSpawner(object):
    tabTypes = []

    @classmethod
    def register(cls):
        TabSpawner.tabTypes.append(cls)
