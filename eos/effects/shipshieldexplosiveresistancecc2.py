# shipShieldExplosiveResistanceCC2
#
# Used by:
# Variations of ship: Moa (3 of 4)
effectType = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusCC2"),
                           skill="Caldari Cruiser")
