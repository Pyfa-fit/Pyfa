# subsystemBonusMinmatarPropulsionAfterburnerSpeedFactor
#
# Used by:
# Subsystem: Loki Propulsion - Fuel Catalyst
effectType = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                  "speedFactor", module.getModifiedItemAttr("subsystemBonusMinmatarPropulsion"),
                                  skill="Minmatar Propulsion Systems")
