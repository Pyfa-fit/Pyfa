# shipBonusAF1TorpedoExplosionVelocity
#
# Used by:
# Ship: Purifier
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "aoeVelocity", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
