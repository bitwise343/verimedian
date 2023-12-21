import json
from subprocess import run
from pyseidon_t3 import poseidon_hash_chain


def prepare_inputs(A, x, m, initial_hash=0):
    values_str = [str(value) for value in x]
    initial_hash_str = str(initial_hash)
    sorting_key = [[str(element) for element in row] for row in A]
    return {"median": str(m),
            "initialHash": initial_hash_str,
            "valuesHash": poseidon_hash_chain(values_str, initial_hash_str),
            "values": values_str,
            "sortingKey": sorting_key,
            }

def calculate_witness(input_json,
                      prefix='',
                      proofs_fpath='proofs/',
                      input_fname='input.json',
                      witness_fname='witness.wtns',
                      verbose=False,
                      ):
    """Calculate the witness by saving the input as a json file then running the
    `moving_median` binary. Creates two files, raises error on failure.

    Files created:
        input file: /proofs_fpath/prefix + input_fname
        witness file: /proofs_fpath/prefix + witness_fname
    """
    input_fpath = proofs_fpath + prefix + input_fname
    witness_fpath = proofs_fpath + prefix + witness_fname

    with open(input_fpath, 'w+') as f:
        json.dump(input_json, f)

    run_result = run(['moving_median', input_fpath, witness_fpath,],
                     capture_output=True)
    if verbose:
        print(run_result)

    if run_result.returncode != 0 or len(run_result.stdout) != 0 \
        or len(run_result.stderr) != 0:
        raise Exception(f"Witness calc failed. stderr: {run_result.stderr}")

def full_prove(input_json,
               prefix='',
               proofs_fpath='proofs/',
               input_fname='input.json',
               witness_fname='witness.wtns',
               proof_fname='proof.json',
               public_fname='public.json',
               zkey_fpathname='build/moving_median.zkey',
               verbose=False,
               ):
    """Compute a zero knowledge proof by first calculating the witness of the
    input, then by running the `prover` rapidsnark binary to create the proof.
    Silently creates four files, raises error on failure.

    Files created:
        input file: /proofs_fpath/prefix + input_fname
        witness file: /proofs_fpath/prefix + witness_fname
        proof data file: /proofs_fpath/prefix + proof_fname
        public inputs file: /proofs_fpath/prefix + public_fname
    """
    calculate_witness(input_json, prefix=prefix, proofs_fpath=proofs_fpath,
                      input_fname=input_fname, witness_fname=witness_fname,
                      verbose=verbose)

    witness_fpath = proofs_fpath + prefix + witness_fname
    proof_fpath = proofs_fpath + prefix + proof_fname
    public_fpath = proofs_fpath + prefix + public_fname

    run_result = run(['prover', zkey_fpathname, witness_fpath, proof_fpath,
                      public_fpath])
    if verbose:
        print(run_result)

    if run_result.returncode != 0:
        raise Exception(f"ZkProof calc failed. stderr: {run_result.stderr}")

def unpack_proof_data(proof_json,):
    proof_a = proof_json["pi_a"][0:2]
    proof_b = [proof_json["pi_b"][0][::-1], proof_json["pi_b"][1][::-1]]
    proof_c = proof_json["pi_c"][0:2]
    return proof_a, proof_b, proof_c