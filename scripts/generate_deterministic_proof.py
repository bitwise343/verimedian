# (c) Justin Beaurone
import sys
import json
import numpy as np
from verimedian import verifiable_median
from verimedian import prepare_inputs
from verimedian import poseidon_hash_chain
from verimedian import full_prove


values = [1625247, 2932010, 2379762, 4185235, 4201745, 2290390, 2901141,
          6468766, 1453971, 1620083, 1925490, 6832793, 6107419, 690155, 6924083,
          5362104, 6707654, 3027114, 1150630, 2413718, 966300, 5861855, 3084829,
          5215113, 4004604, 7418271, 2113262, 3191211, 4802429, 1640759,
          6415508, 5899765, 6691489, 2056834, 4313598, 3477212, 1681116,
          6746876, 735706, 2032879, 3840911, 408824, 5611558, 1946707, 3570179,
          3949772, 2756480, 1155596, 3076175, 117090, 7547931, 5765540, 7641299,
          315311, 1359870, 1194842, 2513047, 4989863, 244852, 124129, 6222386,
          7294703, 2203486, 7597243, 7634582, 5728957, 563561, 1142933, 2063590,
          1448525, 3840786, 2454381, 2668167, 1225347, 1602712, 4102176, 199966
          ]

values = np.array(values, dtype=object)
sortingKey, sortedValues, medianValue = verifiable_median(values)
input_json = prepare_inputs(sortingKey, values, medianValue)

with open(f'proofs/deterministic_input.json', 'w') as f:
    json.dump(input_json, f, indent=2)

full_prove(input_json, prefix='deterministic_')

