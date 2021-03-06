# systemArmorRemoteRepairAmount
#
# Used by:
# Celestials named like: Cataclysmic Variable Effect Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, container, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                     "armorDamageAmount",
                                     container.getModifiedItemAttr("armorDamageAmountMultiplierRemote"),
                                     stackingPenalties=True)
