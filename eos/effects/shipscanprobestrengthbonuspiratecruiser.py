# shipScanProbeStrengthBonusPirateCruiser
#
# Used by:
# Ships named like: Stratios (2 of 2)
# Ship: Astero
# Ship: Gnosis
# Ship: Sunesis
effectType = "passive"


def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                    "baseSensorStrength", container.getModifiedItemAttr("shipBonusPirateFaction2"))
