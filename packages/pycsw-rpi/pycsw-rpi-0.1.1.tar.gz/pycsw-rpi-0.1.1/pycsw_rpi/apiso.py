"""
Monkeypatches for pycsw.core.apiso.apiso module
"""


import pycsw.plugins.profiles.apiso.apiso

apiso__init__ = pycsw.plugins.profiles.apiso.apiso.APISO.__init__


def rpi_apiso__init__(self, model, namespaces, context):
    """
    Patched version of pycsw.plugins.profiles.apiso.apiso.APISO.__init__ function
    """

    apiso__init__(self, model, namespaces, context)
    self.repository["queryables"]["RPIQueryables"] = {
        "rpi:OrganizationUUID": {
            # "xpath": "//",
            "dbcol": self.context.md_core_model["mappings"][
                "pycsw:RPIOrganizationUUID"
            ],
        },
        "rpi:RecordUUID": {
            # "xpath": "//",
            "dbcol": self.context.md_core_model["mappings"]["pycsw:RPIRecordUUID"],
        },
        "rpi:IsViewable": {
            # "xpath": "//",
            "dbcol": self.context.md_core_model["mappings"]["pycsw:RPIIsViewable"],
        },
        "rpi:IsSearchable": {
            # "xpath": "//",
            "dbcol": self.context.md_core_model["mappings"]["pycsw:RPIIsSearchable"],
        },
    }


pycsw.plugins.profiles.apiso.apiso.APISO.__init__ = rpi_apiso__init__
