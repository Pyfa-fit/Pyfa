# subsystemBonusCaldariPropulsion2WarpCapacitor2
#
# Used by:
# Subsystem: Tengu Propulsion - Gravitational Capacitor
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("warpCapacitorNeed", module.getModifiedItemAttr("subsystemBonusCaldariPropulsion2"),
                           skill="Caldari Propulsion Systems")
