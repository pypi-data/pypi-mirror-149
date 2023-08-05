"""
Monkeypatches for pycsw.core.metadata module
"""


from urllib.parse import parse_qs, urlparse

import pycsw.core.metadata
from owslib import util
from owslib.iso import MD_Metadata, namespaces
from pycsw.core.metadata import _set

# we need to access private protected members from pycsw.* package
# pylint: disable=W0212

_parse_iso = pycsw.core.metadata._parse_iso


def rpi_parse_iso(context, repos, exml):

    """
    Patched version of pycsw.core.metadata._parse_iso function

    Added support for parsing new queryables
    """

    # create owslib object for ISO metadata
    metadata = MD_Metadata(exml)

    # parse by original
    recobj = _parse_iso(context, repos, exml)

    # add pycsw:RPIRecordUUID to parsed object
    # /gmd:MD_Metadata/@uuid is not parsed by owslib
    # MD_Metadata() we have to do it manually -> parsing xml
    _set(
        context,
        recobj,
        "pycsw:RPIRecordUUID",
        exml.attrib.get("uuid"),
    )

    # add pycsw:RPIOrganizationUUID to parsed object
    # gmd:contact/gmd:CI_ResponsibleParty/@uuid is not parsed by owslib
    # MD_Metadata() we have to do it manually -> parsing xml
    first_contact_el = exml.find(
        util.nspath_eval("gmd:contact[1]/gmd:CI_ResponsibleParty[1]", namespaces)
    )
    _set(
        context,
        recobj,
        "pycsw:RPIOrganizationUUID",
        first_contact_el.attrib.get("uuid"),
    )

    is_viewable = any(
        [
            check_ows_url(online.url, "is_viewable")
            for online in metadata.distribution.online
        ]
    )

    is_searchable = any(
        [
            check_ows_url(online.url, "is_searchable")
            for online in metadata.distribution.online
        ]
    )

    _set(context, recobj, "pycsw:RPIIsViewable", is_viewable)
    _set(context, recobj, "pycsw:RPIIsSearchable", is_searchable)

    return recobj


# monkey patching ISO metadata parsing function in pycsw package
pycsw.core.metadata._parse_iso = rpi_parse_iso


def check_ows_url(url: str, check_type: str):

    """
    Helper function checking if url is "viewable" or "searchable"
    OWS (WMS, WFS, WMTS) request
    """

    check_types = {
        "is_ows": False,
        "is_viewable": False,
        "is_searchable": False,
    }

    if check_type not in check_types:
        raise ValueError(f"Check type {check_type} not supported")

    qparams = parse_qs(urlparse(url).query)

    # request contains all the needed ows query params
    if {"service", "version", "request"}.issubset(qparams.keys()):
        check_types["is_ows"] = True

        if qparams["service"][0].lower() in ["wms", "wmts"]:
            if qparams["request"][0].lower() in ["getmap", "gettile"]:
                check_types["is_viewable"] = True

        if qparams["service"][0].lower() in ["wfs"]:
            if qparams["request"][0].lower() == "getfeature":
                check_types["is_searchable"] = True

    return check_types[check_type]
