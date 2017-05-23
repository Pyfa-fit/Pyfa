# shipBonusGFTorpedoExplosionVelocity
#
# Used by:
# Ship: Nemesis
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "aoeVelocity", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
