import math
import pickle
import random
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

import AntColony
import GA
import GA_WorstOut
import GA_deap
import GA_Worstout_ECkity
import GA_DEAP_Best_In
import SimpleGreedy
import Naive
import time


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

        # Easy
        elif self.difficulty == "Easy0.9_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 10, 10, 0.9
        elif self.difficulty == "Easy0.7_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 10, 10, 0.7
        elif self.difficulty == "Easy0.5_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 10, 10, 0.5

        # Medium
        elif self.difficulty == "Medium0.9_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 20, 20, 0.9
        elif self.difficulty == "Medium0.7_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 20, 20, 0.7
        elif self.difficulty == "Medium0.5_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 20, 20, 0.5

        # Hard
        elif self.difficulty == "Hard0.95_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 30, 30, 0.95
        elif self.difficulty == "Hard0.9_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 30, 30, 0.9
        elif self.difficulty == "Hard0.7_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 30, 30, 0.7
        elif self.difficulty == "Hard0.5_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 30, 30, 0.5

        # Large
        elif self.difficulty == "Large0.95_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 60, 30, 0.95
        elif self.difficulty == "Large0.9_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 60, 30, 0.9
        elif self.difficulty == "Large0.7_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 60, 30, 0.7
        elif self.difficulty == "Large0.5_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 60, 30, 0.5


        elif self.difficulty == "AI_Medium":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 15, 15, 0.8
        elif self.difficulty == "AI_Hard":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 20, 20, 0.7
        elif self.difficulty == "AI_VeryHard":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 30, 30, 0.8
        else:
            print("please insert one of the following: \"easy\" / \"medium\" / \"hard\"")
            return

    def create_data(self, index):
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
        np.savetxt("writtenData/" + self.difficulty + str(index) + ".txt", self.matrix, delimiter=",", fmt="%d")
        return

    def write_dict_data(self):
        for i in range(self.num_of_job_types):
            self.type_empID_dict[i] = list(
                np.arange(i * self.num_of_employees, i * self.num_of_employees + self.num_of_employees, 1, int))
        f = open("typeDictData/" + self.difficulty + ".pkl", "wb")
        pickle.dump(self.type_empID_dict, f)
        f.close()
        return self.type_empID_dict

    def read_data(self, index):
        try:
            self.matrix = np.loadtxt("writtenData/" + self.difficulty + str(index) + ".txt", delimiter=",").astype(
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
        ax = sns.heatmap(self.matrix, cbar=True, cmap=cmap)
        colorbar = ax.collections[0].colorbar
        colorbar.set_ticks([-1.625, -0.875, -0.125, 0.625])
        colorbar.set_ticklabels(["Symmetry\nunnecessary", "Same job type", "Not friends", "Friends"])
        plt.plot([], [], ' ', label='Types: ' + str(self.num_of_job_types)+'\n' + 'Employees: ' + str(self.num_of_employees)+ '\n' + 'Friendship pct: '+ str(int(self.friendship_percentage*100))+'%')
        plt.legend(loc=3)
        plt.savefig("drawnData/" + self.difficulty + ".png", bbox_inches="tight")
        #plt.show()
        plt.clf()
        plt.figure().clear()
        plt.close()

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
        edge_colors = ["tab:red" if e in pairs else "black" for e in self.G.edges()]
        node_colors = ["tab:green" if n in self.solution else "tab:blue" for n in self.G.nodes()]
        options = {"linewidths": 0.01}
        nx.draw_networkx(self.G, nodelist=list(self.G.nodes()), edge_color=edge_colors,node_color=node_colors, **options)
        plt.suptitle(self.difficulty + " graph", fontsize=20)
        ColorLegend = {'Friends': 'black', 'Solution': 'red'}
        f = plt.figure(1)
        ax = f.add_subplot(1, 1, 1)
        for label in ColorLegend:
            ax.plot([0], [0], color=ColorLegend[label], label=label)
        plt.axis('off')
        f.set_facecolor('w')

        plt.plot([], [], ' ', label='Types: ' + str(self.num_of_job_types)+'\n' + 'Employees: ' + str(self.num_of_employees)+ '\n' + 'Friendship pct: '+ str(int(self.friendship_percentage*100))+'%'+ '\n' + 'Solution size: '+ str(len(self.solution)))
        lines = plt.gca().get_lines()

        legend1 = plt.legend([lines[0],lines[1]],[lines[0].get_label(),lines[1].get_label()],loc=1)
        plt.legend([lines[2]],[lines[2].get_label()],loc=4)
        plt.gca().add_artist(legend1)

        plt.savefig("graphData/" + self.difficulty + ".png", bbox_inches="tight")

        #plt.show()
        plt.clf()
        plt.figure().clear()
        plt.close()

    def main(self, level_name, algo_types, num_of_files):
        sol_length = {}
        run_time = {}
        for a in algo_types:
            sol_length[a] = []
            run_time[a] = []
        for i in range(num_of_files):
            self.create_data(i)
            self.read_data(i)

            if self.matrix.any():
                self.figure_collision_matrix()
                self.G = self.to_graph()

                for algoType in algo_types:
                    # get the start time
                    st = time.time()

                    match algoType:
                        case "Greedy":
                            # Greedy
                            sol = SimpleGreedy.solve(self.G, self.type_empID_dict)

                        case "GA":
                            ga = GA.GA(self.G, self.type_empID_dict)
                            sol = ga.solve()
                            sol = [i for i in sol if i != -1]

                        # case "GA_GAD":
                        #     ga_gad = GA_GAD.GA_GAD(self.G, self.type_empID_dict)
                        #     sol = ga_gad.solve()
                        #     sol = [i for i in sol if i != -1]
                        case "GA_deap":
                            ga = GA_deap.GA_deap(self.G, self.type_empID_dict)
                            sol = ga.solve()
                            if sol:
                                sol = [i for i in sol if i != -1]

                        case "GA_DEAP_Best_In":
                            ga = GA_DEAP_Best_In.GA_DEAP_Best_In(self.G, self.type_empID_dict)
                            sol = ga.solve()
                            if sol:
                                sol = [i for i in sol if i != -1]

                        case "AntColony":
                            sol = AntColony.solve(self.G, self.type_empID_dict)

                        case "Naive":
                            sol = Naive.solve(self.G, self.type_empID_dict)
                        case "GA_WorstOut":
                            ga = GA_WorstOut.GA_WorstOut(self.G, self.type_empID_dict)
                            sol = ga.solve()
                            sol = [i for i in sol if i != -1]
                        case "GA_deap":
                            ga = GA_deap.GA_deap(self.G, self.type_empID_dict)
                            sol = ga.solve()
                            if sol:
                                sol = [i for i in sol if i != -1]
                        case "GA_Worstout_ECkity":
                            ga = GA_Worstout_ECkity.GA_Worstout_ECkity(self.G, self.type_empID_dict)
                            sol = ga.solve()
                            sol = [i for i in sol if i != -1]
                        case _:
                            sol = None

                    et = time.time()
                    print('algoType: ', algoType)
                    print('Execution time:', et - st, 'seconds')
                    print("***** Best Clique: " + str(sol) + " *****")
                    print("***** Solution length: " + str(len(sol)) + " *****")
                    run_time[algoType].append(et - st)
                    sol_length[algoType].append(len(sol))
                    self.solution = list(sol)
                # self.draw_graph()

        with open("results.txt", 'a') as f:
            f.write(str(level_name) + '\n\n')
        print(level_name)
        for algoType in algo_types:
            print("algoType: ", algoType)
            print("avg time: ", sum(run_time[algoType]) / len(run_time[algoType]))
            print("avg size: ", sum(sol_length[algoType]) / len(sol_length[algoType]))
            print()

            with open("results.txt", 'a') as f:
                f.write(
                    "algoType: " + str(algoType) + '\n'
                    "avg time: " + str(sum(run_time[algoType]) / len(run_time[algoType])) + '\n'
                    "avg size: " + str(sum(sol_length[algoType]) / len(sol_length[algoType])) + '\n\n'
                )

def writeMetaData(difficulty, num_of_job_types, num_of_employees, friendship_percentage):
    with open("metaData/" + difficulty + ".txt", 'w') as f:
        f.write(
            str(num_of_job_types) + "," + str(num_of_employees) + "," + str(friendship_percentage))


if __name__ == "__main__":
    levels = ["Easy0.9_", "Easy0.7_", "Easy0.5_",
              "Medium0.9_", "Medium0.7_", "Medium0.5_",
              "Hard0.9_", "Hard0.7_", "Hard0.5_"]
    # algorithms = ["Greedy", "AntColony", "Naive"]
    # levels = ["Large0.9_", "Large0.7_", "Large0.5_"]
    # levels = ["Medium0.9_", "Medium0.7_", "Medium0.5_"]
    # levels = ["Hard0.7_", "Hard0.5_", "Medium0.5_", "Medium0.7_"]
    # levels = ["Hard0.5_"]
    # levels = ["Medium0.7_"]
    algorithms = ["Greedy", "AntColony", "GA"]
    # algorithms = ["Greedy", "GA"]
    # algorithms = ["GA"]
    # algorithms = ["Naive"]
    # algorithms = ["Greedy"]
    # algorithms = ["AntColony"]
    # algorithms = ["GA_WorstOut"]
    # algorithms = ["GA_deap"]
    # algorithms = ["GA_DEAP_Best_In"]
    #algorithms = ["GA_Worstout_ECkity"]
    num_of_files = 20
    for level in levels:
        data = Data(level)  # Test/Easy/Medium/Hard
        data.main(level, algorithms, num_of_files)

