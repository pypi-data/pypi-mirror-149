import math
import itertools
import shutil

import cjkjust

__all__ = [
    'BSDFormatter',
    'GNUFormatter',
    'pprint',
]


class BSDFormatter:
    """
    Warning: Tab in strings ruins the print-out.
    """
    def __init__(self, total_width=None, width_between_cols=1):
        """
        :param total_width: the disposable total width, default to terminal
               width
        :param width_between_cols: width between columns, default to 1
        """
        self.total_width = total_width or shutil.get_terminal_size().columns
        self.width_between_cols = width_between_cols

    def calc_layout(self, n_strings, column_width):
        # expected_ncols * column_width +
        #     (expected_ncols - 1) * width_between_cols <= total_width
        #
        #   -> expected_ncols <= (total_width + width_between_cols) /
        #                        (column_width + width_between_cols)
        #
        # Therefore, expected_ncols is at most the floor of the RHS
        expected_ncols = math.floor(
            (self.total_width + self.width_between_cols) /
            (column_width + self.width_between_cols))
        expected_ncols = max(expected_ncols, 1)
        actual_nrows = math.ceil(n_strings / expected_ncols)
        actual_ncols = (n_strings - 1) // actual_nrows + 1
        return actual_nrows, actual_ncols

    def pprint(self, strings, file=None):
        """
        Pretty print list of strings like BSD ``ls``.

        :param strings: list of strings
        :param file: file handle to which to print, default to stdout
        """
        assert self.total_width >= 1, self.total_width
        assert self.width_between_cols >= 1, self.width_between_cols

        # to support pandas.Series, numpy.ndarray, etc.
        # pylint: disable=use-implicit-booleaness-not-len
        if not len(strings):
            return

        column_width = max(map(cjkjust.cjklen, strings))
        nrows, ncols = self.calc_layout(len(strings), column_width)
        columns = [[] for _ in range(ncols)]
        for i, s in enumerate(strings):
            columns[i // nrows].append(s)

        for row in itertools.zip_longest(*columns):
            padded_row = (cjkjust.cjkljust(s or '', column_width) for s in row)
            print((' ' * self.width_between_cols).join(padded_row), file=file)


class GNUFormatter:
    """
    The quoting property, which print ``"hello"`` as ``'"hello"'`` and
    ``hello world`` as ``'hello world'``, is omitted. Moreover, since GNU-style
    is quite sophisticated, the actual print-out might not look exactly the
    same as GNU ``ls``.

    Warning: Tab in strings ruins the print-out.
    """
    def __init__(self, total_width=None, width_between_cols=2):
        """
        :param total_width: the disposable total width, default to terminal
               width
        :param width_between_cols: width between columns, default to 2
        """
        self.total_width = total_width or shutil.get_terminal_size().columns
        self.width_between_cols = width_between_cols

    def try_layout(self, strings, expected_ncols):
        n_strings = len(strings)
        #assert 1 <= expected_ncols <= n_strings, expected_ncols

        nrows = math.ceil(n_strings / expected_ncols)
        ncols = (n_strings - 1) // nrows + 1

        columns = [[] for _ in range(ncols)]
        for i, s in enumerate(strings):
            columns[i // nrows].append(s)
        column_widths = [max(map(cjkjust.cjklen, c)) for c in columns]
        width = sum(column_widths) + (ncols - 1) * self.width_between_cols

        if width <= self.total_width:
            return columns, column_widths
        return None

    def pprint(self, strings, file=None):
        """
        Pretty print list of strings like GNU ``ls``.

        :param strings: list of strings
        :param file: file handle to which to print, default to stdout
        """
        assert self.total_width >= 1, self.total_width
        assert self.width_between_cols >= 1, self.width_between_cols

        # to support pandas.Series, numpy.ndarray, etc.
        # pylint: disable=use-implicit-booleaness-not-len
        if not len(strings):
            return

        # find the maximum possible `expected_ncols`
        last_valid_layout = None
        for expected_ncols in range(1, len(strings) + 1):
            layout = self.try_layout(strings, expected_ncols)
            if not layout:
                break
            last_valid_layout = layout
        if not last_valid_layout:
            # set `expected_ncols` to 1
            last_valid_layout = [strings], [max(map(cjkjust.cjklen, strings))]

        columns, column_widths = last_valid_layout
        for row in itertools.zip_longest(*columns):
            padded_row = [
                cjkjust.cjkljust(s or '', w)
                for s, w in zip(row, column_widths)
            ]
            print((' ' * self.width_between_cols).join(padded_row), file=file)


def pprint(strings, total_width=None, style='BSD', file=None):
    """
    Pretty print list of strings like ``ls``.

    :param strings: list of strings
    :param total_width: the disposable total width, default to terminal width
    :param style: either 'BSD' or 'GNU', default to 'BSD'
    :param file: file handle to which to print, default to stdout
    """
    style = style.lower()
    if style == 'bsd':
        fmt = BSDFormatter(total_width)
    elif style == 'gnu':
        fmt = GNUFormatter(total_width)
    else:
        raise ValueError('illegal style "{}"'.format(style))
    fmt.pprint(strings, file=file)
