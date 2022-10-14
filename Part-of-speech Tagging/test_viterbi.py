"""Tests for POS tagging."""
import numpy as np
import pytest

from viterbi import viterbi

# pi_i = probability of starting at state i
pi = np.array([0.6, 0.4])
# a_{ij} = probability of transitioning from state i to state j
A = np.array([[0.7, 0.3], [0.4, 0.6]])
# b_{ik} = probability of observing k at state i
B = np.array([[0.1, 0.4, 0.5], [0.6, 0.3, 0.1]])

test_cases = [
    {"obs": [2, 1, 0], "p": 0.01512, "states": [0, 0, 1]},
    {"obs": [2, 1, 0, 0, 1, 2], "p": 0.00030, "states": [0, 0, 1, 1, 0, 0]},
    {
        "obs": [2, 1, 0, 0, 1, 2] * 10,
        "p": 0.00000,
        "states": [0, 0, 1, 1, 0, 0],
    },
]


@pytest.mark.parametrize("test_case", test_cases)
def test_viterbi(test_case):
    """Test the result."""
    states_guess, prob = viterbi(test_case["obs"], pi, A, B)
    assert (
        list(states_guess[-len(test_case["states"]) :]) == test_case["states"]
    )
    assert round(prob, 5) == test_case["p"]


if __name__ == "__main__":
    retcode = pytest.main([__file__])
