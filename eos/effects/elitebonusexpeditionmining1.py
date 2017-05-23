# eliteBonusExpeditionMining1
#
# Used by:
# Ship: Prospect
effectType = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                  "miningAmount", module.getModifiedItemAttr("eliteBonusExpedition1"),
                                  skill="Expedition Frigates")
