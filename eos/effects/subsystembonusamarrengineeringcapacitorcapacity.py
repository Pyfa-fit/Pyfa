# subsystemBonusAmarrEngineeringCapacitorCapacity
#
# Used by:
# Subsystem: Legion Engineering - Augmented Capacitor Reservoir
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("capacitorCapacity", module.getModifiedItemAttr("subsystemBonusAmarrEngineering"),
                           skill="Amarr Engineering Systems")
