# shipTorpedoROFCB
#
# Used by:
# Ship: Scorpion Navy Issue
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Torpedo",
                                  "speed", ship.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")
