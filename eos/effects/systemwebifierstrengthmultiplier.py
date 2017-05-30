# systemWebifierStrengthMultiplier
#
# Used by:
# Celestials named like: Black Hole Effect Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, beacon, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Stasis Web",
                                     "speedFactor", beacon.getModifiedItemAttr("stasisWebStrengthMultiplier"),
                                     stackingPenalties=True, penaltyGroup="postMul")
