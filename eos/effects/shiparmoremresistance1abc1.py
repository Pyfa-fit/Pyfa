# shipArmorEMResistance1ABC1
#
# Used by:
# Variations of ship: Prophecy (2 of 2)
# Ship: Absolution
effectType = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("armorEmDamageResonance", ship.getModifiedItemAttr("shipBonusABC1"),
                           skill="Amarr Battlecruiser")
