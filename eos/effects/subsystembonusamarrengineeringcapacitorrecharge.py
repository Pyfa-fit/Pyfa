# subsystemBonusAmarrEngineeringCapacitorRecharge
#
# Used by:
# Subsystem: Legion Engineering - Capacitor Regeneration Matrix
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("rechargeRate", module.getModifiedItemAttr("subsystemBonusAmarrEngineering"),
                           skill="Amarr Engineering Systems")
