# moduleBonusCapitalDroneScopeChip
#
# Used by:
# Variations of module: Capital Drone Scope Chip I (2 of 2)
effectType = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxRange",
                                 src.getModifiedItemAttr("rangeSkillBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesRange",
                                   src.getModifiedItemAttr("rangeSkillBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                   "fighterAbilityAttackTurretRangeOptimal", src.getModifiedItemAttr("rangeSkillBonus"),
                                   stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                   "fighterAbilityAttackMissileRangeOptimal",
                                   src.getModifiedItemAttr("rangeSkillBonus"), stackingPenalties=True)
    fit.ship.boostItemAttr("cpuOutput", src.getModifiedItemAttr("drawback"))
