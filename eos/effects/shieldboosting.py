# shieldBoosting
#
# Used by:
# Modules from group: Shield Booster (93 of 93)
runTime = "late"
effectType = "active"


def handler(fit, module, context):
    amount = module.getModifiedItemAttr("shieldBonus")
    speed = module.cycleTime / 1000.0
    fit.extraAttributes.increase("shieldRepair", amount / speed)
