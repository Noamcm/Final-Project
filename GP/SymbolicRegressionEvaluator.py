import numpy as np
import pandas as pd
from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator

def _target_func(x, y, z):
    return x + 2 * y + 3 * z

class SymbolicRegressionEvaluator2(SimpleIndividualEvaluator):
    """
    Compute the fitness of an individual.
    """

    def __init__(self):
        super().__init__()

        # np.random.seed(0)

        data = np.random.uniform(-100, 100, size=(200, 3))
        self.df = pd.DataFrame(data, columns=['x', 'y', 'z'])
        self.df['target'] = _target_func(self.df['x'], self.df['y'], self.df['z'])

    def _evaluate_individual(self, individual):
        x, y, z = self.df['x'], self.df['y'], self.df['z']
        return np.mean(np.abs(individual.execute(x=x, y=y, z=z) - self.df['target']))