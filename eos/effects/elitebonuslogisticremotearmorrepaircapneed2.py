# eliteBonusLogisticRemoteArmorRepairCapNeed2
#
# Used by:
# Ship: Guardian
# Ship: Rabisu
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                  src.getModifiedItemAttr("eliteBonusLogistics2"), skill="Logistics Cruisers")
