# crystalMiningamountInfo2
#
# Used by:
# Modules from group: Frequency Mining Laser (3 of 3)
effectType = "passive"


def handler(fit, module, context):
    module.preAssignItemAttr("specialtyMiningAmount", module.getModifiedItemAttr("miningAmount"))
