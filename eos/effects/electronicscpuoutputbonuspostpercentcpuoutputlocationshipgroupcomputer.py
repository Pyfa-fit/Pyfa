# electronicsCpuOutputBonusPostPercentCpuOutputLocationShipGroupComputer
#
# Used by:
# Implants named like: Zainou 'Gypsy' CPU Management EE (6 of 6)
# Modules named like: Processor Overclocking Unit (8 of 8)
# Implant: Genolution Core Augmentation CA-2
# Skill: CPU Management
effectType = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("cpuOutput", container.getModifiedItemAttr("cpuOutputBonus2") * level)
