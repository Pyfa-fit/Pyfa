# eliteBonusGunshipDroneCapacity2
#
# Used by:
# Ship: Ishkur
effectType = "passive"


def handler(fit, ship, context):
    fit.ship.increaseItemAttr("droneCapacity", ship.getModifiedItemAttr("eliteBonusGunship2"), skill="Assault Frigates")
