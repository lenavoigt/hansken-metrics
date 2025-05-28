from typing import Optional, List, Tuple

from hansken.connect import ProjectContext
from hansken.query import *
from hansken.remote import SearchResult


def get_evidence_ids(context: ProjectContext) -> List[str]:
    """
    Get a list of the evidence ids of a project.

    :param context: Hansken project context object.
    :return: 
    """
    evidence_ids = []
    search_term = "type:image"
    search_results = context.search(search_term)
    for trace in search_results:
        evidence_ids.append(trace.image_id)
    return evidence_ids


def count_traces_of_type(context: ProjectContext, type_to_search: str, evidence_id: Optional[str] = None) -> int | None:
    """
    Count the number of traces of a specified type.

    :param context: Hansken project context object.
    :param type_to_search: Trace type name according to HQL trace model.
    :param evidence_id: Identifier of an image in the Hansken case. If None, the number of traces will be counted for
    the whole case.
    :return: Number of traces of that type.
    """
    image_search = ''
    if evidence_id:
        image_search = 'image:' + evidence_id + ' '

    facet = TermFacet('type', size=1024)

    # Concatenated HQL search term
    search_term = image_search + 'type:' + type_to_search + ' '

    # Search and count using facets (to avoid returning the actual traces)
    with context.search(search_term, facets=facet, count=0) as search_result:
        type_to_search_facet = next(
            (bucket for bucket in search_result.facets[0].values() if bucket.value == type_to_search), None)
        if type_to_search_facet:
            count = type_to_search_facet.count
        else:
            count = None

    return count


def count_traces_with_hql(context: ProjectContext, hql_query: str, facet_value_to_count: str,
                          facet_for_filtering: str = 'type',
                          evidence_id: Optional[str] = None) -> int | None:
    """
    Count the number of traces that match a hql query.

    :param context: Hansken project context object.
    :param hql_query: The HQL query that should be conducted.
    :param facet_value_to_count: The specific facet value to use when selecting the count, according to the HQL trace
    model. For example, if the default facet to filter by is the trace type, this parameter should specify which trace
    type to retrieve the count for.
    :param facet_for_filtering: Facet acting like a filter, similar to those in a pivot table. Based on the query
    results, this parameter defines which facet should be used to create the buckets that hold the counters. By default,
    this is the trace type. For more details, see the Hansken Py documentation.
    :param evidence_id: Identifier of an image in the Hansken case. If None, the number of traces will be counted for
    the whole case.
    :return: Number of traces of that type.
    """
    image_search = ''
    if evidence_id:
        image_search = 'image:' + evidence_id + ' '

    facet = TermFacet(facet_for_filtering, size=1024)

    search_term = image_search + '(' + hql_query + ')'

    # Search and count using facets (to avoid returning the actual traces)
    with context.search(search_term, facets=facet, count=0) as search_result:
        selected_facet_value = next(
            (facet_value for facet_value in search_result.facets[0].values() if
             facet_value.value == facet_value_to_count), None)
        if selected_facet_value:
            count = selected_facet_value.count
        else:
            count = None

    return count


def get_buckets_with_hql(context: ProjectContext, hql_query: str, facet_for_filtering: str = 'type',
                         use_range_facet: bool = False, evidence_id: Optional[str] = None,
                         range_facet_scale: str = 'linear') -> List[Tuple[str, int]] | None:
    """
    Retrieve a list of buckets (with name and count per bucket) that match a hql query.

    :param context: Hansken project context object.
    :param facet_for_filtering: Facet acting like a filter, similar to those in a pivot table. Based on the query
    results, this parameter defines which facet should be used to create the buckets that hold the counters. By default,
    this is the trace type. For more details, see the Hansken Py documentation.
    :param hql_query: The HQL query that should be conducted.
    :param use_range_facet: Defines whether a RangeFacet should be used instead of a TermFacet when creating the
    buckets. For more details, see the Hansken Py documentation.
    :param evidence_id: Identifier of an image in the Hansken case. If None, the number of traces will be counted for
    the whole case.
    :param range_facet_scale: specify the bucket sizes. Valid values are 'linear' or 'log' for numeric values, see the
    Hansken Py documentation. Currently, for linear, the interval is always set to be 1, for logarithmic, the base is
    always set to be 10. Currently, no support for range facets that correspond to date times (day, year, month, second)
    :return:
    """
    image_search = ''
    if evidence_id:
        image_search = 'image:' + evidence_id + ' '

    if use_range_facet:
        if range_facet_scale == 'linear':
            facet = RangeFacet(facet_for_filtering, min=0, max=10000, scale=range_facet_scale, interval=1)
        elif range_facet_scale == 'logarithmic':
            facet = RangeFacet(facet_for_filtering, min=0, max=10000, scale=range_facet_scale, base=10)
        else:
            raise Exception('Invalid range facet scale selected.')
    else:
        facet = TermFacet(facet_for_filtering, size=1024)

    search_term = image_search + '(' + hql_query + ')'

    counts = []

    # Search and count using facets (to avoid returning the actual traces)
    with context.search(search_term, facets=facet, count=0) as search_result:
        facets = getattr(search_result, "facets", None)
        if not facets or len(facets) == 0:
            return None

        facet_data = facets[0]
        if not hasattr(facet_data, "values") or not callable(facet_data.values):
            return None

        for bucket in facet_data.values():
            counts.append((bucket.value, bucket.count))

    return counts


def bucket_name_present(context: ProjectContext, hql_query: str, facet_for_filtering: str,
                        bucket_names_to_search: List[str], allow_partial_match: bool = False,
                        evidence_id: Optional[str] = None) -> bool | None:
    """
    Checks if any of the provided names is present as a bucket name in a list of buckets retrieved.

    :param context: Hansken project context object.
    :param facet_for_filtering: Facet acting like a filter, similar to those in a pivot table. Based on the query
    results, this parameter defines which facet should be used to create the buckets that hold the counters. By default,
    this is the trace type. For more details, see the Hansken Py documentation.
    :param hql_query: The HQL query that should be conducted.
    :param bucket_names_to_search: Defines the bucket names that should be searched for.
    :param allow_partial_match: If True, it is sufficient that a bucket name to search is included in a bucket name that
    is found. If False, only exact matches are considered. Matching is case-insensitive.
    :param evidence_id: Identifier of an image in the Hansken case. If None, the number of traces will be counted for
    the whole case.
    :return: Match found?
    """
    buckets_found = get_buckets_with_hql(context, hql_query, facet_for_filtering, evidence_id=evidence_id)

    if len(buckets_found) == 0:
        return None

    for each_bucket_name_found, _ in buckets_found:
        if allow_partial_match:
            if any(each_bucket_name_to_search.lower() in each_bucket_name_found.lower() for each_bucket_name_to_search
                   in bucket_names_to_search):
                return True
        else:
            if any(each_bucket_name_to_search.lower() == each_bucket_name_found.lower() for each_bucket_name_to_search
                   in bucket_names_to_search):
                return True
    return False


def get_registry_value(context: ProjectContext, evidence_id: str, registry_key: str) -> SearchResult:
    """
    Retrieve tha value of a specified registry key

    :param context: Hansken project context object.
    :param evidence_id: Identifier of an image in the Hansken case.
    :param registry_key: Registry key for which the value should be extracted.
    :return: Search result of the registry query
    """
    image_search = 'image:' + evidence_id
    trace_to_search = 'type:registryEntry registryEntry.key:'
    search_term = image_search + ' ' + trace_to_search + registry_key
    search_result = context.search(search_term)
    return search_result


def count_children_of_registry_key(context: ProjectContext, registry_key: str,
                                   evidence_id: Optional[str] = None) -> int | None:
    """
    Counts the number of registry entries (children) directly under the specified Windows registry key.

    :param context: Hansken project context object.
    :param registry_key: Registry key path, e.g., "/Microsoft/Windows/CurrentVersion/Uninstall".
    :param evidence_id: Optional. If provided, restricts the count to a single evidence item.
                        Otherwise, counts children across all Windows systems in the project.
    :return: Number of registry entries (children), or None if count could not be determined
    """
    hql_query = r'parent->{type:registryEntry registryEntry.key:' + registry_key + r'}'
    count = count_traces_with_hql(context=context, hql_query=hql_query, facet_value_to_count='registryEntry',
                                  evidence_id=evidence_id)
    return count


def get_children_of_registry_key(context: ProjectContext, registry_key: str,
                                 evidence_id: Optional[str] = None) -> List[str] | None:
    """
        Returns the names of registry entries (children) directly under the specified Windows registry key.

        :param context: Hansken project context object.
        :param registry_key: Registry key path, e.g., "/Microsoft/Windows/CurrentVersion/Uninstall".
        :param evidence_id: Optional. If provided, restricts the results to a single evidence item.
                            Otherwise, returns children across all Windows systems in the project.
        :return: list of registry entries (children), or None if no children where found for the specified key
    """
    hql_query = r'parent->{type:registryEntry registryEntry.key:' + registry_key + r'}'
    registry_children_present = get_buckets_with_hql(context=context, hql_query=hql_query,
                                                     facet_for_filtering='registryEntry.name', evidence_id=evidence_id)
    return [registry_entry for registry_entry, _ in registry_children_present]


def count_all_descendants_of_registry_key(context: ProjectContext, registry_key: str,
                                          evidence_id: Optional[str] = None) -> int | None:
    """
        Counts the number of all registry entries (all descendants) under the specified Windows registry key.

        :param context: Hansken project context object.
        :param registry_key: Registry key path, e.g., "/Microsoft/Windows/CurrentVersion/Uninstall".
        :param evidence_id: Optional. If provided, restricts the count to a single evidence item.
                            Otherwise, counts children across all Windows systems in the project.
        :return: Number of all descendants registry entries, or None if count could not be determined
    """
    hql_query = r'type:registryEntry registryEntry.key:' + registry_key + r'/*'
    count = count_traces_with_hql(context=context, hql_query=hql_query, facet_value_to_count='registryEntry',
                                  evidence_id=evidence_id)
    return count
