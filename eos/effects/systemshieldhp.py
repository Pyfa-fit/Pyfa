# systemShieldHP
#
# Used by:
# Celestials named like: Pulsar Effect Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, beacon, context):
    fit.ship.multiplyItemAttr("shieldCapacity", beacon.getModifiedItemAttr("shieldCapacityMultiplier"))
