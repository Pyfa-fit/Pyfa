# shipMiningBonusOREfrig1
#
# Used by:
# Variations of ship: Venture (3 of 3)
effectType = "passive"


def handler(fit, container, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                  "miningAmount", container.getModifiedItemAttr("shipBonusOREfrig1"),
                                  skill="Mining Frigate")
