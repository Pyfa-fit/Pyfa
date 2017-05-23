# Not used by any item
effectType = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Energy Neutralizer",
                                  "capacitorNeed", src.getModifiedItemAttr("structureRigEwarCapUseBonus"),
                                  stackingPenalties=True)
