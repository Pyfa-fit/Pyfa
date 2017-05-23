# gasHarvesterMaxRangeBonus
#
# Used by:
# Implants named like: grade Harvest (10 of 12)
effectType = "passive"


def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Gas Cloud Harvester",
                                  "maxRange", implant.getModifiedItemAttr("maxRangeBonus"))
