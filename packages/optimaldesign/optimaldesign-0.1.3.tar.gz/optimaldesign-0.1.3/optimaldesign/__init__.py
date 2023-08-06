import os
from optimaldesign.linear_model import LinearModel
from jax.config import config
from optimaldesign.optimal_design import OptimalDesign

# os.environ["JAX_PLATFORM_NAME"] = "cpu"

os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

os.environ["NUM_INTER_THREADS"] = "1"
os.environ["NUM_INTRA_THREADS"] = "1"

os.environ["XLA_FLAGS"] = "--xla_cpu_multi_thread_eigen=false " "intra_op_parallelism_threads=1"


config.update("jax_enable_x64", True)

__all__ = ["LinearModel", "OptimalDesign"]
