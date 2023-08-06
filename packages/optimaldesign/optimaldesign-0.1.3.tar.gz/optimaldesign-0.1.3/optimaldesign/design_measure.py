from optimaldesign.interior_point_method import FunctionTarget, FunctionTargetSupp
import jax.numpy as np
import jax.scipy as sp
from jax import jit, vmap, grad
from functools import partial


class DCritWeights(FunctionTarget):
    def set_constants(self, linear_model, supp):
        self.linear_model = linear_model
        self.design = linear_model.design(supp)
        self.supp = supp

    @partial(jit, static_argnums=(0,))
    def compute(self, weights):
        fim = self.linear_model.fim(weights, self.supp)
        phi = np.dot(
            self.design,
            sp.linalg.lu_solve(sp.linalg.lu_factor(fim), self.design.T),
        )
        det = np.linalg.det(fim)
        n = self.linear_model.selected_feature_size
        value = -np.log(det) / n
        gradient = -np.diag(phi) / n
        hessian = phi**2 / n
        return value, gradient, hessian


class DCritSupp(FunctionTargetSupp):
    def set_constants(self, linear_model, weights, supp):
        self.linear_model = linear_model
        self.fim = linear_model.fim(weights, supp)

    @partial(jit, static_argnums=(0,), backend="cpu")
    def compute(self, x):
        feature_vec = self.linear_model.feature_vec(x)
        inv_fim_design = sp.linalg.lu_solve(sp.linalg.lu_factor(self.fim), feature_vec)
        jac = self.linear_model.jac(x)
        n = self.linear_model.selected_feature_size
        value = -np.dot(feature_vec, inv_fim_design) / n
        gradient = -2 * np.dot(jac.T, inv_fim_design) / n

        return value, gradient


class CCritWeights(FunctionTarget):
    def set_constants(self, linear_model, supp, m):
        self.linear_model = linear_model
        self.design = linear_model.design(supp)
        self.supp = supp
        self.m = m

    @partial(jit, static_argnums=(0,))
    def compute(self, weights):
        feat_size = self.linear_model.selected_feature_size
        fim = self.linear_model.fim(weights, self.supp)

        e_n = np.ones(feat_size)
        offset = feat_size - self.m
        e_n = e_n.at[:offset].set(0)
        fim_e_n = sp.linalg.lu_solve(sp.linalg.lu_factor(fim), e_n)
        theta = np.dot(self.design, fim_e_n)
        phi = np.dot(e_n, fim_e_n)

        value = np.log(phi)
        gradient = -1.0 / phi * theta**2
        hessian = np.outer(gradient, gradient) + 2.0 / phi * np.multiply(
            np.dot(
                self.design,
                sp.linalg.lu_solve(sp.linalg.lu_factor(fim), self.design.T),
            ),
            np.outer(theta, theta),
        )

        return value, gradient, hessian


class CCritSupp(FunctionTargetSupp):
    def set_constants(self, linear_model, weights, supp, m):
        self.linear_model = linear_model
        self.fim = linear_model.fim(weights, supp)
        self.supp = supp
        self.m = m

    @partial(jit, static_argnums=(0,), backend="cpu")
    def compute(self, x):
        feat_size = self.linear_model.selected_feature_size

        e_n = np.ones(feat_size)
        offset = feat_size - self.m
        e_n = e_n.at[:offset].set(0)

        feature_vec = self.linear_model.feature_vec(x)
        jac = self.linear_model.jac(x)
        fim_e_n = sp.linalg.lu_solve(sp.linalg.lu_factor(self.fim), e_n)
        theta = np.dot(feature_vec, fim_e_n)
        phi = np.dot(e_n, fim_e_n)
        jac_fim_e_n = np.dot(jac.T, fim_e_n)

        value = -(theta**2) / phi
        gradient = -2 * theta * jac_fim_e_n / phi

        return value, gradient


class CostCritWeights(FunctionTarget):
    def set_constants(self, measured_supp, supp, cost_function):
        self.cost_function = cost_function
        if measured_supp.shape[0] > 0:
            supp_distance = vmap(
                lambda x: np.linalg.norm(np.array([x]) - measured_supp, axis=1, ord=2)
            )(supp)
        else:
            supp_distance = np.ones(supp.shape)
        self.supp_penalty = np.all(supp_distance >= 1e-5, axis=1)
        self.supp = supp

    @partial(jit, static_argnums=(0,))
    def compute(self, weights):
        supp_cost = np.multiply(self.supp_penalty, vmap(lambda x: self.cost_function(x))(self.supp))

        lin_cost = np.multiply(self.supp_penalty, 1.0 + np.multiply(supp_cost, weights))

        value = np.sum(lin_cost**2)
        gradient = np.multiply(2 * supp_cost, lin_cost)
        hessian = np.diag(2 * supp_cost**2)

        return value, gradient, hessian


class CostCritSupp(FunctionTargetSupp):
    def set_constants(self, measured_supp, weight, cost_function):
        self.cost_function = cost_function
        self.cost_function_grad = grad(cost_function)
        self.measured_supp = measured_supp
        self.weight = weight

    @partial(jit, static_argnums=(0,), backend="cpu")
    def compute(self, x):
        factor = 0.0
        if self.measured_supp.shape[0] > 0:
            distance = np.linalg.norm(np.array([x]) - self.measured_supp, axis=1, ord=2)
            factor = 1.0 * np.invert(np.any(distance < 1e-5))

        cost = self.cost_function(x)
        cost_grad = self.cost_function_grad(x)
        lin_cost = 1.0 + cost * self.weight

        value = factor * lin_cost**2
        gradient = factor * 2 * cost_grad * lin_cost

        return value, gradient
