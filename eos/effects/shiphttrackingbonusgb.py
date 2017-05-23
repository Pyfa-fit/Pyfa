# shipHTTrackingBonusGB
#
# Used by:
# Ship: Vindicator
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusGB"), skill="Gallente Battleship")
