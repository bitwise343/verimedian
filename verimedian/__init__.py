# (c) Justin Beaurone
"""This module implements things.
"""


__all__ = ['P', 'verifiable_median', 'prepare_inputs', 'calculate_witness',
           'full_prove', 'unpack_proof_data']

import os
import json
import numpy as np


P = int(
    '0x30644e72e131a029b85045b68181585d2833e84879b9709143e1f593f0000001', 16)

FPATH = os.sep.join(__file__.split(os.sep)[:-1])
POSEIDON_CONSTANTS_FPATH = f"{FPATH}{os.sep}poseidon_constants_opt.json"

type_array = np.frompyfunc(type, 1, 1)
int_array = np.frompyfunc(lambda v: int(v, 16), 1, 1)

def load_poseidon_constants() -> dict:
    with open(POSEIDON_CONSTANTS_FPATH, 'r') as f:
        c_raw = json.load(f)
        optimized_constants = {}
        for k, v in c_raw.items():
            m = {}
            for i, vi in enumerate(v):
                m[i] = np.array(int_array(vi), dtype=object)
            optimized_constants[k] = m
    return optimized_constants

from .verifiable_median import verifiable_median
from .prover import prepare_inputs
from .prover import full_prove
from .prover import calculate_witness
from .prover import unpack_proof_data
