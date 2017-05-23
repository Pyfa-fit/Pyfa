# subsystemBonusGallenteEngineeringCapacitorRecharge
#
# Used by:
# Subsystem: Proteus Engineering - Capacitor Regeneration Matrix
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("rechargeRate", module.getModifiedItemAttr("subsystemBonusGallenteEngineering"),
                           skill="Gallente Engineering Systems")
