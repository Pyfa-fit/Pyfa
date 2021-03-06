# subsystemBonusMinmatarDefensive2RemoteShieldTransporterAmount
#
# Used by:
# Subsystem: Loki Defensive - Adaptive Shielding
effectType = "passive"
runTime = "early"


def handler(fit, container, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "shieldBonus", container.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"),
                                  skill="Minmatar Defensive Systems")
