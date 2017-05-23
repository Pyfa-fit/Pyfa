# powerBooster
#
# Used by:
# Modules from group: Capacitor Booster (59 of 59)
effectType = "active"


def handler(fit, module, context):
    # Set reload time to 10 seconds
    module.reloadTime = 10000

    if module.charge is None:
        return
    capAmount = module.getModifiedChargeAttr("capacitorBonus") or 0
    module.itemModifiedAttributes["capacitorNeed"] = -capAmount
