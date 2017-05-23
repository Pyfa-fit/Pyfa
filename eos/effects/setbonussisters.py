# setBonusSisters
#
# Used by:
# Implants named like: grade Virtue (12 of 12)
runTime = "early"
effectType = "passive"


def handler(fit, implant, context):
    fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                             "scanStrengthBonus", implant.getModifiedItemAttr("implantSetSisters"))
