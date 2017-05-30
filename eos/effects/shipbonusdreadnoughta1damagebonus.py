# shipBonusDreadnoughtA1DamageBonus
#
# Used by:
# Ship: Revelation
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"), "damageMultiplier",
                                  src.getModifiedItemAttr("shipBonusDreadnoughtA1"), skill="Amarr Dreadnought")
