# subsystemBonusMinmatarElectronic2ScanResolution
#
# Used by:
# Subsystem: Loki Electronics - Tactical Targeting Network
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("subsystemBonusMinmatarElectronic2"),
                           skill="Minmatar Electronic Systems")
