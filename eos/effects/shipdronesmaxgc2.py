# shipDronesMaxGC2
#
# Used by:
# Ship: Guardian-Vexor
effectType = "passive"


def handler(fit, ship, context):
    fit.extraAttributes.increase("maxActiveDrones", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")
