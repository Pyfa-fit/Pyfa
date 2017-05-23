# shieldTransporterFalloffBonus
#
# Used by:
# Variations of ship: Bantam (2 of 2)
# Variations of ship: Burst (2 of 2)
# Ship: Osprey
# Ship: Scythe
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Shield Booster", "falloffEffectiveness",
                                  src.getModifiedItemAttr("falloffBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Ancillary Remote Shield Booster",
                                  "falloffEffectiveness", src.getModifiedItemAttr("falloffBonus"))
