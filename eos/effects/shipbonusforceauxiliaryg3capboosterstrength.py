# shipBonusForceAuxiliaryG3CapBoosterStrength
#
# Used by:
# Ship: Ninazu
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Capacitor Booster Charge", "capacitorBonus",
                                    src.getModifiedItemAttr("shipBonusForceAuxiliaryG3"), skill="Gallente Carrier")
