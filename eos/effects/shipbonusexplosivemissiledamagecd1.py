# shipBonusExplosiveMissileDamageCD1
#
# Used by:
# Ship: Stork
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "explosiveDamage", src.getModifiedItemAttr("shipBonusCD1"),
                                    skill="Caldari Destroyer")
