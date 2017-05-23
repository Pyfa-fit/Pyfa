# subsystemBonusCaldariOffensiveHeavyAssaultMissileLauncherROF
#
# Used by:
# Variations of subsystem: Tengu Offensive - Accelerated Ejection Bay (3 of 4)
effectType = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy Assault",
                                  "speed", module.getModifiedItemAttr("subsystemBonusCaldariOffensive"),
                                  skill="Caldari Offensive Systems")
