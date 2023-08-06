from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.padding import Padding

def get_table_choice(console: Console, w: int, has_next: bool, extra={}) -> str:
    options = ['[P]rev', '[E]xit']
    basic_choice = ['p', 'e']
    if has_next:
        options.append('[N]ext')
    if extra:
        extra_choices = list(extra.keys())
        basic_choice.extend(extra_choices)
        for key in extra_choices:
            options.append(extra[key])

    max_opt_len = 0
    for index, val in enumerate(options):
        max_opt_len = max(max_opt_len, len(val))
        options[index] =  "[bright_green]" + val

    # console.width is console width of charater
    # one character space for panel outline , two space for column padding
    column_width = int(console.width / 2) - 3
    padding_width = int((column_width - max_opt_len) / 2)

    cols = []
    for option in options:
        cols.append(Padding(option, (0, padding_width)))

    p = Panel.fit(Columns(cols, width=column_width))
    console.print(p, justify='center')

    while True:
        choice = console.input('[green]navigate to: ')
        if choice.lower() in basic_choice:
            return choice.lower()
        elif has_next and choice.lower() in ['n']:
            return choice.lower()
