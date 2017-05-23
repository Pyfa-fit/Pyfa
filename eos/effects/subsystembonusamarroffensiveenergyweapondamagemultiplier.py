# subsystemBonusAmarrOffensiveEnergyWeaponDamageMultiplier
#
# Used by:
# Subsystem: Legion Offensive - Liquid Crystal Magnifiers
effectType = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "damageMultiplier", module.getModifiedItemAttr("subsystemBonusAmarrOffensive"),
                                  skill="Amarr Offensive Systems")
