# Not used by any item
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"), "signatureRadiusBonus",
                                  src.getModifiedItemAttr("eliteBonusCommandDestroyer3"), skill="Command Destroyers")
