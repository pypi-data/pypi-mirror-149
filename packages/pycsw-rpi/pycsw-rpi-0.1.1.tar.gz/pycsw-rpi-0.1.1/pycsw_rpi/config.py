"""
Monkeypatches for pycsw.core.config module
"""


import pycsw.core.config

staticcontenxt__init__ = pycsw.core.config.StaticContext.__init__


def rpi_staticcontext__init__(self, prefix="csw30"):

    """
    Patched version of pycsw.core.config.StaticContext.__init__ function
    """

    staticcontenxt__init__(self, prefix)
    self.md_core_model["mappings"]["pycsw:RPIRecordUUID"] = "rpi_record_uuid"
    self.md_core_model["mappings"][
        "pycsw:RPIOrganizationUUID"
    ] = "rpi_organization_uuid"
    self.md_core_model["mappings"]["pycsw:RPIIsViewable"] = "rpi_is_viewable"
    self.md_core_model["mappings"]["pycsw:RPIIsSearchable"] = "rpi_is_searchable"
    self.namespaces["rpi"] = "https://rpi.gov.sk/"


pycsw.core.config.StaticContext.__init__ = rpi_staticcontext__init__
