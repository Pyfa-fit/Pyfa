# shipBonusTitanA3WarpStrength
#
# Used by:
# Ship: Avatar
# Ship: Molok
effectType = "passive"


def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("shipBonusTitanA3"), skill="Amarr Titan")
