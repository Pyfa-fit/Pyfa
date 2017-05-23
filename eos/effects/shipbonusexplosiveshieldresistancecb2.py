# shipBonusExplosiveShieldResistanceCB2
#
# Used by:
# Ships named like: Rattlesnake (2 of 2)
# Ship: Rokh
# Ship: Scorpion Navy Issue
effectType = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonus2CB"),
                           skill="Caldari Battleship")
