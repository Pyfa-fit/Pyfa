# subSystemBonusCaldariElectronic2TractorBeamVelocity
#
# Used by:
# Subsystem: Tengu Electronics - Emergent Locus Analyzer
effectType = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxTractorVelocity", module.getModifiedItemAttr("subsystemBonusCaldariElectronic2"),
                                  skill="Caldari Electronic Systems")
