# capitalShieldOperationSkillCapacitorNeedBonus
#
# Used by:
# Modules named like: Core Defense Capacitor Safeguard (8 of 8)
# Skill: Capital Shield Operation
effectType = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"),
                                  "capacitorNeed", container.getModifiedItemAttr("shieldBoostCapacitorBonus") * level)
