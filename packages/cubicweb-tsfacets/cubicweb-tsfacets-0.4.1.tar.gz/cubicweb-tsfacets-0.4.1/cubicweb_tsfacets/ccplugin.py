from cubicweb.cwctl import CWCTL
from cubicweb.toolsutils import Command
from cubicweb.utils import admincnx

from cubicweb_tsfacets.importer import build_facet_table


@CWCTL.register
class GenerateFacetsTables(Command):
    """Generate TSFacets tables.


    <instance>
      the identifier of the instance
    """

    name = "generate-tsfacets-tables"
    arguments = "<instance id>"
    min_args = max_args = 1

    def run(self, args):
        appid = args.pop(0)
        with admincnx(appid) as cnx:
            for regid in cnx.vreg["tsfacets"]:
                for facet_cls in cnx.vreg["tsfacets"][regid]:
                    build_facet_table(cnx, facet_cls)
