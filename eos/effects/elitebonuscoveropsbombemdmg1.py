# eliteBonusCoverOpsBombEmDmg1
#
# Used by:
# Ship: Purifier
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Bomb Deployment"),
                                    "emDamage", ship.getModifiedItemAttr("eliteBonusCoverOps1"), skill="Covert Ops")
