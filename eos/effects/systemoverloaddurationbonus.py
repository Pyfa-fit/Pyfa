# systemOverloadDurationBonus
#
# Used by:
# Celestials named like: Red Giant Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: "overloadDurationBonus" in mod.itemModifiedAttributes,
                                     "overloadDurationBonus", module.getModifiedItemAttr("overloadBonusMultiplier"))
