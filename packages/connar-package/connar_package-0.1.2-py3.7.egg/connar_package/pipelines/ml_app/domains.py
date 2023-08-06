import numpy as np
import pandas as pd
from moosir_feature.model_validations.metrics import get_any_metric, binary_returns_avg_metric_fn
from sklearn.base import RegressorMixin

from geneticalgorithm import geneticalgorithm as ga
import pygad



class LarryConnarModel(RegressorMixin):
    def __init__(self, rsi_col: str, moving_average_col: str, ):
        self.moving_average_col = moving_average_col
        self.rsi_col = rsi_col
        self.rsi_threshold = 40.0
        self.ma_threshold = 0.0

    def fit(self, X=None, y=None):
        def fitness_func(solution, solution_idx):
            # print(X)
            rsi_threshold = solution[0]
            ma_threshold = solution[1]

            # predict X,
            X_temp = X.copy()
            X_temp["_pred"] = 0
            X_temp.loc[(X_temp[self.moving_average_col] + ma_threshold < X_temp["Close"]) & (
                    X_temp[self.rsi_col] < rsi_threshold), "_pred"] = 1

            # score
            score = binary_returns_avg_metric_fn(y_true=y, y_pred=X_temp["_pred"].values.reshape(-1))
            # print(score)


            return score



        # varbound = np.array([rsi_boundary, ma_boundary])

        sol_per_pop = 50
        num_genes = 2

        # rsi_boundary = [40, 50]
        # ma_boundary = [0, 200]
        init_range_low = 0
        init_range_high = 200

        mutation_percent_genes = 1

        num_generations = 70
        num_parents_mating = 30

        ga_instance = pygad.GA(num_generations=num_generations,
                               num_parents_mating=num_parents_mating,
                               fitness_func=fitness_func,
                               sol_per_pop=sol_per_pop,
                               num_genes=num_genes,
                               init_range_low=init_range_low,
                               init_range_high=init_range_high,
                               # mutation_percent_genes=mutation_percent_genes
                               )
        ga_instance.run()
        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        # solution = model.output_dict

        self.rsi_threshold = solution[0]
        self.ma_threshold = solution[1]

        # ga_instance.plot_result()
        print(solution)
        print(solution_fitness)

    def predict(self, X: pd.DataFrame):
        X["_temp"] = 0
        X.loc[(X[self.moving_average_col] + self.ma_threshold < X["Close"]) & (
                    X[self.rsi_col] < self.rsi_threshold), "_temp"] = 1

        vals = X["_temp"].values.reshape(-1)
        return vals

    def get_params(self, deep=False):
        return {'rsi_col': self.rsi_col,
                'moving_average_col': self.moving_average_col,
                }

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self













##########################################
#
#########################################
algorithm_parameters = {'max_num_iteration': None,
                        'population_size': 100,
                        'mutation_probability': 0.1,
                        'elit_ratio': 0.01,
                        'crossover_probability': 0.5,
                        'parents_portion': 0.3,
                        'crossover_type': 'uniform',
                        'max_iteration_without_improv': None}
convergence_curve = True


class LarryConnarModel2(RegressorMixin):
    def __init__(self, rsi_col: str, moving_average_col: str, ):
        self.moving_average_col = moving_average_col
        self.rsi_col = rsi_col
        self.rsi_threshold = 40.0
        self.ma_threshold = 0.0

    def fit(self, X=None, y=None):
        def f(X_params):
            # print(X)
            rsi_threshold = X_params[0]
            ma_threshold = X_params[1]

            # predict X,
            X_temp = X.copy()
            X_temp["_pred"] = 0
            X_temp.loc[(X_temp[self.moving_average_col] > X_temp["Close"] + ma_threshold) & (
                    X_temp[self.rsi_col] < rsi_threshold), "_pred"] = 1

            # score
            score = binary_returns_avg_metric_fn(y_true=y, y_pred=X_temp["_pred"].values.reshape(-1))
            # print(score)

            loss = -1 * score

            # by default the package minimize
            return loss

        rsi_boundary = [40, 50]
        ma_boundary = [0, 200]

        varbound = np.array([rsi_boundary, ma_boundary])

        model = ga(function=f,
                   dimension=2,
                   variable_type='real',
                   variable_boundaries=varbound,
                   algorithm_parameters=algorithm_parameters,
                   convergence_curve=convergence_curve)
        model.run()
        # convergence = model.report
        solution = model.output_dict
        best_vars = solution["variable"]

        self.rsi_threshold = best_vars[0]
        self.ma_threshold = best_vars[1]

        print(solution)
        pass

    def predict(self, X: pd.DataFrame):
        X["_temp"] = 0
        X.loc[(X[self.moving_average_col] > X["Close"] + self.ma_threshold) & (
                    X[self.rsi_col] < self.rsi_threshold), "_temp"] = 1

        vals = X["_temp"].values.reshape(-1)
        return vals

    def get_params(self, deep=False):
        return {'rsi_col': self.rsi_col,
                'moving_average_col': self.moving_average_col,
                }

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self
