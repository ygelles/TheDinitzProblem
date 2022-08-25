import random
import matplotlib.colors
import matplotlib.pyplot as plt
from matplotlib.table import Table
from stable_matching import find_stable_matching


class Grid:
    def __init__(self, colors):
        self.n = len(colors)
        self.colors = colors
        self.color_to_cell = dict()
        for row in colors:
            assert len(row) == self.n
        for i in range(self.n):
            for j in range(self.n):
                assert len(colors[i][j]) >= self.n
                for color in colors[i][j]:
                    if color not in self.color_to_cell:
                        self.color_to_cell[color] = set()
                    self.color_to_cell[color].add((i, j))

    def show(self):
        fig, ax = plt.subplots()
        ax.set_axis_off()
        tb = Table(ax, bbox=[0, 0, 1, 1])

        width, height = 1.0 / self.n, 1.0 / self.n

        color_to_number = {}
        number = 0
        for color in sorted(self.color_to_cell):
            if self.color_to_cell[color]:
                color_to_number[color] = number
                number += 1

        norm = matplotlib.colors.Normalize(vmin=0, vmax=len(color_to_number))
        cm = plt.get_cmap()
        # Add cells
        for i in range(self.n):
            for j in range(self.n):
                color = self.colors[i][j][0]
                tb.add_cell(i, j, width, height, text=color, loc='center', facecolor=cm(norm(color_to_number[color])))

        # Row Labels...
        for i in range(self.n):
            tb.add_cell(i, -1, width, height, text=(i + 1), loc='right', edgecolor='none', facecolor='none')
        # Column Labels...
        for j in range(self.n):
            tb.add_cell(-1, j, width, height / 2, text=(j + 1), loc='center', edgecolor='none', facecolor='none')
        ax.add_table(tb)
        plt.show()

    # since arbitrary "regular" coloring is needed we just set each cell color to be (i + j) mod n
    def solve(self):
        for color in self.color_to_cell:
            rows = []
            columns = []
            for _ in range(self.n):
                rows.append([])
                columns.append([])
            # add the cell value
            for (i, j) in self.color_to_cell[color]:
                rows[i].append((i + j) % self.n)
                columns[j].append((i + j) % self.n)
            # fix men ranking by sorting it according to the cell "regular" coloring
            for id, ranking in enumerate(rows):
                rows[id] = [(value - id) % self.n for value in sorted(ranking)]
            # fix women ranking by reverse sorting it according to the cell "regular" coloring
            for id, ranking in enumerate(columns):
                columns[id] = [(value - id) % self.n for value in reversed(sorted(ranking))]
            kernel = find_stable_matching(rows, columns)
            for i, j in kernel:
                self.__set_color(i, j, color)

    def __set_color(self, i, j, color):
        assert color in self.colors[i][j]
        for _color in self.colors[i][j]:
            if _color != color:
                self.color_to_cell[_color].remove((i, j))
        self.colors[i][j] = [color]


def generate_random_grid(n, num_of_colors):
    assert num_of_colors >= n
    colors = []
    for _ in range(n):
        colors.append([])
        for _ in range(n):
            colors[-1].append([])
            colors_set = set()
            while len(colors_set) < n:
                colors_set.add(random.randint(1, num_of_colors))
            colors[-1][-1] = list(colors_set)
    return colors


if __name__ == '__main__':
    colors = [[[1, 2], [2, 3]],
              [[1, 3], [2, 3]]]
    g = Grid(colors)
    g.solve()
    g.show()

    g = Grid(generate_random_grid(4, 24))
    g.solve()
    g.show()

    g = Grid(generate_random_grid(16, 160))
    g.solve()
    g.show()
