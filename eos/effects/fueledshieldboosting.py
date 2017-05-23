# fueledShieldBoosting
#
# Used by:
# Modules from group: Ancillary Shield Booster (5 of 5)
runTime = "late"
effectType = "active"


def handler(fit, module, context):
    amount = module.getModifiedItemAttr("shieldBonus")
    speed = module.cycleTime / 1000.0
    fit.extraAttributes.increase("shieldRepair", amount / speed)
