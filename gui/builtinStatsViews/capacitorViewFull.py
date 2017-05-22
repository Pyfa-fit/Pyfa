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
from gui.statsView import StatsView
from gui.bitmapLoader import BitmapLoader
from gui.utils.numberFormatter import formatAmount


class CapacitorViewFull(StatsView):
    name = "capacitorViewFull"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent

    def getHeaderText(self, fit):
        return "Capacitor"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent(text)
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        parent = self.panel = contentPanel
        self.headerPanel = headerPanel

        panel = "full"

        sizerCapacitor = wx.GridSizer(1, 2)
        contentSizer.Add(sizerCapacitor, 0, wx.EXPAND, 0)
        # Capacitor capacity and time
        baseBox = wx.BoxSizer(wx.HORIZONTAL)

        sizerCapacitor.Add(baseBox, 0, wx.ALIGN_LEFT)
        bitmap = BitmapLoader.getStaticBitmap("capacitorInfo_big", parent, "gui")
        tooltip = wx.ToolTip("Capacitor stability")
        bitmap.SetToolTip(tooltip)
        baseBox.Add(bitmap, 0, wx.ALIGN_CENTER)

        box = wx.BoxSizer(wx.VERTICAL)
        baseBox.Add(box, 0, wx.ALIGN_LEFT)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(hbox, 0, wx.ALIGN_LEFT)

        hbox.Add(wx.StaticText(parent, wx.ID_ANY, "Total: "), 0, wx.ALIGN_LEFT | wx.LEFT, 3)
        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
        setattr(self, "label%sCapacitorCapacity" % panel.capitalize(), lbl)
        hbox.Add(lbl, 0, wx.ALIGN_LEFT)

        hbox.Add(wx.StaticText(parent, wx.ID_ANY, " GJ"), 0, wx.ALIGN_LEFT)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(hbox, 0, wx.ALIGN_LEFT)

        lbl = wx.StaticText(parent, wx.ID_ANY, "Lasts ")
        hbox.Add(lbl, 0, wx.ALIGN_LEFT | wx.LEFT, 3)
        setattr(self, "label%sCapacitorState" % panel.capitalize(), lbl)

        lbl = wx.StaticText(parent, wx.ID_ANY, "0s")
        setattr(self, "label%sCapacitorTime" % panel.capitalize(), lbl)
        hbox.Add(lbl, 0, wx.ALIGN_LEFT)

        # Capacitor balance
        baseBox = wx.BoxSizer(wx.HORIZONTAL)

        sizerCapacitor.Add(baseBox, 0, wx.ALIGN_CENTER_HORIZONTAL)

        tooltip = wx.ToolTip("Capacitor peak regen and module usage")
        bitmap = BitmapLoader.getStaticBitmap("capacitorRecharge_big", parent, "gui")
        bitmap.SetToolTip(tooltip)
        baseBox.Add(bitmap, 0, wx.ALIGN_CENTER)

        # Recharge
        chargeSizer = wx.FlexGridSizer(2, 3)
        baseBox.Add(chargeSizer, 0, wx.ALIGN_CENTER)

        chargeSizer.Add(wx.StaticText(parent, wx.ID_ANY, "Peak: "), 0, wx.ALIGN_CENTER)
        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
        setattr(self, "label%sCapacitorRecharge" % panel.capitalize(), lbl)
        chargeSizer.Add(lbl, 0, wx.ALIGN_CENTER)
        chargeSizer.Add(wx.StaticText(parent, wx.ID_ANY, " GJ/s"), 0, wx.ALIGN_CENTER)

        # Discharge
        chargeSizer.Add(wx.StaticText(parent, wx.ID_ANY, "Used: "), 0, wx.ALIGN_CENTER)
        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
        setattr(self, "label%sCapacitorDischarge" % panel.capitalize(), lbl)
        chargeSizer.Add(lbl, 0, wx.ALIGN_CENTER)
        chargeSizer.Add(wx.StaticText(parent, wx.ID_ANY, " GJ/s"), 0, wx.ALIGN_CENTER)

    def refreshPanel(self, fit):
        # If we did anything intresting, we'd update our labels to reflect the new fit's stats here
        stats = (
            ("label%sCapacitorCapacity", lambda: fit.ship.getModifiedItemAttr("capacitorCapacity"), 3, 0, 9),
            ("label%sCapacitorRecharge", lambda: fit.capRecharge['DeltaAmount'], 3, 0, 0),
            ("label%sCapacitorDischarge", lambda: fit.capUsed, 3, 0, 0),
        )

        if fit:
            neut_resist = fit.ship.getModifiedItemAttr("energyWarfareResistance", 0)
        else:
            neut_resist = 0

        try:
            peak_percentage = fit.capRecharge['Percent']
        except AttributeError:
            peak_percentage = 0

        panel = "Full"
        for labelName, value, prec, lowest, highest in stats:
            label = getattr(self, labelName % panel)

            if fit is None:
                value = 0
            else:
                value = value()

            if labelName == "label%sCapacitorRecharge":
                tooltip_value = "Peak recharge at: " + str(peak_percentage * 100) + "%"
            elif labelName == "label%sCapacitorDischarge":
                tooltip_value = "Capacitor delta from local and projected modules.\nNeut Resistance: {0:.0f}%".format(neut_resist)
            else:
                tooltip_value = str(value)

            if isinstance(value, basestring):
                label.SetLabel(value)
                label.SetToolTip(wx.ToolTip(tooltip_value))
            else:
                label.SetLabel(formatAmount(value, prec, lowest, highest))
                label.SetToolTip(wx.ToolTip(tooltip_value))

        capState = fit.capState if fit is not None else 0
        capStable = fit.capStable if fit is not None else 0
        lblNameTime = "label%sCapacitorTime"
        lblNameState = "label%sCapacitorState"

        if capStable:
            capStable *= 100
            s = "Stable: " + str(capStable) + "% "
            if capState:
                capState /= 1000
                if capState > 60:
                    t = "(%dm%ds)" % divmod(capState, 60)
                else:
                    t = "(%ds)" % capState
            else:
                t = ""
        else:
            s = "Unstable: " + str(capStable) + "% "

            if capState:
                capState /= 1000
                if capState > 60:
                    t = "(%dm%ds)" % divmod(capState, 60)
                else:
                    t = "(%ds)" % capState
            else:
                t = ""

        getattr(self, lblNameState % panel).SetLabel(s)
        getattr(self, lblNameTime % panel).SetLabel(t)
        time_tooltip_value = "If stable: Time until capacitor stabilizes at lowest point.\nIf unstable: Time until modules are unable to run."
        getattr(self, lblNameState % panel).SetToolTip(wx.ToolTip(time_tooltip_value))
        getattr(self, lblNameTime % panel).SetToolTip(wx.ToolTip(time_tooltip_value))

        self.panel.Layout()
        self.headerPanel.Layout()


CapacitorViewFull.register()
