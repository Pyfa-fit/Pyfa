# remoteCapacitorTransmitterPowerNeedBonusEffect
#
# Used by:
# Ships from group: Logistics (3 of 6)
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                  "power", ship.getModifiedItemAttr("powerTransferPowerNeedBonus"))
