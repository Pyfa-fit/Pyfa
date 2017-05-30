# systemMagnetrometricECMBomb
#
# Used by:
# Celestials named like: Red Giant Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, beacon, context):
    fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                       "scanMagnetometricStrengthBonus",
                                       beacon.getModifiedItemAttr("smartbombDamageMultiplier"),
                                       stackingPenalties=True, penaltyGroup="postMul")
