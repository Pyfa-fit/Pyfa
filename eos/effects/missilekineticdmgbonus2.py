# missileKineticDmgBonus2
#
# Used by:
# Skills named like: Missiles (5 of 7)
# Skill: Rockets
# Skill: Torpedoes
effectType = "passive"


def handler(fit, skill, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill(skill),
                                    "kineticDamage", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
