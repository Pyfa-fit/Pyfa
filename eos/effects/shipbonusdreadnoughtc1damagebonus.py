# shipBonusDreadnoughtC1DamageBonus
#
# Used by:
# Ship: Phoenix
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "thermalDamage",
                                    src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "kineticDamage",
                                    src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "emDamage",
                                    src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "explosiveDamage",
                                    src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "explosiveDamage",
                                    src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "thermalDamage",
                                    src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "thermalDamage",
                                    src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "emDamage",
                                    src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "kineticDamage",
                                    src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "kineticDamage",
                                    src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"), "explosiveDamage",
                                    src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"), "emDamage",
                                    src.getModifiedItemAttr("shipBonusDreadnoughtC1"), skill="Caldari Dreadnought")
