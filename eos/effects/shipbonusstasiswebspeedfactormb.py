# shipBonusStasisWebSpeedFactorMB
#
# Used by:
# Ship: Vindicator
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "speedFactor", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")
