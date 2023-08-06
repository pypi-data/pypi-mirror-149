from optimaldesign.linear_model import LinearModel
import jax.numpy as np
from jax import vmap, jit
from optimaldesign.interior_point_method import (
    NLPMinimizeLinearEqualityConstraint,
    NLPMinimizeInequalityConstraint,
    NLPMinimizeBound,
    NLPMinimizeOption,
    NLPSolverOption,
    NLPSolver,
    NLPFunction,
    NLPFunctionSupp,
)
from optimaldesign.design_measure import (
    DCritWeights,
    DCritSupp,
    CCritWeights,
    CCritSupp,
    CostCritWeights,
    CostCritSupp,
)
from typing import Callable, List
from functools import partial
from scipy.optimize import minimize
import multiprocessing as mp
from loguru import logger


class AdaptiveGridOptimalDesign:
    def __init__(
        self,
        linear_models: List[LinearModel],
        target_weights: List[np.float64],
        linear_models_cpu: List[LinearModel],
        design_x_u,
        design_x_l,
        grid_size,
        init_grid,
        cost_function: Callable,
        m: int = 1,
        optimality: str = "d",
        use_cost_function: bool = False,
        alpha_cost: np.float64 = 0.0,
        measured_supp: np.ndarray = np.array([]),
    ):
        self.linear_models = linear_models
        self.linear_models_cpu = linear_models_cpu
        self.design_x_u = design_x_u
        self.design_x_l = design_x_l
        self.optimality = optimality
        self.m = m
        self.use_cost_function = use_cost_function
        self.alpha_cost = alpha_cost
        self.cost_function = cost_function
        if use_cost_function:
            target_weights = (1.0 - alpha_cost) * target_weights
        self.target_weights = target_weights
        self.measured_supp = measured_supp
        self.grid_size = grid_size
        if measured_supp.shape[0] > 0:
            supp_distance = vmap(
                lambda x: np.linalg.norm(np.array([x]) - init_grid, axis=1, ord=2)
            )(measured_supp)
            add_measured_to_grid = np.all(supp_distance >= 1e-5, axis=1)
            init_grid = np.row_stack((init_grid, measured_supp[add_measured_to_grid]))
        self.init_grid = init_grid

    def _minimize_d_opt_weights(self, weights, supp):
        supp_size = supp.shape[0]
        minimize_option = NLPMinimizeOption(
            x0=weights,
            bound_x=NLPMinimizeBound(lower=np.zeros(supp_size), upper=np.ones(supp_size)),
            lin_equal_constr=NLPMinimizeLinearEqualityConstraint(
                mat=np.ones((1, supp_size)), enabled=True
            ),
            inequal_constr=NLPMinimizeInequalityConstraint(),
        )
        solver_option = NLPSolverOption()

        nlp_target = DCritWeights()
        nlp_target.weight = self.target_weights[0]
        nlp_target.set_constants(linear_model=self.linear_models[0], supp=supp)

        nlp_function = NLPFunction()
        nlp_function.add_target(function_target=nlp_target)

        if self.use_cost_function:
            nlp_target_cost = CostCritWeights()
            nlp_target_cost.weight = self.alpha_cost
            nlp_target_cost.set_constants(
                measured_supp=self.measured_supp,
                supp=supp,
                cost_function=self.cost_function,
            )
            nlp_function.add_target(function_target=nlp_target_cost)

        nlp_solver = NLPSolver(func=nlp_function, option=solver_option)

        weights = nlp_solver.minimize(minimize_option=minimize_option)

        return weights

    def _minimize_c_opt_weights(self, weights, supp):
        supp_size = supp.shape[0]
        minimize_option = NLPMinimizeOption(
            x0=weights,
            bound_x=NLPMinimizeBound(lower=np.zeros(supp_size), upper=np.ones(supp_size)),
            lin_equal_constr=NLPMinimizeLinearEqualityConstraint(
                mat=np.ones((1, supp_size)), enabled=True
            ),
            inequal_constr=NLPMinimizeInequalityConstraint(),
        )
        solver_option = NLPSolverOption()

        nlp_target = CCritWeights()
        nlp_target.weight = self.target_weights[0]
        nlp_target.set_constants(linear_model=self.linear_models[0], supp=supp, m=self.m)

        nlp_function = NLPFunction()
        nlp_function.add_target(function_target=nlp_target)

        if self.use_cost_function:
            nlp_target_cost = CostCritWeights()
            nlp_target_cost.weight = self.alpha_cost
            nlp_target_cost.set_constants(
                measured_supp=self.measured_supp,
                supp=supp,
                cost_function=self.cost_function,
            )
            nlp_function.add_target(function_target=nlp_target_cost)

        nlp_solver = NLPSolver(func=nlp_function, option=solver_option)

        weights = nlp_solver.minimize(minimize_option=minimize_option)

        return weights

    def _minimize_cd_opt_weights(self, weights, supp):
        supp_size = supp.shape[0]
        minimize_option = NLPMinimizeOption(
            x0=weights,
            bound_x=NLPMinimizeBound(lower=np.zeros(supp_size), upper=np.ones(supp_size)),
            lin_equal_constr=NLPMinimizeLinearEqualityConstraint(
                mat=np.ones((1, supp_size)), enabled=True
            ),
            inequal_constr=NLPMinimizeInequalityConstraint(),
        )
        solver_option = NLPSolverOption()

        nlp_target_d = DCritWeights()
        nlp_target_d.weight = self.target_weights[0]
        nlp_target_d.set_constants(linear_model=self.linear_models[0], supp=supp)

        nlp_target_c = CCritWeights()
        nlp_target_c.weight = self.target_weights[1]
        nlp_target_c.set_constants(linear_model=self.linear_models[1], supp=supp, m=self.m)

        nlp_function = NLPFunction()
        nlp_function.add_target(function_target=nlp_target_d)
        nlp_function.add_target(function_target=nlp_target_c)

        if self.use_cost_function:
            nlp_target_cost = CostCritWeights()
            nlp_target_cost.weight = self.alpha_cost
            nlp_target_cost.set_constants(
                measured_supp=self.measured_supp,
                supp=supp,
                cost_function=self.cost_function,
            )
            nlp_function.add_target(function_target=nlp_target_cost)

        nlp_solver = NLPSolver(func=nlp_function, option=solver_option)

        weights = nlp_solver.minimize(minimize_option=minimize_option)

        return weights

    def minimize_weights(self, weights, supp):
        if self.optimality == "d":
            weights = self._minimize_d_opt_weights(weights, supp)
            weights, supp = self.filter_design(weights, supp)
            weights = self._minimize_d_opt_weights(weights, supp)
        elif self.optimality == "c":
            weights = self._minimize_c_opt_weights(weights, supp)
            weights, supp = self.filter_design(weights, supp)
            weights = self._minimize_c_opt_weights(weights, supp)
        elif self.optimality == "cd":
            weights = self._minimize_cd_opt_weights(weights, supp)
            weights, supp = self.filter_design(weights, supp)
            weights = self._minimize_cd_opt_weights(weights, supp)
        return weights, supp

    def _minimize_d_opt_supp_idx(
        self,
        weights,
        supp,
        design_x_l,
        design_x_u,
        grid_size,
        target_weights,
        linear_models,
        use_cost_function,
        alpha_cost,
        measured_supp,
        cost_function,
        idx,
    ):
        x0 = supp[idx]

        if self._x_in_measured_supp(x0):
            return x0

        nlp_target = DCritSupp()
        nlp_target.weight = target_weights[0]
        nlp_target.set_constants(linear_model=linear_models[0], weights=weights, supp=supp)

        nlp_function = NLPFunctionSupp()
        nlp_function.add_target(function_target=nlp_target)

        if use_cost_function:
            weight = weights[idx]
            nlp_target_cost = CostCritSupp()
            nlp_target_cost.weight = alpha_cost
            nlp_target_cost.set_constants(
                measured_supp=measured_supp,
                weight=weight,
                cost_function=cost_function,
            )
            nlp_function.add_target(function_target=nlp_target_cost)

        def fun(x):
            return nlp_function.set_x(x)[0]

        def grad(x):
            return nlp_function.set_x(x)[1]

        # use voronoi constraints
        # def _voronoi_constr(x_i, x_j, x):
        #     return (
        #         np.dot(x, x_i - x_j)
        #         - np.linalg.norm(x_i) ** 2
        #         - np.linalg.norm(x_j) ** 2
        #     )

        # voronoi_constr = jit(_voronoi_constr, backend="cpu")

        # constr_list = []
        # for i in range(supp.shape[0]):
        #     if i != idx:
        #         constr_list.append(
        #             {"type": "ineq", "fun": lambda x: voronoi_constr(x0, supp[i], x)}
        #         )
        # constr = tuple(constr_list)

        bounds = tuple(
            [
                (
                    max(x_l, x0[idx] - 4 * grid_size[idx]),
                    min(x_u, x0[idx] + 4 * grid_size[idx]),
                )
                for idx, (x_l, x_u) in enumerate(zip(design_x_l, design_x_u))
            ]
        )

        min_result = minimize(
            fun,
            x0,
            jac=grad,
            # constraints=constr,
            bounds=bounds,
            method="SLSQP",
            options=dict(ftol=1e-8),
        )
        supp_x_idx = min_result.x

        return supp_x_idx

    def _minimize_c_opt_supp_idx(
        self,
        weights,
        supp,
        design_x_l,
        design_x_u,
        grid_size,
        target_weights,
        linear_models,
        m,
        use_cost_function,
        alpha_cost,
        measured_supp,
        cost_function,
        idx,
    ):
        x0 = supp[idx]

        if self._x_in_measured_supp(x0):
            return x0

        nlp_target = CCritSupp()
        nlp_target.weight = target_weights[0]
        nlp_target.set_constants(linear_model=linear_models[0], weights=weights, supp=supp, m=m)

        nlp_function = NLPFunctionSupp()
        nlp_function.add_target(function_target=nlp_target)

        if use_cost_function:
            weight = weights[idx]
            nlp_target_cost = CostCritSupp()
            nlp_target_cost.weight = alpha_cost
            nlp_target_cost.set_constants(
                measured_supp=measured_supp,
                weight=weight,
                cost_function=cost_function,
            )
            nlp_function.add_target(function_target=nlp_target_cost)

        def fun(x):
            return nlp_function.set_x(x)[0]

        def grad(x):
            return nlp_function.set_x(x)[1]

        bounds = tuple(
            [
                (max(x_l, x0[idx] - 4 * grid_size[idx]), min(x_u, x0[idx] + 4 * grid_size[idx]))
                for idx, (x_l, x_u) in enumerate(zip(design_x_l, design_x_u))
            ]
        )
        min_result = minimize(
            fun,
            x0,
            jac=grad,
            bounds=bounds,
            method="SLSQP",
            options=dict(ftol=1e-8),
        )
        supp_x_idx = min_result.x
        return supp_x_idx

    def _minimize_cd_opt_supp_idx(
        self,
        weights,
        supp,
        design_x_l,
        design_x_u,
        grid_size,
        target_weights,
        linear_models,
        m,
        use_cost_function,
        alpha_cost,
        measured_supp,
        cost_function,
        idx,
    ):
        x0 = supp[idx]

        if self._x_in_measured_supp(x0):
            return x0

        nlp_target_d = DCritSupp()
        nlp_target_d.weight = target_weights[0]
        nlp_target_d.set_constants(linear_model=linear_models[0], weights=weights, supp=supp)

        nlp_target_c = CCritSupp()
        nlp_target_c.weight = target_weights[1]
        nlp_target_c.set_constants(linear_model=linear_models[1], weights=weights, supp=supp, m=m)

        nlp_function = NLPFunctionSupp()
        nlp_function.add_target(function_target=nlp_target_d)
        nlp_function.add_target(function_target=nlp_target_c)

        if use_cost_function:
            weight = weights[idx]
            nlp_target_cost = CostCritSupp()
            nlp_target_cost.weight = alpha_cost
            nlp_target_cost.set_constants(
                measured_supp=measured_supp,
                weight=weight,
                cost_function=cost_function,
            )
            nlp_function.add_target(function_target=nlp_target_cost)

        def fun(x):
            return nlp_function.set_x(x)[0]

        def grad(x):
            return nlp_function.set_x(x)[1]

        bounds = tuple(
            [
                (
                    max(x_l, x0[idx] - 4 * grid_size[idx]),
                    min(x_u, x0[idx] + 4 * grid_size[idx]),
                )
                for idx, (x_l, x_u) in enumerate(zip(design_x_l, design_x_u))
            ]
        )

        min_result = minimize(
            fun,
            x0,
            jac=grad,
            bounds=bounds,
            method="SLSQP",
            options=dict(ftol=1e-8),
        )
        supp_x_idx = min_result.x
        return supp_x_idx

    def minimize_supp(self, weights, supp):
        if self.optimality == "d":
            supp_idx_solver = partial(
                self._minimize_d_opt_supp_idx,
                weights,
                supp,
                self.design_x_l,
                self.design_x_u,
                self.grid_size,
                self.target_weights,
                self.linear_models_cpu,
                self.use_cost_function,
                self.alpha_cost,
                self.measured_supp,
                self.cost_function,
            )
            pool = mp.Pool(processes=mp.cpu_count())
            supp_list = pool.map(supp_idx_solver, range(supp.shape[0]))
            pool.close()
            pool.join()

            supp = np.asarray(supp_list)
        elif self.optimality == "c":
            supp_idx_solver = partial(
                self._minimize_c_opt_supp_idx,
                weights,
                supp,
                self.design_x_l,
                self.design_x_u,
                self.grid_size,
                self.target_weights,
                self.linear_models_cpu,
                self.m,
                self.use_cost_function,
                self.alpha_cost,
                self.measured_supp,
                self.cost_function,
            )
            pool = mp.Pool(processes=mp.cpu_count())
            supp_list = pool.map(supp_idx_solver, range(supp.shape[0]))
            pool.close()
            pool.join()

            supp = np.asarray(supp_list)
        elif self.optimality == "cd":
            supp_idx_solver = partial(
                self._minimize_cd_opt_supp_idx,
                weights,
                supp,
                self.design_x_l,
                self.design_x_u,
                self.grid_size,
                self.target_weights,
                self.linear_models_cpu,
                self.m,
                self.use_cost_function,
                self.alpha_cost,
                self.measured_supp,
                self.cost_function,
            )
            pool = mp.Pool(processes=mp.cpu_count())
            supp_list = pool.map(supp_idx_solver, range(supp.shape[0]))
            pool.close()
            pool.join()

            supp = np.asarray(supp_list)
        return weights, supp

    def solve(self):
        i = 0
        distance_proof = True
        measure_proof = True
        supp = self.init_grid
        supp_size = supp.shape[0]
        weights = np.full(supp_size, 1.0 / float(supp_size))
        design_measure = self.design_measure(weights, supp)
        logger.debug(f"Iteration: start, Measure: {design_measure}, #Supp: {supp.shape[0]}")
        weights, supp = self.minimize_weights(weights, supp)
        design_measure = self.design_measure(weights, supp)
        logger.debug(f"Iteration: {i}, Measure: {design_measure}, #Supp: {supp.shape[0]}")
        while i < 100 and (distance_proof and measure_proof):
            i += 1
            old_weights, old_supp = weights, supp
            old_design_measure = design_measure
            weights, supp = self.minimize_supp(weights, supp)
            distance_supp = old_supp - supp
            distance_supp_norm = np.linalg.norm(distance_supp)
            weights, supp = self.collapse_design(weights, supp)

            weights, supp = self.minimize_weights(weights, supp)
            design_measure = self.design_measure(weights, supp)
            logger.debug(f"Iteration: {i}, Measure: {design_measure}, #Supp: {supp.shape[0]}")
            if np.abs(design_measure - old_design_measure) / old_design_measure < 1e-6:
                measure_proof = False
            elif np.isnan(design_measure) or distance_supp_norm < np.linalg.norm(supp) * 1e-6:
                weights, supp = old_weights, old_supp
                distance_proof = False
            elif old_design_measure <= design_measure and old_supp.shape[0] <= supp.shape[0]:
                measure_proof = False
                weights, supp = old_weights, old_supp
        design_measure = self.design_measure(weights, supp)
        logger.debug(f"Iteration: result, Measure: {design_measure}, #Supp: {supp.shape[0]}")
        return weights, supp

    def design_measure(self, weights, supp):
        if self.optimality == "d":
            nlp_target = DCritWeights()
            nlp_target.weight = self.target_weights[0]
            nlp_target.set_constants(linear_model=self.linear_models[0], supp=supp)

            nlp_function = NLPFunction()
            nlp_function.add_target(function_target=nlp_target)
            if self.use_cost_function:
                nlp_target_cost = CostCritWeights()
                nlp_target_cost.weight = self.alpha_cost
                nlp_target_cost.set_constants(
                    measured_supp=self.measured_supp,
                    supp=supp,
                    cost_function=self.cost_function,
                )
                nlp_function.add_target(function_target=nlp_target_cost)
            return nlp_function.set_x(weights)[0]
        elif self.optimality == "c":
            c_crit_weights = CCritWeights()
            c_crit_weights.weight = self.target_weights[0]
            c_crit_weights.set_constants(linear_model=self.linear_models[0], supp=supp, m=self.m)
            return c_crit_weights.compute(weights)[0]
        elif self.optimality == "cd":
            nlp_target_d = DCritWeights()
            nlp_target_d.weight = self.target_weights[0]
            nlp_target_d.set_constants(linear_model=self.linear_models[0], supp=supp)

            nlp_target_c = CCritWeights()
            nlp_target_c.weight = self.target_weights[1]
            nlp_target_c.set_constants(linear_model=self.linear_models[1], supp=supp, m=self.m)

            nlp_function = NLPFunction()
            nlp_function.add_target(function_target=nlp_target_d)
            nlp_function.add_target(function_target=nlp_target_c)
            return nlp_function.set_x(weights)[0]

    def filter_design(self, weights: np.ndarray, supp: np.ndarray):
        filter_design_idx = weights > 1e-4
        weights = weights[filter_design_idx]
        supp = supp[filter_design_idx]

        # normalize weights
        weights = self.normalize_weights(weights)
        return weights, supp

    def normalize_weights(self, weights):
        return weights / np.sum(weights)

    def collapse_design(self, weights, supp):
        supp_distance = vmap(lambda x: np.linalg.norm(np.array([x]) - supp, axis=1, ord=2))(supp)
        distance_cluster = supp_distance < 1e-4
        collapse_cluster = np.argmax(weights * distance_cluster, axis=1) == np.arange(
            weights.shape[0]
        )
        collapse_cluster_weights = np.sum(weights * distance_cluster, axis=1)[collapse_cluster]
        collapse_cluster_supp = supp[collapse_cluster]
        return collapse_cluster_weights, collapse_cluster_supp

    @partial(jit, static_argnums=(0,), backend="cpu")
    def _x_in_measured_supp(self, x):
        if self.measured_supp.shape[0] < 1:
            return False
        supp_distance = np.linalg.norm(np.array([x]) - self.measured_supp, axis=1, ord=2)
        distance_cluster = supp_distance < 1e-5
        return np.any(distance_cluster)
