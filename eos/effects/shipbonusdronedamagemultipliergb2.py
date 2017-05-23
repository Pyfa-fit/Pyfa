# shipBonusDroneDamageMultiplierGB2
#
# Used by:
# Variations of ship: Dominix (3 of 3)
# Ship: Nestor
effectType = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusGB2"),
                                 skill="Gallente Battleship")
