# shieldCapacityMultiply
#
# Used by:
# Modules from group: Capacitor Power Relay (20 of 20)
# Modules from group: Power Diagnostic System (23 of 23)
# Modules from group: Reactor Control Unit (22 of 22)
# Modules named like: Flux Coil (12 of 12)
effectType = "passive"


def handler(fit, module, context):
    fit.ship.multiplyItemAttr("shieldCapacity", module.getModifiedItemAttr("shieldCapacityMultiplier"))
