# subsystemBonusCaldariPropulsionAfterburnerSpeedFactor
#
# Used by:
# Subsystem: Tengu Propulsion - Fuel Catalyst
effectType = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                  "speedFactor", module.getModifiedItemAttr("subsystemBonusCaldariPropulsion"),
                                  skill="Caldari Propulsion Systems")
