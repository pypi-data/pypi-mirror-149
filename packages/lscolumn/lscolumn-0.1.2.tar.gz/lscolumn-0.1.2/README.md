# lscolumn

Print a list of strings in columns like in `ls`.

## Description

Two styles are available -- BSD-style and GNU-style.
Let's see through example:

```
>>> import lscolumn
>>> lscolumn.pprint(['hello', 'hola world', 'greetings', 'hello again and again'],
...                 total_width=60, style='BSD')
hello                 greetings
hola world            hello again and again
>>> lscolumn.pprint(['hello', 'hola world', 'greetings', 'hello again and again'],
...                 total_width=60, style='GNU')
hello  hola world  greetings  hello again and again
```

In BSD-style, the widths of the columns are the same, whereas in GNU-style, they are different.
When formatting long list, BSD-style is faster than GNU-style, but GNU-style is more compact.

CJK (wide) characters are well supported thanks to [`cjkjust`](https://pypi.org/project/cjkjust/).

## Installation

```
pip install lscolumn
```

## Functions and Classes

For detailed help, try `help(...)` in Python REPL.

- `pprint(strings, total_width=None, style='BSD', file=None)`: print in columns the list of strings `strings`
- `BSDFormatter`: the BSD-style formatter (see example below)
- `GNUFormatter`: the GNU-style formatter (see example below)

## Example using `BSDFormatter`

```python
import lscolumn
bsd = lscolumn.BSDFormatter(total_width=80)
# print one list
bsd.pprint(['hello', 'hola world', 'greetings'])
# print another list using the same configuration
bsd.pprint(['greetings', 'hello again and again'])
# print yet another list to `outfile`
with open('filename.txt', 'w') as outfile:
    bsd.pprint(['hello', 'hola world'], file=outfile)
```

The same applies to `GNUFormatter`.
