# overloadSelfMissileGuidanceBonus5
#
# Used by:
# Modules from group: Missile Guidance Computer (3 of 3)
effectType = "overheat"


def handler(fit, module, context):
    for tgtAttr in (
            "aoeCloudSizeBonus",
            "explosionDelayBonus",
            "missileVelocityBonus",
            "maxVelocityModifier",
            "aoeVelocityBonus"
    ):
        module.boostItemAttr(tgtAttr, module.getModifiedItemAttr("overloadTrackingModuleStrengthBonus"))
