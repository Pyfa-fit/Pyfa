# systemTracking
#
# Used by:
# Celestials named like: Magnetar Effect Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, container, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Gunnery"),
                                     "trackingSpeed", container.getModifiedItemAttr("trackingSpeedMultiplier"),
                                     stackingPenalties=True, penaltyGroup="postMul")
