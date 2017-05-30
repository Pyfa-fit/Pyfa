# shipBonusSentryArmorHPGC3
#
# Used by:
# Ship: Ishtar
effectType = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                 "armorHP", ship.getModifiedItemAttr("shipBonusGC3"), skill="Gallente Cruiser")
