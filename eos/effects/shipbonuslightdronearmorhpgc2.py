# shipBonusLightDroneArmorHPGC2
#
# Used by:
# Ship: Ishtar
effectType = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Light Drone Operation"),
                                 "armorHP", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")
