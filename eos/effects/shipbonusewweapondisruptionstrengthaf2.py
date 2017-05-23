# shipBonusEwWeaponDisruptionStrengthAF2
#
# Used by:
# Variations of ship: Crucifier (3 of 3)
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "trackingSpeedBonus",
                                  src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "explosionDelayBonus",
                                  src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "maxRangeBonus",
                                  src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "falloffBonus",
                                  src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "missileVelocityBonus",
                                  src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "aoeVelocityBonus",
                                  src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "aoeCloudSizeBonus",
                                  src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
