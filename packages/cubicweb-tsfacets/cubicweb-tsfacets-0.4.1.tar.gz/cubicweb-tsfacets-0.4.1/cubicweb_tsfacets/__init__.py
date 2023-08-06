"""cubicweb-tsfacets application package

This cube implements facets using postgresql text search vectors.
"""
import string
from contextlib import contextmanager

from rql import RQLHelper

from cubicweb.server.querier import QuerierHelper, manual_build_descr
from cubicweb.server.sources.rql2sql import SQLGenerator


INVALID_TSQUERY_CHARS = string.punctuation + "\0"
SANITIZE_TRANSMAP = str.maketrans(
    INVALID_TSQUERY_CHARS, len(INVALID_TSQUERY_CHARS) * " "
)


@contextmanager
def sqlcursor(repo, errmsg=None):
    cnx = repo.system_source.get_connection()
    crs = cnx.cursor()
    try:
        yield crs
    except Exception:
        errmsg = errmsg or "an error occured"
        print(errmsg)
        cnx.rollback()
        raise  # if something went wrong, we likely would like to stop right
        # here to ease the correction of the issue.
    else:
        cnx.commit()
    cnx.close()


def convert_sql_to_rql(cnx, rql, rql_args=None):
    rqlhelper = RQLHelper(
        cnx.vreg.schema,
        special_relations={"eid": "uid", "has_text": "fti"},
        backend="postgres",
    )
    qhelper = QuerierHelper(cnx.repo, cnx.vreg.schema)
    union = rqlhelper.parse(rql)
    rqlhelper.compute_solutions(union)
    rqlhelper.simplify(union)
    plan = qhelper.plan_factory(union, {}, cnx)
    plan.preprocess(union)
    for select in union.children:
        select.solutions.sort(key=lambda x: list(x.items()))
    dbhelper = cnx.repo.system_source.dbhelper
    sql_generator = SQLGenerator(cnx.vreg.schema, dbhelper)
    sql, args, _ = sql_generator.generate(union, rql_args)
    return sql, args


def build_rset_descr(cnx, rql, args, results):
    rqlhelper = RQLHelper(
        cnx.vreg.schema,
        special_relations={"eid": "uid", "has_text": "fti"},
        backend="postgres",
    )
    rqlst = rqlhelper.parse(rql)
    rqlhelper.compute_solutions(rqlst, {"eid": cnx.entity_type}, kwargs=args)
    return manual_build_descr(cnx, rqlst, args, results)


def convert_to_tsquery(search_string: str) -> str:
    """build a ready-to-use tsquery

    remove all invalid / potential ts_ operators and add
    ':*' at the end of each word to perform a prefixed search.
    """
    sanitized = search_string.translate(SANITIZE_TRANSMAP)
    return "&".join(f"{chunk}:*" for chunk in sanitized.split())


def includeme(config):
    pass
