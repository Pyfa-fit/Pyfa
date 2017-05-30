# boosterMissileExplosionCloudPenaltyFixed
#
# Used by:
# Implants named like: Exile Booster (3 of 4)
# Implants named like: Mindflood Booster (3 of 4)
effectType = "boosterSideEffect"
activeByDefault = False


def handler(fit, booster, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "aoeCloudSize", booster.getModifiedItemAttr("boosterMissileAOECloudPenalty"))
