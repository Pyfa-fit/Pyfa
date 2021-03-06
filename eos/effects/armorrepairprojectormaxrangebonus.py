# armorRepairProjectorMaxRangeBonus
#
# Used by:
# Variations of ship: Navitas (2 of 2)
# Ship: Augoror
# Ship: Deacon
# Ship: Exequror
# Ship: Inquisitor
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer", "maxRange",
                                  src.getModifiedItemAttr("maxRangeBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Ancillary Remote Armor Repairer", "maxRange",
                                  src.getModifiedItemAttr("maxRangeBonus"))
