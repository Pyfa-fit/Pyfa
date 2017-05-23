# missileExplosiveDmgBonusHAM
#
# Used by:
# Implants named like: Zainou 'Snapshot' Heavy Assault Missiles AM (6 of 6)
effectType = "passive"


def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "explosiveDamage", container.getModifiedItemAttr("damageMultiplierBonus"))
