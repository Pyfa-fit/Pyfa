# freighterMaxVelocityBonusM1
#
# Used by:
# Ship: Fenrir
effectType = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("freighterBonusM1"), skill="Minmatar Freighter")
