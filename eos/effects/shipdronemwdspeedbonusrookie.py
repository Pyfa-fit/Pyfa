# shipDroneMWDSpeedBonusRookie
#
# Used by:
# Ship: Taipan
effectType = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda mod: True,
                                 "maxVelocity", ship.getModifiedItemAttr("rookieDroneMWDspeed"))
