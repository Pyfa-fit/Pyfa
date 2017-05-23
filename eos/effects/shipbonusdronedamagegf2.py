# shipBonusDroneDamageGF2
#
# Used by:
# Ship: Utu
effectType = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")
