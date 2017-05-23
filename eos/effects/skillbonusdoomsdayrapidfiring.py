# skillBonusDoomsdayRapidFiring
#
# Used by:
# Skill: Doomsday Rapid Firing
effectType = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Doomsday Operation"), "duration",
                                  src.getModifiedItemAttr("rofBonus") * lvl)
