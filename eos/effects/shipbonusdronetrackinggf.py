# shipBonusDroneTrackingGF
#
# Used by:
# Ship: Maulus Navy Issue
# Ship: Tristan
effectType = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "trackingSpeed", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
