# overloadSelfSpeedBonus
#
# Used by:
# Modules from group: Propulsion Module (127 of 127)
effectType = "overheat"


def handler(fit, module, context):
    module.boostItemAttr("speedFactor", module.getModifiedItemAttr("overloadSpeedFactorBonus"),
                         stackingPenalties=True)
