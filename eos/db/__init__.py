# ===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================================

import threading

from sqlalchemy import MetaData

from eos.db.sqlAlchemyHandler import session_engine_factory
import migration  # noqa: F401
from eos import config
from logbook import Logger

pyfalog = Logger(__name__)
pyfalog.info("Initializing database")
pyfalog.info("Gamedata connection: {0}", config.gamedata_connectionstring)
pyfalog.info("Saveddata connection: {0}", config.saveddata_connectionstring)


class ReadOnlyException(Exception):
    pass


gamedata_factory = session_engine_factory(config.gamedata_connectionstring)
gamedata_meta = MetaData()
gamedata_engine = gamedata_meta.bind = gamedata_factory['Engine']
gamedata_session = gamedata_factory['Session']

# This should be moved elsewhere, maybe as an actual query. Current, without try-except, it breaks when making a new
# game db because we haven't reached gamedata_meta.create_all()
try:
    config.gamedata_version = gamedata_session.execute(
            "SELECT `field_value` FROM `metadata` WHERE `field_name` LIKE 'client_build'"
    ).fetchone()[0]
except Exception as e:
    pyfalog.warning("Missing gamedata version.")
    pyfalog.critical(e)
    config.gamedata_version = None

saveddata_connectionstring = config.saveddata_connectionstring
if config.saveddata_connectionstring is not None:
    saveddata_factory = session_engine_factory(config.saveddata_connectionstring)
    saveddata_meta = MetaData()
    saveddata_engine = saveddata_meta.bind = saveddata_factory['Engine']
    saveddata_session = saveddata_factory['Session']
else:
    saveddata_session = saveddata_engine = saveddata_meta = None

# Lock controlling any changes introduced to session
sd_lock = threading.RLock()

# Import all the definitions for all our database stuff
# noinspection PyPep8
from eos.db.gamedata import (  # noqa: E402,F401
    alphaClones,
    attribute,
    category,
    effect,
    group,
    icon,
    item,
    marketGroup,
    metaData,
    metaGroup,
    traits,
    unit,
)
# noinspection PyPep8
from eos.db.saveddata import (  # noqa: E402,F401
    booster,
    cargo,
    character,
    crest,
    damagePattern,
    databaseRepair,
    drone,
    fighter,
    fit,
    implant,
    implantSet,
    loadDefaultDatabaseValues,
    miscData,
    module,
    override,
    price,
    skill,
    targetResists,
    user,
)

# Import queries
# noinspection PyPep8
from eos.db.gamedata.queries import *  # noqa: F401, F402, F403
# noinspection PyPep8
from eos.db.saveddata.queries import *  # noqa: F401, F402, F403

# If using in memory saveddata, you'll want to reflect it so the data structure is good.
if config.saveddata_connectionstring == "sqlite:///:memory:":
    saveddata_meta.create_all()
    pyfalog.info("Running database out of memory.")


def rollback():
    with sd_lock:
        pyfalog.warning("Session rollback triggered.")
        saveddata_session.rollback()
