# shipShieldThermalResistance1CBC2
#
# Used by:
# Variations of ship: Drake (3 of 3)
# Ship: Vulture
effectType = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldThermalDamageResonance", ship.getModifiedItemAttr("shipBonusCBC2"),
                           skill="Caldari Battlecruiser")
