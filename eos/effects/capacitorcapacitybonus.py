# capacitorCapacityBonus
#
# Used by:
# Modules from group: Capacitor Battery (27 of 27)
effectType = "passive"


def handler(fit, ship, context):
    fit.ship.increaseItemAttr("capacitorCapacity", ship.getModifiedItemAttr("capacitorBonus"))
