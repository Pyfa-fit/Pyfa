# subsystemBonusMinmatarEngineeringCapacitorCapacity
#
# Used by:
# Subsystem: Loki Engineering - Augmented Capacitor Reservoir
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("capacitorCapacity", module.getModifiedItemAttr("subsystemBonusMinmatarEngineering"),
                           skill="Minmatar Engineering Systems")
