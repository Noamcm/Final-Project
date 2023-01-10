import math
import matplotlib as plt
import numpy as np
import sns as sns


def from_array(self, array):
    self.size = int((1 + math.sqrt(len(array) * 8 + 1)) / 2)
    self.ids = list(range(self.size))
    self.matrix = np.ones((self.size, self.size)) * -2
    self.array = array
    index = 0
    counter_c = 0
    counter_z = 0
    for i in range(self.size):
        for j in range(self.size):
            if i >= j:
                self.matrix[i][j] = -2
                counter_z += 1
            else:
                self.matrix[i][j] = array[index]
                if array[index] == 0:
                    counter_c += 1
                if array[index] == -1:
                    counter_z += 1
                index = index + 1
    self.percent = ((100.0 * counter_c) / (self.size * self.size - counter_z))

    def to_array(self):
        arr = np.array(self.matrix.flatten())

    self.array = np.delete(arr, np.where(arr == -2))


def figure_collision_matrix(self, file_path: str, title: str):
    plt.suptitle(title)
    collision_colors = ('#f0f5f5', '#c1d7d7', '#003300', '#33cccc')
    cmap = LinearSegmentedColormap.from_list('Custom', collision_colors, len(collision_colors))
    ax = sns.heatmap(self.matrix, cbar=True, cmap=cmap)
    colorbar = ax.collections[0].colorbar
    colorbar.set_ticks([-1.5, -0.75, 0, 0.75])
    colorbar.set_ticklabels(['symmetry unnecessary', 'same source and destination', 'collision', 'no collision'])

    plt.savefig(f"{file_path}_collision_matrix.png", bbox_inches='tight')

    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()