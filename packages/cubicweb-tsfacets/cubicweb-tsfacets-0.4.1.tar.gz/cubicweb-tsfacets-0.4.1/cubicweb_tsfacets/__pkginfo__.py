# pylint: disable=W0622
"""cubicweb-tsfacets application packaging information"""


modname = "cubicweb_tsfacets"
distname = "cubicweb-tsfacets"

numversion = (0, 4, 1)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "This cube implements facets using postgresql text search vectors."
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/tsfacets"

__depends__ = {
    "cubicweb": ">= 3.31.1",
    "typing_extensions": None,
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python :: 3",
    "Programming Language :: JavaScript",
]
