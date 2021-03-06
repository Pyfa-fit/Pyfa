# shipModuleGuidanceDisruptor
#
# Used by:
# Variations of module: Guidance Disruptor I (6 of 6)
effectType = "active", "projected"


def handler(fit, container, context, *args, **kwargs):
    if "projected" in context:
        for srcAttr, tgtAttr in (
                ("aoeCloudSizeBonus", "aoeCloudSize"),
                ("aoeVelocityBonus", "aoeVelocity"),
                ("missileVelocityBonus", "maxVelocity"),
                ("explosionDelayBonus", "explosionDelay"),
        ):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                            tgtAttr, container.getModifiedItemAttr(srcAttr),
                                            stackingPenalties=True, *args, **kwargs)
