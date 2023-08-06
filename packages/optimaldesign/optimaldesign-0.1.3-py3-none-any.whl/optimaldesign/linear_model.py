import jax.numpy as np
from functools import partial
from jax import jit, vmap, grad, hessian, jacfwd
import jax.scipy as sp
from typing import List, Callable


class LinearModel:
    def __init__(self, f: Callable, feature_size: int, selected_features: List = []):
        self.f = f
        self.feature_size = feature_size
        if 0 == len(selected_features):
            self.selected_feature_idx = np.arange(feature_size)
        else:
            self.selected_feature_idx = selected_features
        self.selected_feature_size = len(self.selected_feature_idx)
        self.identity = np.zeros((len(self.selected_feature_idx), self.feature_size))
        for i, idx in enumerate(self.selected_feature_idx):
            self.identity = self.identity.at[i, idx].set(1)
        self.zeros = np.zeros(feature_size)

    @partial(jit, static_argnums=(0,))
    def __c_mapper(self, c):
        return self.zeros.at[self.selected_feature_idx].set(c[self.selected_feature_idx])

    @partial(jit, static_argnums=(0,))
    def val(self, x, c):
        return self.f(x, self.__c_mapper(c))

    @partial(jit, static_argnums=(0,))
    def grad(self, x, c):
        return grad(self.f, argnums=0)(x, c)

    @partial(jit, static_argnums=(0,))
    def hessian(self, x, c):
        return hessian(self.f, argnums=0)(x, c)

    @partial(jit, static_argnums=(0,))
    def design(self, data):
        return vmap(lambda x: vmap(lambda y: self.f(x, y))(self.identity))(data)

    @partial(jit, static_argnums=(0,))
    def feature_vec(self, x):
        return vmap(lambda c: self.f(x, c))(self.identity)

    @partial(jit, static_argnums=(0,))
    def feature_vec_hessian(self, x):
        return vmap(lambda c: self.hessian(x, c))(self.identity)

    @partial(jit, static_argnums=(0,))
    def jac(self, x):
        return vmap(lambda c: jacfwd(self.f)(x, c))(self.identity)

    @partial(jit, static_argnums=(0,))
    def fim(self, weights, x):
        dm = self.design(x)
        return np.dot(dm.T, np.dot(np.diag(weights), dm))

    @partial(jit, static_argnums=(0,))
    def fit(self, x, y):
        # solve normal equation and estimate coefficient c: a * c = b
        dm = self.design(x)
        a = np.dot(dm.T, dm)
        b = np.dot(dm.T, y)
        c = sp.linalg.solve(a, b, sym_pos=True)
        rmse = np.sqrt(1.0 / y.shape[0]) * np.linalg.norm(np.dot(dm, c) - y)
        return c, rmse


class LinearModelCPU:
    def __init__(self, f: Callable, feature_size: int, selected_features: List = []):
        self.f = f
        self.feature_size = feature_size
        if 0 == len(selected_features):
            self.selected_feature_idx = np.arange(feature_size)
        else:
            self.selected_feature_idx = selected_features
        self.selected_feature_size = len(self.selected_feature_idx)
        self.identity = np.zeros((len(self.selected_feature_idx), self.feature_size))
        for i, idx in enumerate(self.selected_feature_idx):
            self.identity = self.identity.at[i, idx].set(1)
        self.zeros = np.zeros(feature_size)

    @partial(jit, static_argnums=(0,), backend="cpu")
    def __c_mapper(self, c):
        return self.zeros.at[self.selected_feature_idx].set(c[self.selected_feature_idx])

    @partial(jit, static_argnums=(0,), backend="cpu")
    def val(self, x, c):
        return self.f(x, self.__c_mapper(c))

    @partial(jit, static_argnums=(0,), backend="cpu")
    def grad(self, x, c):
        return grad(self.f, argnums=0)(x, c)

    @partial(jit, static_argnums=(0,), backend="cpu")
    def hessian(self, x, c):
        return hessian(self.f, argnums=0)(x, c)

    @partial(jit, static_argnums=(0,), backend="cpu")
    def design(self, data):
        return vmap(lambda x: vmap(lambda y: self.f(x, y))(self.identity))(data)

    @partial(jit, static_argnums=(0,), backend="cpu")
    def feature_vec(self, x):
        return vmap(lambda c: self.f(x, c))(self.identity)

    @partial(jit, static_argnums=(0,), backend="cpu")
    def feature_vec_hessian(self, x):
        return vmap(lambda c: self.hessian(x, c))(self.identity)

    @partial(jit, static_argnums=(0,), backend="cpu")
    def jac(self, x):
        return vmap(lambda c: jacfwd(self.f)(x, c))(self.identity)

    @partial(jit, static_argnums=(0,), backend="cpu")
    def fim(self, weights, x):
        dm = self.design(x)
        return np.dot(dm.T, np.dot(np.diag(weights), dm))

    @partial(jit, static_argnums=(0,), backend="cpu")
    def fit(self, x, y):
        # solve normal equation and estimate coefficient c: a * c = b
        dm = self.design(x)
        a = np.dot(dm.T, dm)
        b = np.dot(dm.T, y)
        c = sp.linalg.solve(a, b, sym_pos=True)
        rmse = np.sqrt(1.0 / y.shape[0]) * np.linalg.norm(np.dot(dm, c) - y)
        return c, rmse
