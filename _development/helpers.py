# noinspection PyPackageRequirements
import pytest

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
# Add root folder to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, u'..', u'..')))
sys._called_from_test = True


# noinspection PyUnresolvedReferences,PyUnusedLocal
@pytest.fixture
def DBInMemory():
    print("Creating database in memory")

    import eos.config

    import eos
    import eos.db

    # Output debug info to help us troubleshoot Travis
    print(eos.db.saveddata_engine)
    print(eos.db.gamedata_engine)

    helper = {
        'config'           : eos.config,
        'db'               : eos.db,
        'gamedata_session' : eos.db.gamedata_session,
        'saveddata_session': eos.db.saveddata_session,
    }
    return helper


@pytest.fixture
def Gamedata():
    print("Building Gamedata")
    from eos.gamedata import Item

    helper = {
        'Item': Item,
    }
    return helper


@pytest.fixture
def Saveddata():
    print("Building Saveddata")
    from eos.saveddata.ship import Ship
    from eos.saveddata.fit import Fit
    from eos.saveddata.character import Character
    from eos.saveddata.module import Module, State
    from eos.saveddata.citadel import Citadel
    from eos.saveddata.booster import Booster

    helper = {
        'Structure': Citadel,
        'Ship'     : Ship,
        'Fit'      : Fit,
        'Character': Character,
        'Module'   : Module,
        'State'    : State,
        'Booster'  : Booster,
    }
    return helper
