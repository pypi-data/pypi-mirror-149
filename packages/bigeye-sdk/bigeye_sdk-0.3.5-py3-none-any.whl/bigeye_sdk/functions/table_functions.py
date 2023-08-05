from typing import List
from bigeye_sdk.log import get_logger
from fuzzywuzzy import process

log = get_logger(__file__)


def transform_table_list_to_dict(tables: List[dict]) -> dict:
    return {t['datasetName'].lower(): _transform_table_field_list_to_dict(t) for t in tables}


def _transform_table_field_list_to_dict(table: dict) -> dict:
    """
    Converts the table['fields'] list to a dictionary of { <tableName.lower>: <field_entry> } for quick, easy,
    case-insensitive keying
    :param table: a dictionary representing a dataset in Bigeye derived from the dataset/tables endpoint.
    :return: the modified table entry
    """
    table['fields'] = {f['fieldName'].lower(): f for f in table['fields']}
    return table


def create_table_name_pairs(table1: List[str], table2: List[str]):
    temp_tbl2_matched = []

    for t in table1:
        temp_tbl2_matched.append(process.extract(t, table2, limit=1)[0][0])

    matching_table_pairs = list(zip(table1, temp_tbl2_matched))

    return matching_table_pairs
