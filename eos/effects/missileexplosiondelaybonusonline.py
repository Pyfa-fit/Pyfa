# missileExplosionDelayBonusOnline
#
# Used by:
# Modules from group: Missile Guidance Enhancer (3 of 3)
effectType = "passive"


def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "explosionDelay", container.getModifiedItemAttr("explosionDelayBonus"),
                                    stackingPenalties=True)
