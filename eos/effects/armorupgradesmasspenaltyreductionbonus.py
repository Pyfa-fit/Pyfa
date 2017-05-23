# armorUpgradesMassPenaltyReductionBonus
#
# Used by:
# Skill: Armor Layering
effectType = "passive"


def handler(fit, container, context):
    level = container.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Reinforcer",
                                  "massAddition", container.getModifiedItemAttr("massPenaltyReduction") * level)
