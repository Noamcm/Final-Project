import math
import pickle
import random
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import SimpleGreedy
import json

from itertools import product


class Data:

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.plantSolution = True
        self.matrix = None
        self.type_empID_dict = {}
        self.G = None
        self.solution = None
        if self.difficulty == "Easy":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 10, 10, 0.95
        elif self.difficulty == "Medium":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 30, 30, 0.8
        elif self.difficulty == "Hard":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 30, 100, 0.6
        elif self.difficulty == "Test":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 5, 5, 0.5
        else:
            print("please insert one of the following: \"easy\" / \"medium\" / \"hard\"")
            return

    def create_data(self):
        writeMetaData(self.difficulty, self.num_of_job_types, self.num_of_employees, self.friendship_percentage)
        self.type_empID_dict = self.write_dict_data()
        self.matrix = np.zeros(
            (self.num_of_job_types * self.num_of_employees, self.num_of_job_types * self.num_of_employees))

        possible_friends = []
        for i in range(self.num_of_job_types):
            for j in range(self.num_of_job_types):
                for k in range(self.num_of_employees):
                    for l in range(self.num_of_employees):
                        if j < i:
                            self.matrix[i * self.num_of_employees + k][j * self.num_of_employees + l] = -2
                        elif i == j:
                            self.matrix[i * self.num_of_employees + k][j * self.num_of_employees + l] = -1
                        elif j > i:
                            possible_friends.append((i * self.num_of_employees + k, j * self.num_of_employees + l))
        counter = 0
        amount_of_friends = ((math.pow(self.num_of_job_types * self.num_of_employees,
                                       2) - self.num_of_job_types * math.pow(
            self.num_of_employees, 2)) / 2) * self.friendship_percentage

        if (self.plantSolution):
            amount_of_friends -= self.num_of_job_types
            for i in range(0, self.num_of_job_types * self.num_of_employees, self.num_of_job_types):
                for j in range(i, self.num_of_job_types * self.num_of_employees, self.num_of_job_types):
                    if self.matrix[i][j] == 0:
                        self.matrix[i][j] = 1
        while counter < amount_of_friends:
            choice = random.choice(possible_friends)
            if self.matrix[choice[0]][choice[1]] == 0:
                self.matrix[choice[0]][choice[1]] = 1
                counter += 1
        np.savetxt("writtenData/" + self.difficulty + ".txt", self.matrix, delimiter=",", fmt="%d")
        return

    def write_dict_data(self):
        for i in range(self.num_of_job_types):
            self.type_empID_dict[i] = list(
                np.arange(i * self.num_of_employees, i * self.num_of_employees + self.num_of_employees, 1, int))
        f = open("typeDictData/" + self.difficulty + ".pkl", "wb")
        pickle.dump(self.type_empID_dict, f)
        f.close()
        return self.type_empID_dict

    def read_data(self):
        try:
            self.matrix = np.loadtxt("writtenData/" + self.difficulty + ".txt", delimiter=",").astype(
                int)  # reads as int instead float
            self.type_empID_dict = self.read_dict_data()
            self.read_meta_data()
        except OSError:
            print("File name does not exist")
        except Exception as e:
            print(e)
        return

    def read_dict_data(self):
        try:
            file_to_read = open("typeDictData/" + self.difficulty + ".pkl", "rb")
            self.type_empID_dict = pickle.load(file_to_read)
        except Exception as e:
            print("readDictData")
            print(e)
        return self.type_empID_dict

    def read_meta_data(self):
        try:
            with open("metaData/" + self.difficulty + ".txt", 'r') as f:
                txt = f.read()
                str_split = txt.split(",")
                self.num_of_job_types = int(str_split[0])
                self.num_of_employees = int(str_split[1])
                self.friendship_percentage = float(str_split[2])
        except Exception as e:
            print("readMetaData")
            print(e)
        return

    def figure_collision_matrix(self):
        plt.suptitle(self.difficulty, fontsize=20)
        colors = ("#f0f5f5", "#c1d7d7", "#003300", "#33cccc")
        cmap = LinearSegmentedColormap.from_list("Custom", colors, len(colors))
        ax = sns.heatmap(self.matrix, cbar=True, cmap=cmap,cbar_kws={"shrink": .75 , "anchor":(0,0)})
        colorbar = ax.collections[0].colorbar
        colorbar.set_ticks([-1.625, -0.875, -0.125, 0.625])
        colorbar.set_ticklabels(["Symmetry\nunnecessary", "Same job type", "Not friends", "Friends"])

        text = 'Types: ' + str(self.num_of_job_types)+'\n' + 'Employees: ' + str(self.num_of_employees)+ '\n' + 'Friendship pct: '+ str(int(self.friendship_percentage*100))+'%'
        props = dict(boxstyle='round', facecolor="#f0f5f5", alpha=0.5)
        plt.text(26, 3, text, fontsize=10, bbox=props)

        plt.savefig("drawnData/" + self.difficulty + ".png", bbox_inches="tight")
        plt.show()

    def to_graph(self):
        edges = (list(zip(*np.where(self.matrix == 1))))
        G = nx.Graph(edges)
        return G

    def draw_graph(self):
        pairs = []
        for idx, a in enumerate(self.solution):
            for b in self.solution[idx + 1:]:
                pairs.append((a, b))
                pairs.append((b, a))
        edge_colors = ["red" if e in pairs else "black" for e in self.G.edges()]
        options = {"linewidths": 0.01}
        nx.draw_networkx(self.G, nodelist=list(self.G.nodes()), edge_color=edge_colors, **options)
        plt.suptitle(self.difficulty + " graph")
        plt.savefig("graphData/" + self.difficulty + ".png", bbox_inches="tight")

        #plt.show()

    def main(self):
        #self.create_data()
        self.read_data()
        if self.matrix.any():
            self.figure_collision_matrix()
            #self.G = self.to_graph()
            #self.solution = SimpleGreedy.solve(self.G, self.type_empID_dict)
            #self.draw_graph()


def writeMetaData(difficulty, num_of_job_types, num_of_employees, friendship_percentage):
    with open("metaData/" + difficulty + ".txt", 'w') as f:
        f.write(
            str(num_of_job_types) + "," + str(num_of_employees) + "," + str(friendship_percentage))


if __name__ == "__main__":
    data = Data("Test")  # Test/Easy/Medium/Hard
    data.main()
