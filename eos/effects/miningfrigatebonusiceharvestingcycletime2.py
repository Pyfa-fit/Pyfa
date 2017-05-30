# miningFrigateBonusIceHarvestingCycleTime2
#
# Used by:
# Ship: Endurance
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"), "duration",
                                  src.getModifiedItemAttr("shipBonusOREfrig2"), skill="Mining Frigate")
