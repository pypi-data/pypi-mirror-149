from optimaldesign.linear_model import LinearModel, LinearModelCPU
import jax.numpy as np
from jax.config import config
from jax import vmap

config.update("jax_enable_x64", True)


class TestLinearModel:
    """
    Test Case with a simple line as linear model
    """

    linear_model_feature_size = 2
    x = np.array([1.0])
    c = np.array([1, 2])

    points = vmap(lambda i: np.array([-1 + i / 2 * 2.0]))(np.arange(3))
    weights = np.array([0.4, 0.2, 0.4])

    def linear_model_f(x, c):
        return c[0] + c[1] * x[0]

    linear_model = LinearModel(f=linear_model_f, feature_size=linear_model_feature_size)

    def test_class_init(self):
        assert np.array_equal(self.linear_model.zeros, np.zeros(self.linear_model_feature_size))

    def test_val(self):
        val = self.linear_model.val(self.x, self.c)
        assert val == 3.0

    def test_design(self):
        design_matrix = self.linear_model.design(self.points)
        design_matrix_target = np.array([[1, -1], [1, 0], [1, 1]])
        assert np.array_equal(design_matrix, design_matrix_target)

    def test_fim(self):
        fim = self.linear_model.fim(self.weights, self.points)
        fim_target = np.array([[1, 0], [0, 0.8]])
        assert np.array_equal(fim, fim_target)

    def test_fit(self):
        x = np.array([[1], [2], [3], [4]])
        y = np.array([1, 2, 3, 4])
        c, rmse = self.linear_model.fit(x, y)
        c_target = np.array([0, 1])
        val_x = np.array([1337])
        val_target = self.linear_model.val(val_x, c)
        assert rmse < 1e-10
        assert np.linalg.norm(c_target - c) < 1e-10
        assert np.abs(val_target - 1337) < 1e-10


class TestLinearModelCPU:
    """
    Test Case with a simple line as linear model
    """

    linear_model_feature_size = 2
    x = np.array([1.0])
    c = np.array([1, 2])

    points = vmap(lambda i: np.array([-1 + i / 2 * 2.0]))(np.arange(3))
    weights = np.array([0.4, 0.2, 0.4])

    def linear_model_f(x, c):
        return c[0] + c[1] * x[0]

    linear_model = LinearModelCPU(f=linear_model_f, feature_size=linear_model_feature_size)

    def test_class_init(self):
        assert np.array_equal(self.linear_model.zeros, np.zeros(self.linear_model_feature_size))

    def test_val(self):
        val = self.linear_model.val(self.x, self.c)
        assert val == 3.0

    def test_design(self):
        design_matrix = self.linear_model.design(self.points)
        design_matrix_target = np.array([[1, -1], [1, 0], [1, 1]])
        assert np.array_equal(design_matrix, design_matrix_target)

    def test_fim(self):
        fim = self.linear_model.fim(self.weights, self.points)
        fim_target = np.array([[1, 0], [0, 0.8]])
        assert np.array_equal(fim, fim_target)

    def test_fit(self):
        x = np.array([[1], [2], [3], [4]])
        y = np.array([1, 2, 3, 4])
        c, rmse = self.linear_model.fit(x, y)
        c_target = np.array([0, 1])
        val_x = np.array([1337])
        val_target = self.linear_model.val(val_x, c)
        assert rmse < 1e-10
        assert np.linalg.norm(c_target - c) < 1e-10
        assert np.abs(val_target - 1337) < 1e-10
