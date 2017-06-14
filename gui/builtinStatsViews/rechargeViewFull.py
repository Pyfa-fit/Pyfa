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
import gui.mainFrame
from gui.builtinStatsViews.resistancesViewFull import EFFECTIVE_HP_TOGGLED as EHP_TOGGLE_FULL
from gui.builtinStatsViews.resistancesViewMinimal import EFFECTIVE_HP_TOGGLED as EHP_TOGGLE_MINIMAL
from service.fit import Fit
from gui.utils.helpers_wxPython import Fonts


class RechargeViewFull(StatsView):
    name = "rechargeViewFull"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.mainFrame.Bind(EHP_TOGGLE_FULL, self.toggleEffective)
        self.mainFrame.Bind(EHP_TOGGLE_MINIMAL, self.toggleEffective)
        self.effective = True

    def getHeaderText(self, fit):
        return "Recharge rates"

    def getTextExtentW(self, text):
        width, __ = self.parent.GetTextExtent(text)
        return width

    def toggleEffective(self, event):
        self.effective = event.effective
        sFit = Fit.getInstance()
        self.refreshPanel(sFit.getFit(self.mainFrame.getActiveFit()))
        event.Skip()

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()

        self.panel = contentPanel
        self.headerPanel = headerPanel
        sizerTankStats = wx.FlexGridSizer(3, 5)
        for i in range(4):
            sizerTankStats.AddGrowableCol(i + 1)

        contentSizer.Add(sizerTankStats, 0, wx.EXPAND, 0)

        # Add an empty label first for correct alignment.
        sizerTankStats.Add(wx.StaticText(contentPanel, wx.ID_ANY, ""), 0)
        toolTipText = {
            "shieldPassive": "Passive shield recharge",
            "shieldActive" : "Active shield boost",
            "armorActive"  : "Armor repair amount",
            "hullActive"   : "Hull repair amount",
            "reinforced"   : "Reinforced: The maximum possible amount",
            "sustained"    : "Sustained: The average amount accounting for capacitor stability",
        }
        for tankType in ("shieldPassive", "shieldActive", "armorActive", "hullActive"):
            bitmap = BitmapLoader.getStaticBitmap("%s_big" % tankType, contentPanel, "gui")
            tooltip = wx.ToolTip(toolTipText[tankType])
            bitmap.SetToolTip(tooltip)
            sizerTankStats.Add(bitmap, 0, wx.ALIGN_CENTER)

        for stability in ("reinforced", "sustained"):
            bitmap = BitmapLoader.getStaticBitmap("regen%s_big" % stability.capitalize(), contentPanel, "gui")
            tooltip = wx.ToolTip(toolTipText[stability])
            bitmap.SetToolTip(tooltip)
            sizerTankStats.Add(bitmap, 0, wx.ALIGN_CENTER)
            for tankType in ("shieldPassive", "shieldActive", "armorActive", "hullActive"):
                if stability == "sustained" and tankType == "shieldPassive":
                    sizerTankStats.Add(wx.StaticText(contentPanel, wx.ID_ANY, ""))
                    continue

                tankTypeCap = tankType[0].capitalize() + tankType[1:]
                lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0.0", style=wx.ALIGN_RIGHT)
                setattr(self, "labelTank%s%s" % (stability.capitalize(), tankTypeCap), lbl)
                tooltip = wx.ToolTip(toolTipText[tankType])
                lbl.SetToolTip(tooltip)

                box = wx.BoxSizer(wx.HORIZONTAL)
                box.Add(lbl, 0, wx.EXPAND)

                unitlbl = wx.StaticText(contentPanel, wx.ID_ANY, " EHP/s")
                setattr(self, "unitLabelTank%s%s" % (stability.capitalize(), tankTypeCap), unitlbl)
                box.Add(unitlbl, 0, wx.EXPAND)

                sizerTankStats.Add(box, 0, wx.ALIGN_CENTRE)

        contentPanel.Layout()

    def refreshPanel(self, fit):
        # If we did anything interesting, we'd update our labels to reflect the new fit's stats here

        try:
            unit = " EHP/s" if self.parent.nameViewMap['resistancesViewFull'].showEffective else " HP/s"
        except:
            unit = " EHP/s" if self.parent.nameViewMap['resistancesViewMinimal'].showEffective else " HP/s"

        for stability in ("reinforced", "sustained"):
            if stability == "reinforced" and fit is not None:
                tank = fit.effectiveTank if self.effective else fit.tank
            elif stability == "sustained" and fit is not None:
                tank = fit.effectiveSustainableTank if self.effective else fit.sustainableTank
            else:
                tank = None

            for name in ("shield", "armor", "hull"):
                lbl = getattr(self, "labelTank%s%sActive" % (stability.capitalize(), name.capitalize()))
                unitlbl = getattr(self, "unitLabelTank%s%sActive" % (stability.capitalize(), name.capitalize()))
                unitlbl.SetLabel(unit)
                if tank is not None:
                    # Too large of a font will cause issuses with size and fit, so don't display extra info
                    if 10 < getattr(Fonts.getFont("font_standard"), "PointSize", 9):
                        lbl.SetLabel("%i" % tank["%sRepair" % name])
                    else:
                        lbl.SetLabel("%.1f" % tank["%sRepair" % name])
                else:
                    lbl.SetLabel("0")

        if fit is not None:
            label = getattr(self, "labelTankReinforcedShieldPassive")
            value = fit.effectiveTank["passiveShield"] if self.effective else fit.tank["passiveShield"]

            # Too large of a font will cause issuses with size and fit, so don't display extra info
            if 10 < getattr(Fonts.getFont("font_standard"), "PointSize", 9):
                label.SetLabel(formatAmount(value, 1, 0, 9))
            else:
                label.SetLabel(formatAmount(value, 3, 0, 9))

            unitlbl = getattr(self, "unitLabelTankReinforcedShieldPassive")
            unitlbl.SetLabel(unit)

        else:
            value = 0
            label = getattr(self, "labelTankReinforcedShieldPassive")
            label.SetLabel("0")

        self.panel.Layout()
        self.headerPanel.Layout()


RechargeViewFull.register()
