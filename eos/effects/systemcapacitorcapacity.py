# systemCapacitorCapacity
#
# Used by:
# Celestials named like: Cataclysmic Variable Effect Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, beacon, context):
    fit.ship.multiplyItemAttr("capacitorCapacity", beacon.getModifiedItemAttr("capacitorCapacityMultiplierSystem"))
