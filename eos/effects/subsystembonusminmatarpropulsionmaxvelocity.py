# subsystemBonusMinmatarPropulsionMaxVelocity
#
# Used by:
# Subsystem: Loki Propulsion - Chassis Optimization
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("subsystemBonusMinmatarPropulsion"),
                           skill="Minmatar Propulsion Systems")
