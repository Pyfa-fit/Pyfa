# weaponUpgradesCpuNeedBonusPostPercentCpuLocationShipModulesRequiringEnergyPulseWeapons
#
# Used by:
# Skill: Weapon Upgrades
effectType = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Energy Pulse Weapons"),
                                  "cpu", skill.getModifiedItemAttr("cpuNeedBonus") * skill.level)
