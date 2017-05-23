# shipShieldEMResistanceRookie
#
# Used by:
# Ships from group: Heavy Interdiction Cruiser (3 of 5)
# Ship: Ibis
# Ship: Taipan
effectType = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldEmDamageResonance", ship.getModifiedItemAttr("rookieShieldResistBonus"))
