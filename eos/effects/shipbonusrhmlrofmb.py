# shipBonusRHMLROFMB
#
# Used by:
# Ship: Typhoon
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Heavy",
                                  "speed", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")
