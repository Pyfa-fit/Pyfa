# shipBonusEnergyNeutOptimalRS3
#
# Used by:
# Ship: Pilgrim
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "maxRange",
                                  src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")
