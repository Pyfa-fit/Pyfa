# shipBonusVelocityGI
#
# Used by:
# Variations of ship: Epithal (2 of 2)
# Variations of ship: Miasmos (4 of 4)
# Ship: Iteron Mark V
# Ship: Kryos
# Ship: Viator
effectType = "passive"


def handler(fit, ship, context):
    # TODO: investigate if we can live without such ifs or hardcoding
    # Viator doesn't have GI bonus
    if "shipBonusGI" in fit.ship.item.attributes:
        bonusAttr = "shipBonusGI"
    else:
        bonusAttr = "shipBonusGI2"
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr(bonusAttr), skill="Gallente Industrial")
