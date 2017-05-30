# rorqualCargoScanRangeBonus
#
# Used by:
# Ship: Rorqual
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cargo Scanner",
                                  "cargoScanRange", ship.getModifiedItemAttr("cargoScannerRangeBonus"))
