# shipMissileKineticDamageRookie
#
# Used by:
# Ship: Ibis
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", ship.getModifiedItemAttr("rookieMissileKinDamageBonus"))
