# (c) Justin Beaurone
import sys
import json
import numpy as np
from verimedian import verifiable_median
from verimedian import prepare_inputs
from verimedian import poseidon_hash_chain

if (len(sys.argv) != 3):
    raise SystemError('Usage: python generate_test_cases_json.py values_length output_dir')

try:
    values_length = int(sys.argv[1])
except:
    print('Usage: python generate_test_cases_json.py values_length output_dir')
    raise SystemError('values_length must be an integer.')

output_dir = sys.argv[2]

unsortedValues = np.array(np.arange(values_length, dtype=int), dtype=object)
np.random.shuffle(unsortedValues)

sortingKey, medianValue = verifiable_median(unsortedValues)
input_json = prepare_inputs(sortingKey, unsortedValues, medianValue)

with open(f'{output_dir}/input.json', 'w') as f:
    json.dump(input_json, f, indent=2)
