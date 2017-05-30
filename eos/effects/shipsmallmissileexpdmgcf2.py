# shipSmallMissileExpDmgCF2
#
# Used by:
# Ship: Caldari Navy Hookbill
# Ship: Kestrel
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(
            lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
            "explosiveDamage", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")
