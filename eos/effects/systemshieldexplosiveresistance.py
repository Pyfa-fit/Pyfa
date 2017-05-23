# systemShieldExplosiveResistance
#
# Used by:
# Celestials named like: Wolf Rayet Effect Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, beacon, context):
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance",
                           beacon.getModifiedItemAttr("shieldExplosiveDamageResistanceBonus"),
                           stackingPenalties=True)
