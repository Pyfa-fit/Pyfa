# boosterModifyBoosterArmorPenalties
#
# Used by:
# Implants named like: Eifyr and Co. 'Alchemist' Neurotoxin Control NC (2 of 2)
# Implants named like: grade Edge (10 of 12)
# Skill: Neurotoxin Control
effectType = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    attrs = ("boosterArmorHPPenalty", "boosterArmorRepairAmountPenalty")
    for attr in attrs:
        fit.boosters.filteredItemBoost(lambda booster: True, attr,
                                       container.getModifiedItemAttr("boosterAttributeModifier") * level)
