import shutil

import numpy as np


table_defaults = {
    'justify': 'left',
    'compact': False,
    'row_index': False,
    'header_positions': ['top'],
    'compact': False,
    'decimal_places': None,
    'column_gap_spaces': 2,
    'cross_border': '┼',
    'vertical_border': '│',
    'horizontal_border': '─',
}


def print_table(
    rows,
    file=None,
    to_stdout=True,
    justify=None,
    column_delimiter=None,
    column_widths=None,
    headers=None,
    row_index=None,
    column_index=None,
    compact=None,
    edge_gaps=None,
    trim_to_terminal=False,
    trim_width=None,
    header_positions=None,
    none_str=None,
    number_commas=True,
    decimal_places=None,
    column_gap_spaces=None,
    cross_border=None,
    vertical_border=None,
    horizontal_border=None,
    add_line_rows=None,
    indent=None,
):
    """print a table

    - for defaults, see table_defaults above

    ## Inputs
    - rows: list of lists of rows
    - file: file handle to output to
    - to_stdout:
    - justify:
    - column_delimiter: str delimiter to use between cell values
    - column_widths: list of int widths to use for each column
    - headers: list of str headers for each column
    - row_index: bool of whether to add an index column to each row
    - column_index: bool of whether to add character index to each column
    - compact: bool of whether to output table in compact mode
    - edge_gaps: bool of whether to include gaps on left and right table edges
    - trim_to_terminal: bool of whether to trim table to current terminal size
    - trim_width: int number of chars to trim table width to
    - header_positions: list of str header positions, inluding 'top' or 'bottom'
    - none_str: str to use in place of None values
    - number_commas: bool of whether to format numeric entries with commas
    - decimal_places: int number of decimal places to trim numeric values to
    - column_gap_spaces: int number of spaces used to pad column borders
    - cross_border: character to use for cross border
    - vertical_border: character to use for vertical border
    - add_line_rows: list of int row indices where to add border line rows
    - indent: int number of spaces to indent table, or str of row line prefixes
    """

    # set defaults
    if justify is None:
        justify = table_defaults['justify']
    if compact is None:
        compact = table_defaults['compact']
    if row_index is None:
        row_index = table_defaults['row_index']
    if header_positions is None:
        header_positions = table_defaults['header_positions']
    if decimal_places is None:
        decimal_places = table_defaults['decimal_places']
    if column_gap_spaces is None:
        column_gap_spaces = table_defaults['column_gap_spaces']
    if cross_border is None:
        cross_border = table_defaults['cross_border']
    if vertical_border is None:
        vertical_border = table_defaults['vertical_border']
    if horizontal_border is None:
        horizontal_border = table_defaults['horizontal_border']

    # add column index
    if column_index is not None:
        if headers is None:
            headers = ['' for i in range(len(rows[0]))]
        if isinstance(column_index, bool):
            column_index_labels = [
                chr(ord('A') + i) for i in range(len(headers))
            ]
        else:
            column_index_labels = column_index

        delimiter = '. '
        headers = [
            label + delimiter + header
            for header, label in zip(headers, column_index_labels)
        ]

    # add row index
    if row_index:
        if not isinstance(row_index, bool):
            first_index = row_index
        else:
            first_index = 0

        indexed_rows = []
        for r, row in enumerate(rows):
            indexed_rows.append([first_index + r + 1] + row)
        rows = indexed_rows

        if headers is not None:
            headers.insert(0, '')

    # format rows
    formatted_rows = _format_rows(
        rows=rows,
        headers=headers,
        header_positions=header_positions,
        to_stdout=to_stdout,
        file=file,
        compact=compact,
        column_widths=column_widths,
        trim_to_terminal=trim_to_terminal,
        trim_width=trim_width,
        column_gap_spaces=column_gap_spaces,
        vertical_border=vertical_border,
        horizontal_border=horizontal_border,
        cross_border=cross_border,
        none_str=none_str,
        number_commas=number_commas,
        decimal_places=decimal_places,
        justify=justify,
        column_delimiter=column_delimiter,
        edge_gaps=edge_gaps,
        ellipsis=True,
        add_line_rows=add_line_rows,
        indent=indent,
    )

    # output rows
    if to_stdout:
        print(formatted_rows['as_str'])
    if file is not None:
        print(formatted_rows['as_str'], file=file)

    # return table
    return formatted_rows


def _format_rows(
    rows,
    headers,
    header_positions,
    to_stdout,
    file,
    compact,
    column_widths,
    trim_to_terminal,
    column_gap_spaces,
    vertical_border,
    horizontal_border,
    cross_border,
    number_commas,
    decimal_places,
    add_line_rows,
    indent,
    **row_format,
):

    # set derived parameters
    if to_stdout is None:
        to_stdout = file is None
    if compact:
        if compact == 2:
            column_delimiter = ' '
            line_delimiter = ' '
            edge_gaps = False
        else:
            column_delimiter = '  '
            line_delimiter = '  '
            edge_gaps = False
    else:
        column_delimiter = (
            ' ' * column_gap_spaces + vertical_border + ' ' * column_gap_spaces
        )
        line_delimiter = (
            horizontal_border * column_gap_spaces
            + cross_border
            + horizontal_border * column_gap_spaces
        )
        edge_gaps = True
    row_format['column_delimiter'] = column_delimiter
    if row_format.get('edge_gaps') is None:
        row_format['edge_gaps'] = edge_gaps
    if len(column_delimiter) != len(line_delimiter):
        raise Exception('delimiters need equal length')
    if trim_to_terminal:
        n_terminal_columns = shutil.get_terminal_size().columns
        trim_width = row_format.get('trim_width')
        if trim_width is None or trim_width > n_terminal_columns:
            row_format['trim_width'] = n_terminal_columns

    if headers is not None:
        headers = [str(header) for header in headers]

    # format numbers
    if number_commas or decimal_places is not None:
        if number_commas and decimal_places is not None:
            format_str = '{:,.' + str(decimal_places) + 'f}'
        elif number_commas and decimal_places is None:
            format_str = '{:,}'
        elif not number_commas and decimal_places is not None:
            format_str = '{:.' + str(decimal_places) + 'f}'
        rows = [
            [
                format_str.format(cell)
                if isinstance(cell, (float, int, np.int64))
                else cell
                for cell in row
            ]
            for row in rows
        ]

    # stringify
    rows = [[str(column) for column in row] for row in rows]

    # compute column widths
    if column_widths is None:

        # include headers in column width calculations
        if headers is not None:
            width_rows = [headers] + rows
        else:
            width_rows = rows

        # get max width for each column
        n_columns = len(rows[0])
        column_widths = [0] * n_columns
        for row in width_rows:
            for c, column in enumerate(row):
                column_size = len(column)
                if column_size > column_widths[c]:
                    column_widths[c] = column_size
    row_format['column_widths'] = column_widths

    # create format for line rows
    line_format_kwargs = dict(
        row_format,
        column_delimiter=line_delimiter,
        ellipsis=False,
    )

    # format rows
    str_rows = []
    if headers is not None or add_line_rows is not None:
        line_row = [horizontal_border * width for width in column_widths]
    for row in rows:
        str_rows.append(_format_row(row, **row_format))
    if add_line_rows is not None:
        line_row_formatted = _format_row(line_row, **line_format_kwargs)
        for index in add_line_rows[::-1]:
            str_rows.insert(index, line_row_formatted)
    if headers is not None and 'top' in header_positions:
        str_rows.insert(0, _format_row(headers, **row_format))
        str_rows.insert(1, _format_row(line_row, **line_format_kwargs))
    if headers is not None and 'bottom' in header_positions:
        str_rows.append(_format_row(line_row, **line_format_kwargs))
        str_rows.append(_format_row(headers, **row_format))

    # indent
    if indent is not None:
        if isinstance(indent, int):
            indent = ' ' * indent
        str_rows = [indent + str_row for str_row in str_rows]

    # format total output
    as_str = '\n'.join(str_rows)
    longest_row = max(len(str_row) for str_row in str_rows)
    return {
        'as_str': as_str,
        'longest_row': longest_row,
    }


def _format_row(
    row,
    none_str,
    justify,
    column_widths,
    column_delimiter,
    edge_gaps,
    trim_width,
    ellipsis,
):

    # replace None values
    if none_str is not None:
        row = [(none_str if column is None else column) for column in row]

    # create row column by column
    line = []
    for c, column in enumerate(row):

        # get width
        width = column_widths[c]

        # downsize
        as_str = column[:width]

        # justify
        if justify == 'left':
            as_str = as_str.ljust(width)
        elif justify == 'right':
            as_str = as_str.rjust(width)
        else:
            raise Exception('unknown justify value: ' + str(justify))

        # append to line
        line.append(as_str)
    line = column_delimiter.join(line)

    # add edge gaps
    # a bit hacky: if using edge gaps, use the column_delimiter/2
    if edge_gaps:
        half_len = int(len(column_delimiter) / 2)
        line = column_delimiter[-half_len:] + line + column_delimiter[:half_len]

    if trim_width is not None:
        trimmed = False
        if len(line) > trim_width:
            line = line[:trim_width]
            trimmed = True

        if trimmed and ellipsis and line[-1] != ' ':
            line = line[:-3] + '...'

    return line

