Summary
-------
This cube implements facets using postgresql text search vectors.

What does this cube offer ?
---------------------------

This cube defines a new CubicWeb AppObject registry: `tsfacets`.
The base class is `cubicweb_tsfacets.views.TSFacets`; it provides
three methods allowing to recover information to use facets in
a CubicWeb application:

* `get_facets_values_with_count`, which recovers all available facets
  with how many target entities it filters for each value;
* `get_target_entities_count`, which counts target entities taking into
  account the selected facets and possibly a RQL request to restrict
  results;
* `get_target_entities_rset`, which builds a CubicWeb ResultSet taking
  into account the selected facets and possibly a RQL request to restrict
  results.

How to use it ?
---------------

For each group of facets, you have to define a child class of
`cubicweb_tsfacets.views.TSFacets`. Then, you have to complete
the following attributes:

* `key_names_to_rql_definition`: a dictionary linking each facet key 
  with a RQLRequestFacetDef object. A facet key must only contain
  characters, no space, no ".", no "_", etc.
  This object represents a RQL request with the information of if we
  need a mapping table for the value or not. We need a mapping if we
  want to index string with space or other characters like "'";
* `text_search_indexation`: a RQL request returning a list of tuples:
  (target entity eid, text to index for full text search). This
  attribute is optional, and is only used if you want to add
  text search to your result list. Note: this feature will be added in
  an upcoming version;
* `target_etypes`: which entity types are targeted by your facet search;
* `table_name`: the name of the specific postgresql table.

Example of implementation:
--------------------------

In this example, we want to add facets to `Performance` entities.
These facets will be the city, country and theater of the representation,
the date of the representation and the director.

```python
from cubicweb_tsfacets.views import TSFacets, RQLRequestFacetDef


class PerformanceTSFacets(TSFacets):
    __regid__ = "performance_tsfacets"
    table_name = "performance_tsfacets"

    key_names_to_rql_definition = {
        "city": RQLRequestFacetDef("Any X, R Where X representation_city R", True),
        "country": RQLRequestFacetDef("Any X, R Where X representation_country R", True),
        "theater": RQLRequestFacetDef("Any X, R Where X representation_theater R", True),
        "date": RQLRequestFacetDef("Any X, D Where X formatted_start_date D", False),
        "director": RQLRequestFacetDef(
          "Any X, D Where X is Performance, C manifestation X, "
          "C contributor D, C role R, R code 500",
          False
        ),
    }

    target_etypes = {"Performance"}
```

Thus, `CubicWeb-TSFacets` will provide the methods we will need to
build our interface.
