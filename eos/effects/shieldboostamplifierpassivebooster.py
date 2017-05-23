# shieldBoostAmplifierPassiveBooster
#
# Used by:
# Implants named like: Blue Pill Booster (5 of 5)
# Implant: Antipharmakon Thureo
effectType = "passive"


def handler(fit, container, context):
    fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill("Capital Shield Operation"),
            "shieldBonus", container.getModifiedItemAttr("shieldBoostMultiplier"))
