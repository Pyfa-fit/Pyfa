# subSystemBonusGallenteDefensiveInformationWarfare
#
# Used by:
# Subsystem: Proteus Defensive - Warfare Processor
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff4Value",
                                  src.getModifiedItemAttr("subsystemBonusGallenteDefensive"),
                                  skill="Gallente Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff2Value",
                                  src.getModifiedItemAttr("subsystemBonusGallenteDefensive"),
                                  skill="Gallente Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff3Value",
                                  src.getModifiedItemAttr("subsystemBonusGallenteDefensive"),
                                  skill="Gallente Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "buffDuration",
                                  src.getModifiedItemAttr("subsystemBonusGallenteDefensive"),
                                  skill="Gallente Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff1Value",
                                  src.getModifiedItemAttr("subsystemBonusGallenteDefensive"),
                                  skill="Gallente Defensive Systems")
