# droneRangeBonusAdd
#
# Used by:
# Modules from group: Drone Control Range Module (7 of 7)
effectType = "passive"


def handler(fit, module, context):
    amount = module.getModifiedItemAttr("droneRangeBonus")
    fit.extraAttributes.increase("droneControlRange", amount)
