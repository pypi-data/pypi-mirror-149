import abc
from typing import List

from bigeye_sdk.generated.com.torodata.models.generated import ComparisonMetricInfo, ComparisonMetricStatus, \
    PredefinedMetricName, ComparisonTableInfo
from bigeye_sdk.model import left_rule, right_rule


def _format_table_rows(metric_name: PredefinedMetricName,
                       source_column: str,
                       target_column: str,
                       source_value: str,
                       target_value: str,
                       difference: str,
                       source_table: str,
                       target_table: str
                       ):
    return (metric_name.name, source_column, target_column, source_value, target_value,
            difference, source_table, target_table)


def create_records(source_table: str, target_table: str, cmis: List[ComparisonMetricInfo]):
    return [_format_table_rows(cmi.comparison_metric_configuration.metric.predefined_metric.metric_name,
                               cmi.comparison_metric_configuration.source_column_name,
                               cmi.comparison_metric_configuration.target_column_name,
                               '{0:.1f}'.format(cmi.source_value),
                               '{0:.1f}'.format(cmi.target_value),
                               '{0:.2f}%'.format(cmi.difference * 100),
                               source_table,
                               target_table
                               )
            for cmi in cmis if cmi.status == ComparisonMetricStatus.COMPARISON_METRIC_STATUS_ALERT]


def evaluate_field(record, field_spec):
    """
            Evaluate a field of a record using the type of the field_spec as a guide.
            """
    if type(field_spec) is int:
        return str(record[field_spec])
    elif type(field_spec) is str:
        return str(getattr(record, field_spec))
    else:
        return str(field_spec(record))


def format_table(file, records, fields, headings, alignment=None):
    """
            Generate a Doxygen-flavor Markdown table from records.

            file -- Any object with a 'write' method that takes a single string
                parameter.
            records -- Iterable.  Rows will be generated from this.
            fields -- List of fields for each row.  Each entry may be an integer,
                string or a function.  If the entry is an integer, it is assumed to be
                an index of each record.  If the entry is a string, it is assumed to be
                a field of each record.  If the entry is a function, it is called with
                the record and its return value is taken as the value of the field.
            headings -- List of column headings.
            alignment - List of pairs alignment characters.  The first of the pair
                specifies the alignment of the header, (Doxygen won't respect this, but
                it might look good, the second specifies the alignment of the cells in
                the column.

                Possible alignment characters are:
                    '<' = Left align (default for cells)
                    '>' = Right align
                    '^' = Center (default for column headings)
            """

    num_columns = len(fields)
    assert len(headings) == num_columns

    # Compute the table cell data
    columns = [[] for i in range(num_columns)]
    for record in records:
        for i, field in enumerate(fields):
            columns[i].append(evaluate_field(record, field))

    # Fill out any missing alignment characters.
    extended_align = alignment if alignment is not None else []
    if len(extended_align) > num_columns:
        extended_align = extended_align[0:num_columns]
    elif len(extended_align) < num_columns:
        extended_align += [('^', '<')
                           for _ in range(num_columns - len(extended_align))]

    heading_align, cell_align = [x for x in zip(*extended_align)]

    field_widths = [len(max(column, key=len)) if len(column) > 0 else 0
                    for column in columns]
    heading_widths = [max(len(head), 2) for head in headings]
    column_widths = [max(x) for x in zip(field_widths, heading_widths)]

    _ = ' | '.join(['{:' + a + str(w) + '}'
                    for a, w in zip(heading_align, column_widths)])
    heading_template = '| ' + _ + ' |'
    _ = ' | '.join(['{:' + a + str(w) + '}'
                    for a, w in zip(cell_align, column_widths)])
    row_template = '| ' + _ + ' |'

    _ = ' | '.join([left_rule[a] + '-' * (w - 2) + right_rule[a]
                    for a, w in zip(cell_align, column_widths)])
    ruling = '| ' + _ + ' |'

    # file.write(heading_template.format(*headings).rstrip() + '\n')
    # file.write(ruling.rstrip() + '\n')
    # for row in zip(*columns):
    #     file.write(row_template.format(*row).rstrip() + '\n')

    heading = f'{heading_template.format(*headings).rstrip()}\n{ruling.rstrip()}\n'
    rows = '\n'.join(f'{row_template.format(*row).rstrip()}' for row in zip(*columns))
    return heading + rows


class VendorReport(abc.ABC):

    @abc.abstractmethod
    def publish(self, source_table_name: str, target_table_name: str, cti: ComparisonTableInfo):
        pass
