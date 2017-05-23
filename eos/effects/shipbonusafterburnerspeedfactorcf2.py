# shipBonusAfterburnerSpeedFactorCF2
#
# Used by:
# Ship: Imp
# Ship: Succubus
effectType = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                  "speedFactor", module.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")
