# systemTracking
#
# Used by:
# Celestials named like: Magnetar Effect Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Gunnery"),
                                     "trackingSpeed", module.getModifiedItemAttr("trackingSpeedMultiplier"),
                                     stackingPenalties=True, penaltyGroup="postMul")
