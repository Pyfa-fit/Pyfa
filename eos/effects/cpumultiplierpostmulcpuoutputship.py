# cpuMultiplierPostMulCpuOutputShip
#
# Used by:
# Modules from group: CPU Enhancer (19 of 19)
effectType = "passive"


def handler(fit, module, context):
    fit.ship.multiplyItemAttr("cpuOutput", module.getModifiedItemAttr("cpuMultiplier"))
