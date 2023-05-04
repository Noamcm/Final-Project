import random
import numpy as np
from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.creators.ga_creators.bit_string_vector_creator import GABitStringVectorCreator
from eckity.creators.ga_creators.int_vector_creator import GAIntVectorCreator
from eckity.genetic_operators.crossovers.vector_k_point_crossover import VectorKPointsCrossover
from eckity.genetic_operators.mutations.vector_random_mutation import IntVectorNPointMutation
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation
from examples.vectorga.knapsack.knapsack_evaluator import KnapsackEvaluator, NUM_ITEMS

from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator


class GA_Worstout_ECkity:
    def __init__(self, graph, types_emp_id_dict):
        self.graph = graph
        self.types_emp_id_dict = types_emp_id_dict
        self.total_from_each_type = len(types_emp_id_dict[0])
        self.generations = 100
        self.POPULATION_SIZE = 300
        self.BEST_N_AMOUNT = 10
        self.population = []
        self.grades = []
        self.best_n_index = []
        self.best_sol = []

        self.algo = SimpleEvolution(
                Subpopulation(creators=GAIntVectorCreator(self.total_from_each_type),
                              population_size=10,
                              # user-defined fitness evaluation method
                              evaluator=KnapsackEvaluator(),
                              # maximization problem (fitness is sum of values), so higher fitness is better
                              higher_is_better=True,
                              # genetic operators sequence to be applied in each generation
                              operators_sequence=[
                                  VectorKPointsCrossover(probability=0.5, k=2),
                                  IntVectorNPointMutation(n=self.total_from_each_type//2)
                              ],
                              selection_methods=[
                                  # (selection method, selection probability) tuple
                                  (TournamentSelection(tournament_size=4, higher_is_better=True), 1)
                              ]),
                breeder=SimpleBreeder(),
                max_workers=1,
                max_generation=500,
                statistics=BestAverageWorstStatistics()
            )
        self.algo.evolve()
        print(self.algo.execute())



#
# class GAEvaluator(SimpleIndividualEvaluator):
#     """
#     Evaluator class for the Knapsack problem, responsible of defining a fitness evaluation method and evaluating it.
#     In this example, fitness is the total price of the knapsack
#
#     Attributes
#     -------
#     items: dict(int, tuple(int, float))
#         dictionary of (item id: (weights, prices)) of the items
#     """
#
#     def __init__(self, items=None, max_weight=30):
#         super().__init__()
#
#         if items is None:
#             # Generate ramdom items for the problem (keys=weights, values=values)
#             items = {i: (random.randint(1, 10), random.uniform(0, 100)) for i in range(NUM_ITEMS)}
#         elif type(items) == list:
#
#             for item in items:
#                 if type(item) is not tuple or type(item[0]) is not int \
#                         or (type(item[1]) is not int and type(item[1]) is not float):
#                     raise ValueError('Elements in items list must be tuples of (weight: int, price: int or float)')
#
#             # Convert items list to dictionary by adding item id
#             items = {i: items[i] for i in range(len(items))}
#         self.items = items
#         self.max_weight = max_weight
#
#     def evaluate_individual(self, individual):
#         """
#         Compute the fitness value of a given individual.
#
#         Parameters
#         ----------
#         individual: Vector
#             The individual to compute the fitness value for.
#
#         Returns
#         -------
#         float
#             The evaluated fitness value of the given individual.
#         """
#         weight, value = 0.0, 0.0
#         for i in range(individual.size()):
#             if individual.cell_value(i):
#                 weight += self.items[i][0]
#                 value += self.items[i][1]
#
#         # worse possible fitness is returned if the weight of the items exceeds the maximum weight of the bag
#         if weight > self.max_weight:
#             return -np.inf
#
#         # fitness value is the total value of the bag
#         return value