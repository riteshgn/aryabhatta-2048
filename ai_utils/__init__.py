
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def print_grid(state, digits_in_max_score=4):
    grid = state['grid']['cells']
    grid_transpose = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

    total_chars_with_spacing = digits_in_max_score + 2
    grid_to_print = ['|'.join([' %s ' % str(cell.get('value', 0)).zfill(digits_in_max_score)
                               if cell is not None else ' ' * total_chars_with_spacing for cell in row])
                     for row in grid_transpose]
    border = ' %s' % (' '.join(['%s' % '-' * total_chars_with_spacing] * digits_in_max_score))
    cell_separator = '|'

    print(border)
    for row in grid_to_print:
        print('%s%s%s' % (cell_separator, row, cell_separator))
        print(border)
