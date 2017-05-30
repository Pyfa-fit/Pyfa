# systemTargetingRange
#
# Used by:
# Celestials named like: Black Hole Effect Beacon Class (6 of 6)
# Celestials named like: Magnetar Effect Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, beacon, context):
    fit.ship.multiplyItemAttr("maxTargetRange", beacon.getModifiedItemAttr("maxTargetRangeMultiplier"),
                              stackingPenalties=True, penaltyGroup="postMul")
