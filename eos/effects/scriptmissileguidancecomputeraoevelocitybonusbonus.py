# scriptMissileGuidanceComputerAOEVelocityBonusBonus
#
# Used by:
# Charges from group: Tracking Script (2 of 2)
# Charges named like: Missile Script (4 of 4)
effectType = "passive"


def handler(fit, container, context):
    container.boostItemAttr("aoeVelocityBonus", container.getModifiedChargeAttr("aoeVelocityBonusBonus"))
