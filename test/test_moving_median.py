# (c) Justin Beaurone
import numpy as np
from verimedian import P
from verimedian import verifiable_median
from verimedian import prepare_inputs
from verimedian import full_prove


# Construct array of BigInt values, descending from P.
N = 77

values = np.array([P - int(i + 1) for i in range(N)], dtype=object)
np.random.shuffle(values)

ones = np.ones(values.size)

sorting_key, median = verifiable_median(values)

def test_matmul():
    Ax = np.matmul(sorting_key, values)
    assert np.all(Ax[:-1] <= Ax[1:])

def test_binary_condition():
    # every element of A is binary
    assert np.all((sorting_key * (1 - sorting_key)) == 0)

def test_basis_columns():
    # every column is a unit vector
    assert np.all(sorting_key.sum(axis=0) == ones)

def test_completion():
    # none of the unit vectors repeat
    assert np.all(sorting_key.sum(axis=1) == ones)

def test_prover():
    input_json = prepare_inputs(sorting_key, values, median)
    result = full_prove(
        input_json,
        prefix='test_proof_',
        proofs_fpath='./proofs/',
        zkey_fpathname='./build/moving_median.zkey',
    )
