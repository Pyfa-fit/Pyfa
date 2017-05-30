# systemDamageFighters
#
# Used by:
# Celestials named like: Magnetar Effect Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, beacon, context):
    fit.drones.filteredItemMultiply(lambda drone: drone.item.requiresSkill("Fighters"),
                                    "damageMultiplier", beacon.getModifiedItemAttr("damageMultiplierMultiplier"),
                                    stackingPenalties=True, penaltyGroup="postMul")
