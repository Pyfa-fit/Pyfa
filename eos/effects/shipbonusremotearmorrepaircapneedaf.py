# shipBonusRemoteArmorRepairCapNeedAF
#
# Used by:
# Ship: Deacon
# Ship: Inquisitor
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                  src.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
