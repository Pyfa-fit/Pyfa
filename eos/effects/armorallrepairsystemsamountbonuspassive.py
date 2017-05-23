# armorAllRepairSystemsAmountBonusPassive
#
# Used by:
# Implants named like: Exile Booster (4 of 4)
# Implant: Antipharmakon Kosybo
effectType = "passive"


def handler(fit, booster, context):
    fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Repair Systems") or mod.item.requiresSkill("Capital Repair Systems"),
            "armorDamageAmount", booster.getModifiedItemAttr("armorDamageAmountBonus"))
