# boosterMissileVelocityPenalty
#
# Used by:
# Implants named like: Crash Booster (3 of 4)
# Implants named like: X Instinct Booster (3 of 4)
effectType = "boosterSideEffect"
activeByDefault = False


def handler(fit, booster, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "maxVelocity", "boosterMissileVelocityPenalty")
