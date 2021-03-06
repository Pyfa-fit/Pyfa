# ===============================================================================
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
# ===============================================================================

import gui.mainFrame
from eos.gnosis import GnosisSimulation
from gui.graph import Graph


class capWarfareGraph(Graph):
    def __init__(self):
        Graph.__init__(self)
        # self.defaults["time"] = "0-300"
        self.name = "Capacitor Warfare"
        self.capWarfare = None
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def getGraphFields(self):
        # return self.defaults
        return None

    @staticmethod
    def getLabels():
        # return self.propertyLabelMap
        return None

    def getIcons(self):
        """
        icons = {}
        sAttr = service.Attribute.getInstance()
        for key, attrName in self.propertyAttributeMap.iteritems():
            iconFile = sAttr.getAttributeInfo(attrName).icon.iconFile
            bitmap = BitmapLoader.getBitmap(iconFile, "icons")
            if bitmap:
                icons[key] = bitmap

        return icons
        """
        return None

    @staticmethod
    def getPoints(fit, fields):
        capacitor_amount = fit.ship.getModifiedItemAttr("capacitorCapacity")
        capacitor_recharge = fit.ship.getModifiedItemAttr("rechargeRate")

        try:
            projected = fit.__extraDrains
        except AttributeError:
            projected = False

        try:
            if not projected:
                projected = fit._Fit__extraDrains
        except AttributeError:
            projected = False

        if not projected:
            projected = []

        return_matrix = GnosisSimulation.capacitor_simulation(fit, projected, capacitor_amount,
                                                              capacitor_recharge)

        x = []
        y = []
        for tick in return_matrix['Matrix']['Cached Runs']:
            x.append(tick['Current Time'] / 1000)  # Divide by 1000 to give seconds
            y.append(tick['Capacitor Percentage'] * 100)

        return x, y


capWarfareGraph.register()
