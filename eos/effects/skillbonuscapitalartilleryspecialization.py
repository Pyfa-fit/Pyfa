# skillBonusCapitalArtillerySpecialization
#
# Used by:
# Skill: Capital Artillery Specialization
effectType = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Artillery Specialization"),
                                  "damageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
