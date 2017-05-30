# shipBonusEliteCover2TorpedoThermalDamage
#
# Used by:
# Ship: Nemesis
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "thermalDamage", ship.getModifiedItemAttr("eliteBonusCoverOps2"),
                                    skill="Covert Ops")
