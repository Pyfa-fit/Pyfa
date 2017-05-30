# shipBonusEnergyNosFalloffRS2
#
# Used by:
# Ship: Pilgrim
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                  src.getModifiedItemAttr("eliteBonusReconShip2"), skill="Recon Ships")
