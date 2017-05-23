# shipModeSETOptimalRangePostDiv
#
# Used by:
# Module: Confessor Sharpshooter Mode
effectType = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(
            lambda mod: mod.item.requiresSkill("Small Energy Turret"),
            "maxRange",
            1 / module.getModifiedItemAttr("modeMaxRangePostDiv"),
            stackingPenalties=True,
            penaltyGroup="postDiv"
    )
