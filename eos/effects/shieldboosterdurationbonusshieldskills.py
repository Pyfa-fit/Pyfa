# shieldBoosterDurationBonusShieldSkills
#
# Used by:
# Modules named like: Core Defense Operational Solidifier (8 of 8)
effectType = "passive"


def handler(fit, container, context):
    fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill("Capital Shield Operation"),
            "duration", container.getModifiedItemAttr("durationSkillBonus"))
