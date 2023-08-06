from optimaldesign.optimal_design import OptimalDesign
import jax.numpy as np
from jax.config import config

config.update("jax_enable_x64", True)


def quadratic_polynomial(x, c):
    return c[0] + c[1] * x[0] + c[2] * x[0] ** 2


def const_cost_function(x):
    return 1.0


class TestOptimalDesign:
    """
    Test Case with a optimal design for linear regression model with features (1,x,x^2) on
    design space [-1,1] with 101 equal distributed support points as initial grid.
    """

    def test_solve_d(self):
        points_per_dim = 101
        dim = 1
        x_u = np.full(dim, 1)
        x_l = -x_u
        x_q = np.full(dim, points_per_dim, dtype=np.int64)
        optimal_design = OptimalDesign(
            f=quadratic_polynomial,
            feature_size=3,
            x_u=x_u,
            x_l=x_l,
            x_q=x_q,
            optimality="d",
        )
        weights, supp = optimal_design.solve()
        supp_solution = np.array([[-1], [0], [1]])
        weights_solution = np.array([1 / 3, 1 / 3, 1 / 3])
        assert np.linalg.norm(supp - supp_solution) < 1e-5
        assert np.linalg.norm(weights - weights_solution) < 1e-5

    def test_solve_c(self):
        points_per_dim = 101
        dim = 1
        x_u = np.full(dim, 1)
        x_l = -x_u
        x_q = np.full(dim, points_per_dim, dtype=np.int64)
        optimal_design = OptimalDesign(
            f=quadratic_polynomial,
            feature_size=3,
            x_u=x_u,
            x_l=x_l,
            x_q=x_q,
            optimality="c",
            m=1,
        )
        weights, supp = optimal_design.solve()
        supp_solution = np.array([[-1], [0], [1]])
        weights_solution = np.array([1 / 4, 1 / 2, 1 / 4])
        assert np.linalg.norm(supp - supp_solution) < 1e-5
        assert np.linalg.norm(weights - weights_solution) < 1e-5

    def test_solve_cd(self):
        points_per_dim = 101
        dim = 1
        x_u = np.full(dim, 1)
        x_l = -x_u
        x_q = np.full(dim, points_per_dim, dtype=np.int64)
        optimal_design = OptimalDesign(
            f=quadratic_polynomial,
            feature_size=3,
            x_u=x_u,
            x_l=x_l,
            x_q=x_q,
            optimality="cd",
            m=1,
            alpha=0.75,
        )
        weights, supp = optimal_design.solve()
        supp_solution = np.array([[-1], [0], [1]])
        weights_solution = np.array([0.3, 0.4, 0.3])
        assert np.linalg.norm(supp - supp_solution) < 1e-5
        assert np.linalg.norm(weights - weights_solution) < 1e-5

    def test_solve_d_cost(self):
        points_per_dim = 101
        dim = 1
        x_u = np.full(dim, 1)
        x_l = -x_u
        x_q = np.full(dim, points_per_dim, dtype=np.int64)
        optimal_design = OptimalDesign(
            f=quadratic_polynomial,
            feature_size=3,
            x_u=x_u,
            x_l=x_l,
            x_q=x_q,
            optimality="d",
            use_cost_function=True,
            alpha_cost=0.3164558,
            cost_function=const_cost_function,
            measured_supp=np.array([[0.1]]),
        )
        weights, supp = optimal_design.solve()
        supp_solution = np.array([[-1], [0.1], [1]])
        weights_solution = np.array([0.2, 0.6, 0.2])
        assert np.linalg.norm(supp - supp_solution) < 1e-5
        assert np.linalg.norm(weights - weights_solution) < 1e-5
