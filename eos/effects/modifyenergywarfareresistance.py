# modifyEnergyWarfareResistance
#
# Used by:
# Modules from group: Capacitor Battery (27 of 27)
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("energyWarfareResistance",
                           module.getModifiedItemAttr("energyWarfareResistanceBonus"),
                           stackingPenalties=True)
