"""Test algo functionality."""
from .errors import TestError
from .tabular import test_tabular
from ..base.tabular import TabularClassifier, TabularRegressor

def test_algo(algo, output_dir, timeout = 100, nan_fraction = 0.1):
    """
    Function for testing algo functionality.

    Args:
        algo: TabularClassifier or TabularRegressor.
        output_dir: local directory for saving model.
        timeout: search time in seconds.
        nan_fraction: probability of null values in data.

    Returns:
        None.
    """
    if isinstance(algo, TabularClassifier)  or isinstance(algo, TabularRegressor):
        return test_tabular(algo, output_dir, timeout, nan_fraction)
    else:
        raise TestError('invalid algo class')
