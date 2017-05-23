# roleBonusCDLinksPGReduction
#
# Used by:
# Ships from group: Command Destroyer (4 of 4)
# Ship: Porpoise
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"), "power",
                                  src.getModifiedItemAttr("roleBonusCD"))
