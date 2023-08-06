from cubicweb_tsfacets import convert_sql_to_rql, sqlcursor
from cubicweb_tsfacets.views import build_mapping_table_name


def build_facet_table(cnx, facet_cls):
    table_name = facet_cls.table_name
    with sqlcursor(cnx.repo, errmsg=f"could not build {table_name} table.") as crs:
        target_etype_sql_part = ",".join(
            (f"'{etype}'" for etype in facet_cls.target_etypes)
        )
        crs.execute(
            f"""
            CREATE TEMPORARY TABLE {table_name}_entities AS (
                SELECT eid FROM entities WHERE type IN ({target_etype_sql_part})
            )
        """
        )
        from_parts = []
        vector_parts = []
        args = {}
        for (
            facet_key,
            request_facet_def,
        ) in facet_cls.key_names_to_rql_definition.items():
            sql, _args = convert_sql_to_rql(cnx, request_facet_def.rql_request)
            args.update(_args)
            if request_facet_def.needs_mapping:
                # here we need to create a mapping table:
                rset = cnx.execute(request_facet_def.rql_request)
                all_values = set()
                for _target, value in rset:
                    all_values.add(value)

                mapping_table_name = build_mapping_table_name(facet_cls, facet_key)
                crs.execute(f"DROP TABLE IF EXISTS {mapping_table_name}")
                crs.execute(
                    f"""
                    CREATE TABLE
                        {mapping_table_name} (id serial PRIMARY KEY, value varchar)
                    """
                )
                insert = f"""
                INSERT INTO {mapping_table_name} (value)
                values {",".join(["(%s)"]*len(all_values))}
                """
                crs.execute(insert, list(all_values))
                crs.execute(f"CREATE INDEX ON {mapping_table_name}(value)")
                from_parts.append(
                    f"""
                    LEFT OUTER JOIN (
                        SELECT
                            _f{facet_key}_to_be_mapped.target_eid,
                            {mapping_table_name}.id
                        FROM
                            ({sql}) as _f{facet_key}_to_be_mapped(target_eid,value)
                            JOIN {mapping_table_name} ON (
                                {mapping_table_name}.value = _f{facet_key}_to_be_mapped.value
                            )
                    ) as _f{facet_key}(target_eid,value)
                    ON entities.eid = _f{facet_key}.target_eid
                    """  # noqa
                )
            else:
                from_parts.append(
                    f"""
                    LEFT OUTER JOIN ({sql}) as _f{facet_key}(target_eid,value)
                    ON entities.eid = _f{facet_key}.target_eid
                    """
                )
            vector_parts.append(
                f"""
                ARRAY_AGG(
                    DISTINCT CASE WHEN _f{facet_key}.value is NULL
                    THEN ''  ELSE '{facet_key}.' || _f{facet_key}.value END
                )
                """
            )
        if facet_cls.text_search_indexation:
            sql, _args = convert_sql_to_rql(cnx, facet_cls.text_search_indexation)
            args.update(_args)
            fti_vector_from = f"""
            LEFT OUTER JOIN ({sql}) as _tstable(target_eid, text)
            ON entities.eid = _tstable.target_eid
            """
            fti_vector = "TO_TSVECTOR(_tstable.text) as textsearchvector"
        else:
            fti_vector = "NULL as textsearchvector"
            fti_vector_from = ""
        crs.execute(f"DROP TABLE IF EXISTS {table_name}")
        crs.execute(
            f"""
                CREATE TABLE {table_name} AS (
                    SELECT
                        entities.eid,
                        ARRAY_TO_TSVECTOR(
                            ARRAY_REMOVE(
                                {"||".join(vector_parts)},
                                ''
                            )
                        ) as facetvector,
                        {fti_vector}
                    FROM
                        {table_name}_entities AS entities
                        {" ".join(from_parts)}
                        {fti_vector_from}
                    GROUP BY entities.eid
                    {", _tstable.text" if fti_vector_from else ""}
                )
            """,
            args,
        )
        if fti_vector_from:
            crs.execute(
                f"CREATE INDEX {table_name}_ginidx ON {table_name} USING GIN(textsearchvector)"
            )
        crs.execute(
            f"CREATE INDEX {table_name}_fti_ginidx ON {table_name} USING GIN(facetvector)"
        )
