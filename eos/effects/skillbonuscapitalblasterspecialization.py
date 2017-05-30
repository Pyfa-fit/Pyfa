# skillBonusCapitalBlasterSpecialization
#
# Used by:
# Skill: Capital Blaster Specialization
effectType = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Blaster Specialization"),
                                  "damageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
