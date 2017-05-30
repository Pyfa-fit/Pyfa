# systemDroneTracking
#
# Used by:
# Celestials named like: Magnetar Effect Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, beacon, context):
    fit.drones.filteredItemMultiply(lambda drone: True,
                                    "trackingSpeed", beacon.getModifiedItemAttr("trackingSpeedMultiplier"),
                                    stackingPenalties=True, penaltyGroup="postMul")
