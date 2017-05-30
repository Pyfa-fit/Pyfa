# ewGroupTpMaxRangeBonus
#
# Used by:
# Implants named like: grade Centurion (10 of 12)
effectType = "passive"


def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                  "maxRange", implant.getModifiedItemAttr("rangeSkillBonus"))
