# missileExplosiveDmgBonusHeavy
#
# Used by:
# Implants named like: Zainou 'Snapshot' Heavy Missiles HM (6 of 6)
effectType = "passive"


def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "explosiveDamage", container.getModifiedItemAttr("damageMultiplierBonus"))
