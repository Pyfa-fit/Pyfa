# skillBonusCapitalBeamLaserSpecialization
#
# Used by:
# Skill: Capital Beam Laser Specialization
effectType = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Beam Laser Specialization"),
                                  "damageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
