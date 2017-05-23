# shipBonusEnergyNosFalloffRS3
#
# Used by:
# Ship: Curse
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                  src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")
