# eliteBonusCoverOpsBombKineticDmg1
#
# Used by:
# Ship: Manticore
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                    "kineticDamage", ship.getModifiedItemAttr("eliteBonusCoverOps1"),
                                    skill="Covert Ops")
