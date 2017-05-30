# armoredCommandDurationBonus
#
# Used by:
# Skill: Armored Command
effectType = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "buffDuration",
                                  src.getModifiedItemAttr("durationBonus") * lvl)
