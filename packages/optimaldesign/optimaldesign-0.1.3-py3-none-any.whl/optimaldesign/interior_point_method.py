import jax.numpy as np
from typing import List, Optional, Any, Tuple
from pydantic import BaseModel
import jax.scipy as sp
from jax import jit
from abc import ABC, abstractmethod
from functools import partial


class JaxBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class FunctionTarget(ABC):
    weight: np.float64 = 1.0

    @classmethod
    @abstractmethod
    def set_constants(self, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def compute(self, x) -> Tuple[np.float64, np.ndarray, np.ndarray]:
        pass


class FunctionTargetSupp(ABC):
    weight: np.float64 = 1.0

    @classmethod
    @abstractmethod
    def set_constants(self, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def compute(self, x) -> Tuple[np.float64, np.ndarray]:
        pass


class HelperVoronoiTarget(FunctionTarget):
    def set_constants(self, supp, x_id):
        diff: np.ndarray = 2 * (np.array([supp[x_id]]) - supp)

        supp_col_wise_squared_norm = np.power(np.linalg.norm(supp, axis=1, ord=2), 2)
        squared_norm_diff: np.ndarray = (
            supp_col_wise_squared_norm[x_id] - supp_col_wise_squared_norm
        )

        self.supp = supp
        self.x_id = x_id
        self.diff = diff
        self.squared_norm_diff = squared_norm_diff

    @partial(jit, static_argnums=(0,))
    def compute(self, x):
        tmp_f: np.ndarray = self.squared_norm_diff - np.dot(x, self.diff.T)
        tmp_f = tmp_f.at[self.x_id].set(-1)
        tmp: np.ndarray = self.diff / np.array([tmp_f]).T

        value = -np.sum(np.log(-tmp_f))
        gradient = np.sum(tmp, axis=0)
        hessian = np.dot(tmp.T, tmp)

        return value, gradient, hessian


class NLPSolverPrecision(JaxBaseModel):
    barrier: float = 1e-8
    newton: float = 1e-8


class NLPSolverMaxIter(JaxBaseModel):
    barrier: int = int(1e3)
    backline: int = int(4e1)
    newton: int = int(1e3)


class NLPSolverBarrier(JaxBaseModel):
    mu: float = 5
    t0: float = 100


class NLPSolverBackline(JaxBaseModel):
    a: float = 0.2
    b: float = 0.1


class NLPSolverOption(JaxBaseModel):
    prec: NLPSolverPrecision = NLPSolverPrecision()
    max_iter: NLPSolverMaxIter = NLPSolverMaxIter()
    barrier: NLPSolverBarrier = NLPSolverBarrier()
    backline: NLPSolverBackline = NLPSolverBackline()


class NLPMinimizeBound(JaxBaseModel):
    lower: np.ndarray
    upper: np.ndarray


class NLPMinimizeLinearEqualityConstraint(JaxBaseModel):
    mat: Optional[np.ndarray]
    newton_constr_mat: Optional[np.ndarray]
    enabled: bool = False


class NLPMinimizeInequalityConstraint(JaxBaseModel):
    use_template: str = "none"
    func: Optional[FunctionTarget]
    result_value: Optional[np.float64]
    result_gradient: Optional[np.ndarray]
    result_hessian: Optional[np.ndarray]
    enabled: bool = False
    voronoi_supp: Optional[np.ndarray]
    voronoi_x_id: Optional[Any]


class NLPMinimizeOption(JaxBaseModel):
    x0: np.ndarray
    bound_x: NLPMinimizeBound
    lin_equal_constr: NLPMinimizeLinearEqualityConstraint
    inequal_constr: NLPMinimizeInequalityConstraint


class NLPFunction:
    def __init__(self):
        self.nlp_targets: List[FunctionTarget] = []

    def add_target(self, function_target: FunctionTarget):
        self.nlp_targets.append(function_target)

    @partial(jit, static_argnums=(0,))
    def set_x(self, x):
        x_size: int = x.shape[0]
        value: np.float64 = 0.0
        gradient: np.ndarray = np.zeros(x_size)
        hessian: np.ndarray = np.zeros((x_size, x_size))
        for nlp_target in self.nlp_targets:
            (
                nlp_target_value,
                nlp_target_gradient,
                nlp_target_hessian,
            ) = nlp_target.compute(x)
            value += nlp_target.weight * nlp_target_value
            gradient += nlp_target.weight * nlp_target_gradient
            hessian += nlp_target.weight * nlp_target_hessian
        return value, gradient, hessian


class NLPFunctionSupp:
    def __init__(self):
        self.nlp_targets: List[FunctionTargetSupp] = []

    def add_target(self, function_target: FunctionTargetSupp):
        self.nlp_targets.append(function_target)

    @partial(jit, static_argnums=(0,), backend="cpu")
    def set_x(self, x):
        x_size: int = x.shape[0]
        value: np.float64 = 0.0
        gradient: np.ndarray = np.zeros(x_size)
        for nlp_target in self.nlp_targets:
            (
                nlp_target_value,
                nlp_target_gradient,
            ) = nlp_target.compute(x)
            value += nlp_target.weight * nlp_target_value
            gradient += nlp_target.weight * nlp_target_gradient
        return value, gradient


class NLPSolver:
    option: NLPSolverOption
    minimize_option: NLPMinimizeOption

    def __init__(self, func: NLPFunction, option: NLPSolverOption):
        self.func: NLPFunction = func
        self.option = option

    def minimize(self, minimize_option: NLPMinimizeOption):
        self.minimize_option = minimize_option

        if self.minimize_option.lin_equal_constr.enabled:
            self.pre_build_newton_linear_constraint_matrix()
        self.minimize_option.inequal_constr.enabled = True

        x_opt = self.barrier_method()
        return x_opt

    def barrier_method(self):
        x = self.minimize_option.x0
        x_size: int = x.shape[0]
        self.option.barrier.t0 = max(2e2, min(self.option.barrier.t0 * np.sqrt(x_size), 5e3))
        t = self.option.barrier.t0
        i = 0
        while i < self.option.max_iter.barrier and x_size / t >= self.option.prec.barrier:
            i += 1
            x = self.newton_method(x, t)
            t *= self.option.barrier.mu
        return x

    def newton_method(self, x, t):
        x_size = x.shape[0]
        iter_barrier: int = t / self.option.barrier.t0 / self.option.barrier.mu

        A: np.ndarray
        b: np.ndarray
        delta_x: np.ndarray

        if self.minimize_option.lin_equal_constr.enabled:
            A = self.minimize_option.lin_equal_constr.newton_constr_mat
        else:
            A = np.zeros((x_size, x_size))

        b = np.zeros(A.shape[0])

        i: int = 0
        crit: np.float64 = np.finfo(np.float64).max
        backline_exceeded: bool = False

        func_val, func_grad, func_hes = self.func.set_x(x)

        while (
            i < self.option.max_iter.newton
            and crit >= self.option.prec.newton * max(1.0, 1e4 * np.power(2, -iter_barrier))
            and not backline_exceeded
        ):
            i += 1
            # condition inequality constraints
            if self.minimize_option.lin_equal_constr.enabled:
                A = A.at[:x_size, :x_size].set(t * func_hes)
                b = b.at[:x_size].set(-t * func_grad)
                if self.minimize_option.inequal_constr.enabled:
                    (
                        inequal_constr_val,
                        inequal_constr_grad,
                        inequal_constr_hessian,
                    ) = self.compute_log_barrier_function(x)
                    A = A.at[:x_size, :x_size].add(inequal_constr_hessian)
                    b = b.at[:x_size].add(-inequal_constr_grad)
                delta_x = sp.linalg.lu_solve(sp.linalg.lu_factor(A), b)[:x_size]
            else:
                A = t * func_hes
                b = -t * func_grad
                if self.minimize_option.inequal_constr.enabled:
                    (
                        inequal_constr_val,
                        inequal_constr_grad,
                        inequal_constr_hessian,
                    ) = self.compute_log_barrier_function(x)
                    A += inequal_constr_hessian
                    b -= inequal_constr_grad
                delta_x = sp.linalg.lu_solve(sp.linalg.lu_factor(A), b)
            # criterion
            crit = np.linalg.norm(delta_x)
            x, backline_exceeded, func_val, func_grad, func_hes = self.backline_search(
                x, delta_x, func_val
            )
        return x

    def backline_search(self, x, delta_x, old_func_val):
        backline_exceeded: bool = False
        # normalize delta_x if norm > 1
        delta_x_norm = np.linalg.norm(delta_x)
        if delta_x_norm > 1:
            delta_x /= delta_x_norm
        a: np.float64 = self.option.backline.a
        i: int = 0
        search: bool = True
        x_tmp: np.ndarray
        while i < self.option.max_iter.backline and search:
            i += 1
            x_tmp = x + a * delta_x
            new_func_val, new_func_grad, new_func_hes = self.func.set_x(x_tmp)
            if new_func_val < old_func_val and self.feasibility_check(x_tmp):
                search = False
                x = x_tmp
            a *= self.option.backline.b
        if i >= self.option.max_iter.backline:
            backline_exceeded = True
        return x, backline_exceeded, new_func_val, new_func_grad, new_func_hes

    def pre_build_newton_linear_constraint_matrix(self):
        x_size: int = self.minimize_option.x0.shape[0]
        mat_rows: int = self.minimize_option.lin_equal_constr.mat.shape[0]
        newton_mat_size: int = x_size + mat_rows
        newton_constraint_mat: np.ndarray = np.zeros((newton_mat_size, newton_mat_size))
        newton_constraint_mat = newton_constraint_mat.at[x_size:newton_mat_size, 0:x_size].set(
            self.minimize_option.lin_equal_constr.mat
        )
        newton_constraint_mat = newton_constraint_mat.at[:x_size, x_size:newton_mat_size].set(
            self.minimize_option.lin_equal_constr.mat.T
        )
        self.minimize_option.lin_equal_constr.newton_constr_mat = newton_constraint_mat

    @partial(jit, static_argnums=(0,))
    def compute_log_barrier_function(self, x):
        x_size: int = x.shape[0]
        value: np.float64 = 0.0
        gradient: np.ndarray = np.zeros(x_size)
        hessian: np.ndarray = np.zeros((x_size, x_size))
        if self.minimize_option.bound_x:
            x_l = self.minimize_option.bound_x.lower
            x_u = self.minimize_option.bound_x.upper
            # value
            value -= np.sum(np.log(x_u - x) + np.log(x - x_l))
            # gradient
            gradient += 1.0 / (x_u - x) + 1 / (x_l - x)
            # hessian
            hessian += np.diag(1 / np.power(x_u - x, 2) + 1 / np.power(x_l - x, 2))
        if "custom" == self.minimize_option.inequal_constr.use_template:
            (
                func_val,
                func_grad,
                func_hes,
            ) = self.minimize_option.inequal_constr.func.set_x(x)
            value -= np.log(-func_val)
            gradient -= 1.0 / func_val * func_grad
            hessian += 1 / np.power(func_val, 2) * func_grad * func_grad.T - 1 / func_val * func_hes
        elif "voronoi" == self.minimize_option.inequal_constr.use_template:
            helper_voronoi_target = HelperVoronoiTarget()
            helper_voronoi_target.set_constants(
                supp=self.minimize_option.inequal_constr.voronoi_supp,
                x_id=self.minimize_option.inequal_constr.voronoi_x_id,
            )
            (
                helper_voronoi_result_value,
                helper_voronoi_result_gradient,
                helper_voronoi_result_hessian,
            ) = helper_voronoi_target.compute(x)
            value += helper_voronoi_result_value
            gradient += helper_voronoi_result_gradient
            hessian += helper_voronoi_result_hessian

        return value, gradient, hessian

    def feasibility_check(self, x) -> bool:
        check: bool = True
        if (
            np.amin(x - self.minimize_option.bound_x.lower) < 0
            or np.amax(x - self.minimize_option.bound_x.upper) > 0
        ):
            check = False
        return check
