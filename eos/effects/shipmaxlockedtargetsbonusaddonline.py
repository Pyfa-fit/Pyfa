# shipMaxLockedTargetsBonusAddOnline
#
# Used by:
# Modules from group: Signal Amplifier (7 of 7)
effectType = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("maxLockedTargets", module.getModifiedItemAttr("maxLockedTargetsBonus"))
