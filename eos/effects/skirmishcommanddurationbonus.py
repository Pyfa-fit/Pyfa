# skirmishCommandDurationBonus
#
# Used by:
# Skill: Skirmish Command
effectType = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "buffDuration",
                                  src.getModifiedItemAttr("durationBonus") * lvl)
