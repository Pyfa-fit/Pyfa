# shipShieldKineticResistanceCF2
#
# Used by:
# Variations of ship: Merlin (3 of 4)
# Ship: Cambion
# Ship: Whiptail
effectType = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldKineticDamageResonance", ship.getModifiedItemAttr("shipBonusCF"),
                           skill="Caldari Frigate")
