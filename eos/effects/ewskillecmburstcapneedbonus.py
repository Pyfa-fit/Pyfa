# ewSkillEcmBurstCapNeedBonus
#
# Used by:
# Implants named like: Zainou 'Gypsy' Electronic Warfare EW (6 of 6)
# Modules named like: Signal Disruption Amplifier (8 of 8)
# Skill: Electronic Warfare
effectType = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Burst Jammer",
                                  "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)
