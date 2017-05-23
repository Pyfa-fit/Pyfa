# iceMinerCpuUsagePercent
#
# Used by:
# Variations of module: Ice Harvester Upgrade I (5 of 5)
effectType = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"),
                                  "cpu", module.getModifiedItemAttr("cpuPenaltyPercent"))
