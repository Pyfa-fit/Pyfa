# kineticShieldCompensationHardeningBonusGroupShieldAmp
#
# Used by:
# Skill: Kinetic Shield Compensation
effectType = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Resistance Amplifier",
                                  "kineticDamageResistanceBonus",
                                  skill.getModifiedItemAttr("hardeningBonus") * skill.level)
