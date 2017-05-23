# eliteReconBonusHeavyMissileVelocity
#
# Used by:
# Ship: Rook
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("eliteBonusReconShip1"),
                                    skill="Recon Ships")
