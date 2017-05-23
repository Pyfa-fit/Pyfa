# shipBonusRemoteArmorRepairCapNeedGC1
#
# Used by:
# Ship: Exequror
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                  src.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")
