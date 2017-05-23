# shipVelocityBonusATC1
#
# Used by:
# Ship: Adrestia
# Ship: Mimir
effectType = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusATC1"))
