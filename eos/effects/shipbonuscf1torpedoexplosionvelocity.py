# shipBonusCF1TorpedoExplosionVelocity
#
# Used by:
# Ship: Manticore
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "aoeVelocity", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")
