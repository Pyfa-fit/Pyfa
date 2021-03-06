# shipBonusForceAuxiliaryM4WarfareLinksBonus
#
# Used by:
# Ship: Lif
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff3Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryM4"), skill="Minmatar Carrier")
    fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff2Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryM4"), skill="Minmatar Carrier")
    fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff1Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryM4"), skill="Minmatar Carrier")
    fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "buffDuration", src.getModifiedItemAttr("shipBonusForceAuxiliaryM4"), skill="Minmatar Carrier")
    fit.modules.filteredItemBoost(
            lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
            "warfareBuff4Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryM4"), skill="Minmatar Carrier")
