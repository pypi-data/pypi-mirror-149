"""
Monkeypatch for pycsw.core.admin module
"""

# Imports from . import * are needed to override original PyCSW behaviour
# pylint: disable=C,W,R

from shutil import which

import pycsw.core.admin
from sqlalchemy import Column, Text

from . import apiso, config, metadata

setup_db = pycsw.core.admin.setup_db


def rpi_setup_db(
    database,
    table,
    home,
    create_sfsql_tables=True,
    create_plpythonu_functions=True,
    postgis_geometry_column="wkb_geometry",
    extra_columns=[],
    language="english",
):
    """
    Patched version of pycsw.core.admin.setup_db function
    """

    extra_columns += [
        Column("rpi_organization_uuid", Text, index=True),
        Column("rpi_record_uuid", Text, index=True),
        Column("rpi_is_viewable", Text, index=True),
        Column("rpi_is_searchable", Text, index=True),
    ]

    setup_db(
        database,
        table,
        home,
        create_sfsql_tables,
        create_plpythonu_functions,
        postgis_geometry_column,
        extra_columns,
        language,
    )


pycsw.core.admin.setup_db = rpi_setup_db


def run():
    pycsw_admin_script = which("pycsw-admin.py")
    if pycsw_admin_script:
        exec(
            open(pycsw_admin_script).read().replace("pycsw-admin.py", "pycsw_rpi-admin")
        )
    else:
        raise FileExistsError("Pycsw admin script 'pycsw-admin.py' not found in $PATH")
