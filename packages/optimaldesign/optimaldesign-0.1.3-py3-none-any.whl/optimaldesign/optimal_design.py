from optimaldesign.linear_model import LinearModel, LinearModelCPU
from optimaldesign.adaptive_grid_optimal_design import AdaptiveGridOptimalDesign
import jax.numpy as np
from typing import Callable, List, Optional
import numpy
from loguru import logger
import sys


class OptimalDesign:
    weights: np.ndarray
    supp: np.ndarray

    def __init__(
        self,
        f: Callable,
        feature_size: int,
        x_u,
        x_l,
        x_q,
        cost_function: Optional[Callable] = None,
        selected_features: List = [],
        optimality: str = "d",
        m: int = 1,
        alpha: np.float64 = 0.5,
        use_cost_function: bool = False,
        alpha_cost: np.float64 = 0.0,
        measured_supp: np.ndarray = np.array([]),
        log_level: str = "WARNING",
    ):
        logger.remove()
        logger.add(sys.stderr, level=log_level.upper())
        self.f = f
        self.linear_model = LinearModel(f, feature_size, selected_features)
        self.linear_model_cpu = LinearModelCPU(f, feature_size, selected_features)
        self.design_x_u = x_u
        self.design_x_l = x_l
        self.design_x_q = x_q
        self.optimality = optimality
        self.m = m
        self.alpha = alpha
        self.use_cost_function = use_cost_function
        self.alpha_cost = alpha_cost
        self.cost_function = cost_function
        self.measured_supp = measured_supp
        self.grid_size = (x_u - x_l) / x_q

    def solve(self):
        init_grid = self._grid()

        if self.optimality in ["d", "c"]:
            agod = AdaptiveGridOptimalDesign(
                linear_models=[self.linear_model],
                linear_models_cpu=[self.linear_model_cpu],
                target_weights=np.array([1.0]),
                design_x_u=self.design_x_u,
                design_x_l=self.design_x_l,
                init_grid=init_grid,
                optimality=self.optimality,
                m=self.m,
                use_cost_function=self.use_cost_function,
                alpha_cost=self.alpha_cost,
                cost_function=self.cost_function,
                measured_supp=self.measured_supp,
                grid_size=self.grid_size,
            )
            result = agod.solve()
        elif self.optimality == "cd":
            agod = AdaptiveGridOptimalDesign(
                linear_models=[self.linear_model, self.linear_model],
                linear_models_cpu=[self.linear_model_cpu, self.linear_model_cpu],
                target_weights=np.array([self.alpha, 1.0 - self.alpha]),
                design_x_u=self.design_x_u,
                design_x_l=self.design_x_l,
                init_grid=init_grid,
                optimality=self.optimality,
                m=self.m,
                use_cost_function=self.use_cost_function,
                alpha_cost=self.alpha_cost,
                cost_function=self.cost_function,
                measured_supp=self.measured_supp,
                grid_size=self.grid_size,
            )
            result = agod.solve()
        return result

    def _grid(self):
        x_u = numpy.array(self.design_x_u)
        x_l = numpy.array(self.design_x_l)
        x_q = numpy.array(self.design_x_q)
        grid_dim = self.design_x_u.shape[0]
        grid_points_list = []

        def _generate_grid(grid_points_list, pos, d, point):
            dim = grid_dim
            if d < dim:
                delta_x = (x_u - x_l) / (x_q - 1.0)
                for i in range(x_q[d]):
                    point_d_value = x_l[d] + i * delta_x[d]
                    point[d] = point_d_value
                    pos[d] = i
                    _generate_grid(grid_points_list, pos.copy(), d + 1, point.copy())
            else:
                grid_points_list.append(point)

        _generate_grid(grid_points_list, numpy.zeros(grid_dim), 0, numpy.empty(grid_dim))

        grid_points = np.asarray(grid_points_list)
        return grid_points
