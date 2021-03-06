# kineticArmorCompensationHardeningBonusGroupEnergized
#
# Used by:
# Skill: Kinetic Armor Compensation
effectType = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Plating Energized",
                                  "kineticDamageResistanceBonus",
                                  skill.getModifiedItemAttr("hardeningBonus") * skill.level)
