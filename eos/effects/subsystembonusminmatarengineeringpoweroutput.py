# subsystemBonusMinmatarEngineeringPowerOutput
#
# Used by:
# Subsystem: Loki Engineering - Power Core Multiplier
effectType = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("powerOutput", module.getModifiedItemAttr("subsystemBonusMinmatarEngineering"),
                           skill="Minmatar Engineering Systems")
