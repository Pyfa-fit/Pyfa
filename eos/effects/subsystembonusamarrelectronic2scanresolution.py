# subsystemBonusAmarrElectronic2ScanResolution
#
# Used by:
# Subsystem: Legion Electronics - Tactical Targeting Network
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("subsystemBonusAmarrElectronic2"),
                           skill="Amarr Electronic Systems")
