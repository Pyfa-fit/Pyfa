# systemSmartBombEmDamage
#
# Used by:
# Celestials named like: Red Giant Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, container, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Smart Bomb",
                                     "emDamage", container.getModifiedItemAttr("smartbombDamageMultiplier"))
