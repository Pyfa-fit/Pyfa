# shipBonusAgilityGI2
#
# Used by:
# Ship: Nereus
effectType = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("shipBonusGI2"), skill="Gallente Industrial")
