# shipBonusSupercarrierA4BurstProjectorBonus
#
# Used by:
# Ship: Aeon
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation"),
                                  "durationWeaponDisruptionBurstProjector",
                                  src.getModifiedItemAttr("shipBonusSupercarrierA4"), skill="Amarr Carrier")
