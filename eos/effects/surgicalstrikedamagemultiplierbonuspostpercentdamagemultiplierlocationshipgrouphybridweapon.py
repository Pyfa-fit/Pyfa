# surgicalStrikeDamageMultiplierBonusPostPercentDamageMultiplierLocationShipGroupHybridWeapon
#
# Used by:
# Skill: Surgical Strike
effectType = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                  "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
