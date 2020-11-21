"""A filter function that can work on any JSON-like data structure
(i.e. lists, dicts, and values). The filter function takes a list of the JSON-like
data instances and then applies filters (specified by simple filter format) to them.
Filters can be supplied to filter out matching instances or filter in matching instances.
The filters can be for string matches, substring check (via python "in"), re.search pattern
or re.match pattern. Filters may also be flagged to be applied separately as a set
(i.e. compound filter).

"""

import copy
import operator
from functools import reduce
import re


def get_by_path(root, items):
    """Access a nested object in root by item sequence.

    Source: https://stackoverflow.com/questions/19589233/reduce-function-with-three-parameters
    """
    return reduce(operator.getitem, items, root)


def in_nested_path(root, items):
    """ 'in' equivalent for a nested dict/list structure"""
    try:
        get_by_path(root, items)
    except KeyError:
        return False

    return True


def set_by_path(root, items, value):
    """Set a vlaue in a nested object in root by item sequence"""
    get_by_path(root, items[:-1])[items[-1]] = value


def filter_data(data, filters, mode="inclusive", compound=True):
    """Filter in or out data instances based on supplied filters

    Can handle fields in nested dict/list(s), at any level

    Deepcopies data so that the data returned is entirely independent set

    Filter format:

    filter_1 = {
        "type": "<type>",
        "field": "<field>",
        "value": "<value>",
        "replace": "<replacement_value>"
    }

    where:

    <type> may be one of "match", "in", "re-match", "re-search", "replace". <type> specifies
    the type of filter mechanism to be applied. "match" is exact string match, "in" is the
    application of the pythonic "in" for substings, and "re-match" and "re-search" apply the
    corresponding python regex function.

    <field> is the field to apply the filter to. The field can also be a nested
    field. For example, "field1.field2.field3" will apply the filter to the data_structure[field1][field2][field3]
    and "field1.[2].field2" would apply the filter to data_structure[field1][2][field2], where the path
    component "[2]" denotes an index in a list.

    <value> is the value of the filter to be evaluated against the field value.
    For filters of type "re-match" and "re-search", these values can be anything
    within the python regex pattern string spec

    <replace> is the value to replace the actual <value> that was matched, if the
    filter type is "replace"

    Args:
        data (list): list of JSON-like data structures. Each item in the list
          should be a JSON-like (i.e. dict and list based) data structure
        filters (list): list of filters, where each fitler is a dict of the
          above specified form
        mode (str): the mode in which to apply the filters to the data. "include"
          specifies that all data instances that match the filter(s) will be
          included in the returned data. "exclude" specifies that all data instances
          that match the filter(s) will be excluded from the returned data. If one of
          the filters is of type 'replace', then this flag is ignored.
        compound (bool): flag to specify whether the filters should be applied
          together (as one compound filter) or separately. If one of the filters
          is of type 'replace', then this flag is ignored.

    Returns: (list) data instances that matched filter(s)
    """
    results = []
    data = copy.deepcopy(data)  # modify locally
    filters = copy.deepcopy(filters)  # modify locally

    if not isinstance(data, list):
        data = [data]  # make list so can iterate regardless

    if not isinstance(filters, list):
        filters = [filters]

    # expand nested field paths to a list (to work with access functions)
    for filt in filters:
        filt["field"] = filt["field"].split(".")

    # Any field path that has the "[#]" for are interpreted as list
    # indexes (instead of keys), so convert them to integers so nested
    # access works correctly
    for filt in filters:
        for idx, path_component in enumerate(filt["field"]):
            if re.match("\[[0-9]+\]", path_component):
                filt["field"][idx] = int(path_component.strip("[]"))

    for instance in data:
        match_count = 0
        replace_flag = False
        match = False

        for filt in filters:
            if not in_nested_path(instance, filt["field"]):
                continue

            if filt["type"] == "match":
                if get_by_path(instance, filt["field"]) == filt["value"]:
                    match_count += 1
                    if not compound:
                        break
            elif filt["type"] == "in":
                if filt["value"] in get_by_path(instance, filt["field"]):
                    match_count += 1
                    if not compound:
                        break
            elif filt["type"] == "re-match":
                if re.match(filt["value"], get_by_path(instance, filt["field"])):
                    match_count += 1
                    if not compound:
                        break
            elif filt["type"] == "re-search":
                if re.search(filt["value"], get_by_path(instance, filt["field"])):
                    match_count += 1
                    if not compound:
                        break
            elif filt["type"] == "replace":
                replace_flag = True
                instance_value = get_by_path(instance, filt["field"])
                matches = re.findall(filt["value"], instance_value)
                if matches:
                    for match in matches:
                        if type(match) is tuple:
                            # multi group regular expression, just going to use first one
                            match = match[0]
                        instance_value = instance_value.replace(match, filt["replace"])
                    set_by_path(instance, filt["field"], instance_value)
                    match_count += 1

        if replace_flag:
            # if one of the filters was of type==replace, 'compound' and
            # 'exclusive/inclusive' options are ignored as can no longer apply.
            # All data instances are returned no matter what (albeit some possibly modified)
            results.append(instance)
        else:
            # Determine if match occured based on filters matched and whether
            # the filters are specified as a compound filter
            if compound:
                if match_count == len(filters):
                    match = True
            elif not compound:
                if match_count > 0:
                    match = True

            if match and mode == "inclusive":
                # inclusive filter mode and a match, so add
                results.append(instance)
            elif not match and mode == "exclusive":
                # exclusive filter mode and not a match, so add
                results.append(instance)

    return results


