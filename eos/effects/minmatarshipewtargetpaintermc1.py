# minmatarShipEwTargetPainterMC1
#
# Used by:
# Ship: Bellicose
# Ship: Rapier
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("shipBonusMC"),
                                  skill="Minmatar Cruiser")
