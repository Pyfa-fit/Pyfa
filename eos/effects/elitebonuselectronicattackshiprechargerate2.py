# eliteBonusElectronicAttackShipRechargeRate2
#
# Used by:
# Ship: Sentinel
effectType = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("rechargeRate", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip2"),
                           skill="Electronic Attack Ships")
