# ewSkillTrackingDisruptionTrackingSpeedBonus
#
# Used by:
# Modules named like: Tracking Diagnostic Subroutines (8 of 8)
# Skill: Weapon Destabilization
effectType = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Weapon Disruptor",
                                  "trackingSpeedBonus",
                                  container.getModifiedItemAttr("scanSkillEwStrengthBonus") * level)
