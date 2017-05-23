# shipBonusScanProbeStrengthCF
#
# Used by:
# Ship: Heron
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                    "baseSensorStrength", ship.getModifiedItemAttr("shipBonusCF2"),
                                    skill="Caldari Frigate")
