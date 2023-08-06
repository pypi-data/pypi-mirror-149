# -*- coding: utf-8 -*-
# copyright 2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from typing import Dict, List, Set, Tuple, Optional, Union
from typing_extensions import TypedDict
import re

from cubicweb.appobject import AppObject
from cubicweb.rset import ResultSet
from cubicweb_tsfacets import (
    sqlcursor,
    convert_sql_to_rql,
    build_rset_descr,
    convert_to_tsquery,
)


class FacetItemType(TypedDict):
    value: str
    count: str


class RQLRequestFacetDef:
    def __init__(
        self,
        rql_request: str,
        needs_mapping: bool = False,
    ):
        self.rql_request = rql_request
        self.needs_mapping = needs_mapping


class TSFacets(AppObject):
    """Base class for facets declaration.

    Each subclass of it allow to define a group of facets
    allowing to retrieve target entities. These entities don't have
    to be of the same type.

    Each subclass represent a specific postgresql table.

    :attr:`key_names_to_rql_definition`
        a dictionary linking each facet key with a RQLRequestFacetDef object.
        This object represents a RQL request with the information of if we
        need a mapping table for the value or not. We need a mapping if we
        want to index string with space or other characters like "'".

    :attr:`text_search_indexation`
        a RQL request returning a list of tuples:
        (target entity eid, text to index for full text search)
    """

    __registry__ = "tsfacets"
    __abstract__ = True

    key_names_to_rql_definition: Dict[str, RQLRequestFacetDef] = {}

    text_search_indexation: str = ""

    target_etypes: Set = set()

    table_name: Optional[str] = None

    def get_mapping_table_name(self, facet_key: str) -> str:
        return build_mapping_table_name(self, facet_key)

    def _build_tsvector_parts(self, selected_facets: Dict[str, List[str]]):
        tsvector_parts = []
        for facet_key in self.key_names_to_rql_definition:
            values = selected_facets.get(facet_key)
            if not values:
                continue
            for value in values:
                tsvector_parts.append(f"{facet_key}.{value.lower()}")
        return tsvector_parts

    def _build_sql_parts(
        self,
        rql: str = None,
        rql_args: Dict = None,
        selected_facets: Dict[str, List[str]] = None,
        text_search: str = None,
        quote_to_use_in_sql="'",
        with_row_nb: bool = False,
    ) -> Tuple[str, str, Dict[str, str]]:
        if rql:
            converted_sql, sql_args = convert_sql_to_rql(self._cw.cnx, rql, rql_args)
            if with_row_nb:
                converted_sql = f"""
                SELECT _TABLE_TO_COUNT.*, ROW_NUMBER() OVER () AS row_nb
                FROM ({converted_sql}) as _TABLE_TO_COUNT
                """
            sql_restriction_part = f"""
            JOIN ({converted_sql}) as _TABLE_FROM_RQL(target_eid)
            ON TSFT.eid = _TABLE_FROM_RQL.target_eid
            """
        else:
            sql_restriction_part = ""
            sql_args = {}
        if rql_args:
            sql_args.update(rql_args)

        ts_vector_parts = self._build_tsvector_parts(selected_facets or {})
        where_parts = []
        if ts_vector_parts:
            # here we use double ' because we will be inside a function.
            where_parts.append(
                f"""
                TSFT.facetvector @@ to_tsquery(
                    {quote_to_use_in_sql}{'&'.join(ts_vector_parts)}{quote_to_use_in_sql}
                )
            """
            )

        if text_search:
            query = convert_to_tsquery(text_search)
            where_parts.append(
                f"""
                to_tsquery({quote_to_use_in_sql}{query}{quote_to_use_in_sql})
                @@ TSFT.textsearchvector
            """
            )

        if where_parts:
            where = f"WHERE {' AND '.join(where_parts)}"
        else:
            where = ""

        return sql_restriction_part, where, sql_args

    def get_facets_values_with_count(
        self,
        rql_restriction: str = None,
        rql_args: Dict = None,
        selected_facets: Dict[str, List[str]] = None,
        text_search: str = None,
    ) -> Dict[str, List[FacetItemType]]:
        """
        Retrieve all facet values with target entities count for each of them.
        :param rql_restriction: A RQL with a single variable in the Any close corresponding
        to the target entities.
        :param rql_args: arguments of rql_restriction.
        :param selected_facets: all selected facets as Dict[facet_key, [facet values]].
        :param text_search: a string to filter results.
        :return: a dictionary of the type Dict[facet_key, Dict[value, target entity count]]
        """
        selected_facets = selected_facets or {}
        sql_restriction_part, where_sql_part, sql_args = self._build_sql_parts(
            rql_restriction,
            rql_args,
            selected_facets,
            text_search,
        )

        with sqlcursor(
            self._cw.cnx.repo,
            errmsg=(
                "Error with tsfacets table, are you sure "
                "you executed generate-tsfacets-tables ?"
            ),
        ) as crs:
            crs.execute(
                f"""
                SELECT
                    -- Break encoded words to get `code` and `value`
                    split_part(word, '.', 1) as code,
                    split_part(word, '.', 2) as value,
                    ndoc
                FROM
                    -- Word-count on all qualified records
                    ts_stat($ts_stat$
                        SELECT TSFT.facetvector
                        FROM {self.table_name} as TSFT
                        {sql_restriction_part}
                        {where_sql_part}
                    $ts_stat$)
                ORDER BY code, ndoc DESC;
                """,
                sql_args,
            )

            all_facets: Dict[str, List[FacetItemType]] = {}
            for code, value, count in crs.fetchall():
                if code not in self.key_names_to_rql_definition:
                    continue
                if value in selected_facets.get(code, []):
                    continue

                all_facets.setdefault(code, []).append(
                    {
                        "value": value,
                        "count": count,
                    }
                )

        return all_facets

    def get_target_entities_count(
        self,
        rql_restriction: str = None,
        rql_args: Dict = None,
        selected_facets: Dict[str, List[str]] = None,
        text_search: str = None,
    ) -> int:
        """
        Count target entities taking into account selected facets.
        :param rql_restriction: A RQL with a single variable in the Any close corresponding
        to the target entities.
        :param rql_args: arguments of rql_restriction.
        :param selected_facets: all selected facets as Dict[facet_key, [facet values]].
        :param text_search: a string to filter results.
        :return: how many entities correspond to these facets.
        """
        if rql_restriction and not (text_search or selected_facets):
            return len(self._cw.execute(rql_restriction, rql_args, build_descr=False))
        sql_restriction_part, where_sql_part, sql_args = self._build_sql_parts(
            rql_restriction, rql_args, selected_facets, text_search
        )

        with sqlcursor(
            self._cw.cnx.repo,
            errmsg=(
                "Error with tsfacets table, are you sure "
                "you executed generate-tsfacet-tables ?"
            ),
        ) as crs:
            crs.execute(
                f"""
                SELECT COUNT(*)
                FROM {self.table_name} as TSFT
                {sql_restriction_part}
                {where_sql_part}
                """,
                sql_args,
            )
            try:
                return int(crs.fetchall()[0][0])
            except IndexError:
                return 0

    def get_target_entities_rset(
        self,
        base_rql: str,
        selected_facets: Dict[str, List[str]],
        rql_args: Dict = None,
        text_search: str = None,
    ) -> ResultSet:
        """
        Construct a rset corresponding to the selected facets.
        :param base_rql: a rql allowing to get target entities with all needed parameters.
        Target entity have to be the first variable in the Any clause.
        :param selected_facets: all selected facets as Dict[facet_key, [facet values]].
        :param rql_args: arguments for base_rql.
        :param text_search: a string to filter results.
        :return: a CubicWeb ResultSet.
        """
        if not (text_search or selected_facets):
            return self._cw.execute(base_rql, rql_args)
        rql_args = rql_args or {}
        sql_restriction_part, where_sql_part, sql_args = self._build_sql_parts(
            base_rql, rql_args, selected_facets, text_search, with_row_nb=True
        )
        limit_match = re.search(r"LIMIT \d+", sql_restriction_part)
        if limit_match:
            limit_part = limit_match.group(0)
            sql_restriction_part = sql_restriction_part.replace(limit_part, "")
        else:
            limit_part = ""
        offset_match = re.search(r"OFFSET \d+", sql_restriction_part)
        if offset_match:
            offset_part = offset_match.group(0)
            sql_restriction_part = sql_restriction_part.replace(offset_part, "")
        else:
            offset_part = ""

        with sqlcursor(
            self._cw.cnx.repo,
            errmsg=(
                "Error with tsfacets table, are you sure "
                "you executed generate-tsfacets-tables ?"
            ),
        ) as crs:
            crs.execute(
                f"""
                SELECT
                    _TABLE_FROM_RQL.*
                FROM
                    {self.table_name} as TSFT
                    {sql_restriction_part}
                {where_sql_part}
                ORDER BY _TABLE_FROM_RQL.row_nb
                {limit_part}
                {offset_part}
                """,
                {
                    **sql_args,
                    **rql_args,
                },
            )
            raw_results = crs.fetchall()
        results = []
        for row in raw_results:
            # we remove row_nb
            results.append(row[:-1])
        description = build_rset_descr(self._cw, base_rql, rql_args, results)
        rset = ResultSet(results, base_rql, rql_args, description)
        rset.req = self._cw
        return rset

    def get_id_to_value_mapping(self, facet_key: str) -> Union[Dict[str, str], None]:
        """
        This method retrieves the mapping id -> value,
        if we are in the case a mapping was needed.
        :param facet_key: the key for which we want the mapping.
        :return: a dictionnary containing the mapping, or
        or None if there is no mapping.
        """
        if not self.key_names_to_rql_definition[facet_key].needs_mapping:
            return None
        with sqlcursor(
            self._cw.cnx.repo,
            errmsg=(
                "Error with tsfacets table, are you sure "
                "you executed generate-tsfacets-tables ?"
            ),
        ) as crs:
            crs.execute(
                f"""
                SELECT CAST(id as TEXT), value FROM {self.get_mapping_table_name(facet_key)}
                WHERE value is not NULL AND value <> ''
                """
            )
            return dict(crs.fetchall())

    def get_id_to_value(self, facet_key: str, f_id: Union[str, int]) -> str:
        """
        This method retrieves value for a given facet_key and id,
        if we are in the case a mapping was needed.
        :param facet_key: the key for which we want the mapping.
        :param f_id: the id for which we want the value.
        :return: the corresponding value.
        """
        if not self.key_names_to_rql_definition[facet_key].needs_mapping:
            return f_id
        with sqlcursor(
            self._cw.cnx.repo,
            errmsg=(
                "Error with tsfacets table, are you sure "
                "you executed generate-tsfacets-tables ?"
            ),
        ) as crs:
            crs.execute(
                f"""
                SELECT value FROM {self.get_mapping_table_name(facet_key)} WHERE id = %(id)s
                """,
                {"id": int(f_id)},
            )
            return crs.fetchall()[0][0]


def build_mapping_table_name(facet_cls: TSFacets, facet_key: str):
    return f"{facet_cls.table_name}_{facet_key}_mapping"
