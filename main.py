import math
import time
import pickle
import random
import numpy as np
import networkx as nx
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from deap import tools

import Naive
import SimpleGreedy
import AntColony
import GA_Worst_out
import GA_Best_In
import WriteToCsv


class Data:

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.plantSolution = True
        self.matrix = None
        self.type_empID_dict = {}
        self.G = None
        self.solution = None

        # Easy
        if self.difficulty == "Easy_0.9":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 10, 10, 0.9
        elif self.difficulty == "Easy_0.7":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 10, 10, 0.7
        elif self.difficulty == "Easy_0.5":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 10, 10, 0.5

        # Medium
        elif self.difficulty == "Medium_0.9":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 20, 20, 0.9
        elif self.difficulty == "Medium_0.7":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 20, 20, 0.7
        elif self.difficulty == "Medium_0.5":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 20, 20, 0.5

        # Hard
        elif self.difficulty == "Hard0.95_":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 30, 30, 0.95
        elif self.difficulty == "Hard_0.9":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 30, 30, 0.9
        elif self.difficulty == "Hard_0.7":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 30, 30, 0.7
        elif self.difficulty == "Hard_0.5":
            self.num_of_job_types, self.num_of_employees, self.friendship_percentage = 30, 30, 0.5

        else:
            print("please insert one of the following: \"easy\" / \"medium\" / \"hard\"")
            return

        # algorithms data:
        self.population_sizes = [50,100,200,500]
        self.crossovers =[tools.cxUniform,tools.cxTwoPoint]

        self.LIST_N_ANTS = [20, 50, 100, 500]
        self.LIST_PHEROMONE_DEPOSIT =  [2, 5, 10, 50]
        self.LIST_EVAPORATION_RATE = [0.7, 0.9, 0.95]

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
        np.savetxt("Data/writtenData/" + self.difficulty + str(index) + ".txt", self.matrix, delimiter=",", fmt="%d")
        return

    def write_dict_data(self):
        for i in range(self.num_of_job_types):
            self.type_empID_dict[i] = list(
                np.arange(i * self.num_of_employees, i * self.num_of_employees + self.num_of_employees, 1, int))
        f = open("Data/typeDictData/" + self.difficulty + ".pkl", "wb")
        pickle.dump(self.type_empID_dict, f)
        f.close()
        return self.type_empID_dict

    def read_data(self, index):
        try:
            self.matrix = np.loadtxt("Data/writtenData/" + self.difficulty + str(index) + ".txt", delimiter=",").astype(
                int)  # reads as int instead float
            self.type_empID_dict = self.read_dict_data()
            self.read_meta_data()
        except OSError:
            print(f"File name Data/writtenData/ {self.difficulty,str(index)}  .txt does not exist")
        except Exception as e:
            print(e)
        return

    def read_dict_data(self):
        try:
            file_to_read = open("Data/typeDictData/" + self.difficulty + ".pkl", "rb")
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
        plt.savefig("Data/drawnData/" + self.difficulty + ".png", bbox_inches="tight")
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

        plt.savefig("Results/graphData/" + self.difficulty + ".png", bbox_inches="tight")

        plt.clf()
        plt.figure().clear()
        plt.close()

    def main(self, level_name, algo_types, num_of_files):
        sol_length = {}
        run_time = {}
        solutions={}
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
                    if algoType not in solutions:
                        solutions[algoType] = {}
                    # get the start time
                    st = time.time()

                    match algoType:
                        case "Naive":
                            sol = Naive.solve(self.G, self.type_empID_dict,level_name, algo_types)
                        case "Greedy":
                            sol = SimpleGreedy.solve(self.G, self.type_empID_dict)
                        case "AntColony":
                            for n_ants in self.LIST_N_ANTS:
                                for pheromone_deposit in self.LIST_PHEROMONE_DEPOSIT:
                                    for evaporation_rate in self.LIST_EVAPORATION_RATE:
                                        parameters=str(n_ants)+"_"+str(pheromone_deposit)+"_"+str(evaporation_rate)+"_"+level_name
                                        if parameters not in solutions[algoType]:
                                            solutions[algoType][parameters] = []
                                        ant_colony=AntColony.AntColony(self.G, self.type_empID_dict,level_name, algo_types,n_ants,pheromone_deposit,evaporation_rate)
                                        sol_len = calculate_length(ant_colony.solve())
                                        solutions[algoType][parameters].append(sol_len)
                                        print( algoType , parameters , sol_len)
                        case "GA_Worst_out":
                            for crossover in self.crossovers:
                                # Define the genetic operators
                                for population_size in self.population_sizes:
                                    parameters=str(crossover.__name__)+"_"+str(population_size)+"_"+level_name
                                    if parameters not in solutions[algoType]:
                                        solutions[algoType][parameters] = []
                                    ga = GA_Worst_out.GA_Worst_out(self.G, self.type_empID_dict,level_name, algo_types,crossover,population_size)
                                    solutions[algoType][parameters].append(calculate_length(ga.solve()))
                        case "GA_Best_In":
                            for population_size in self.population_sizes:
                                parameters = str(population_size) + "_" + level_name
                                if parameters not in solutions[algoType]:
                                    solutions[algoType][parameters] = []
                                ga = GA_Best_In.GA_Best_In(self.G, self.type_empID_dict, level_name, algo_types, population_size)
                                solutions[algoType][parameters].append(calculate_length(ga.solve()))
                        case _:
                            sol = None

                    et = time.time()
                    run_time[algoType].append(et - st)

        for algoType in solutions:
            for parameters in solutions[algoType]:
                solutions[algoType][parameters] =round(sum(solutions[algoType][parameters]) / len(solutions[algoType][parameters]), 2)

        WriteToCsv.write(solutions)


def writeMetaData(difficulty, num_of_job_types, num_of_employees, friendship_percentage):
    with open("Data/metaData/" + difficulty + ".txt", 'w') as f:
        f.write(
            str(num_of_job_types) + "," + str(num_of_employees) + "," + str(friendship_percentage))

def calculate_length(group):
    return len([i for i in group if i != -1])

if __name__ == "__main__":
    levels = ["Easy_0.9", "Easy_0.7", "Easy_0.5",
             "Medium_0.9", "Medium_0.7", "Medium_0.5",
             "Hard_0.9", "Hard_0.7", "Hard_0.5"]
    algorithms = ["Greedy", "Naive", "AntColony", "GA_Worst_out", "GA_Best_In"]
    num_of_files = 20
    for level in levels:
        data = Data(level)  # Test/Easy/Medium/Hard
        data.main(level, algorithms, num_of_files)

