# scriptMissileGuidanceComputerExplosionDelayBonusBonus
#
# Used by:
# Charges named like: Missile Script (4 of 4)
effectType = "passive"


def handler(fit, container, context):
    container.boostItemAttr("explosionDelayBonus", container.getModifiedChargeAttr("explosionDelayBonusBonus"))
