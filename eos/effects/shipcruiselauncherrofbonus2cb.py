# shipCruiseLauncherROFBonus2CB
#
# Used by:
# Ship: Raven
# Ship: Raven State Issue
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Cruise",
                                  "speed", ship.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")
