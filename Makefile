.PHONY : all
all : snarkjs venv rapidsnark circom circuits witness_calculator zkey

circom : venv/bin/circom

circuits : circom snarkjs

pyseidon : depends/poseidon/src/pyseidon_t3.c

snarkjs : node_modules/.bin/snarkjs

rapidsnark : venv/bin/prover

venv : venv/bin/activate

witness_calculator : venv/bin/moving_median moving_median.dat

zkey : build/moving_median.zkey build/verification_key.json build/powers16.ptau

build/moving_median_cpp/moving_median : build/moving_median_cpp/moving_median.cpp
	cd build/moving_median_cpp && make

build/moving_median.r1cs build/moving_median_cpp/moving_median.cpp build/moving_median_cpp/nlohmann/json.hpp &: node_modules/.bin/snarkjs venv/bin/circom depends/rapidsnark/depends/json/single_include/nlohmann/json.hpp circuits/moving_median.circom
	venv/bin/circom --r1cs --c circuits/moving_median.circom -o=build
	cp -r depends/rapidsnark/depends/json/single_include/* build/moving_median_cpp

build/moving_median.zkey : node_modules/.bin/snarkjs build/powers16.ptau build/moving_median.r1cs
	npx snarkjs g16s build/moving_median.r1cs build/powers16.ptau build/moving_median_0000.zkey
	npx snarkjs zkc build/moving_median_0000.zkey build/moving_median_0001.zkey --name="1st Contributor Name" -e="this is entropy" -v
	npx snarkjs zkb build/moving_median_0001.zkey build/moving_median.zkey 0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f 10 -n="Final Beacon phase2"

build/verification_key.json : node_modules/.bin/snarkjs build/moving_median.zkey
	npx snarkjs zkev build/moving_median.zkey build/verification_key.json

build/verifier.sol : node_modules/.bin/snarkjs build/moving_median.zkey
	npx snarkjs zkesv build/moving_median.zkey build/verifier.sol

build/powers16.ptau:
	wget -O build/powers16.ptau https://storage.googleapis.com/zkevm/ptau/powersOfTau28_hez_final_16.ptau

depends/rapidsnark/package/bin/prover : depends/rapidsnark/src/main_prover.cpp depends/rapidsnark/depends/json/single_include/nlohmann/json.hpp
	cd depends/rapidsnark && ./build_gmp.sh host
	mkdir depends/rapidsnark/build_prover
	cd depends/rapidsnark/build_prover && cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../package && make -j4 && make install

build/bin/circom : depends/circom/circom/src/main.rs
	cd depends/circom && cargo build --release
	cd depends/circom && mkdir -p build
	cd depends/circom && cargo install --path circom --root ../../build

depends/rapidsnark/src/main_prover.cpp depends/rapidsnark/depends/json/single_include/nlohmann/json.hpp depends/circom/circom/src/main.rs depends/poseidon/src/pyseidon_t3.c &:
	git submodule update --init --recursive

node_modules/.bin/snarkjs : package.json
	npm install .

depends/poseidon/gmp/package/lib/libgmp.a:
	cd depends/poseidon && ./build_gmp.sh host

venv/bin/activate : requirements.txt pyseidon depends/poseidon/gmp/package/lib/libgmp.a
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && cd depends/poseidon && pip install .

venv/bin/prover : depends/rapidsnark/package/bin/prover venv/bin/activate
	cp depends/rapidsnark/package/bin/prover venv/bin

venv/bin/circom : build/bin/circom venv/bin/activate
	cp build/bin/circom venv/bin

venv/bin/moving_median moving_median.dat &: build/moving_median_cpp/moving_median build/moving_median_cpp/moving_median.dat venv/bin/activate
	cp build/moving_median_cpp/moving_median venv/bin
	cp build/moving_median_cpp/moving_median.dat .

.PHONY : clean docker
clean :
	rm -rf ./build/*
	rm -rf ./depends/*
	rm -rf ./node_modules
	rm -rf ./venv
	rm -rf ./verimedian.egg-info

# docker : Dockerfile build/moving_median_cpp/moving_median.cpp build/moving_median_cpp/moving_median.dat build/verification_key.json build/moving_median.zkey requirements.txt setup.py ./verimedian/*
# 	docker build -t verimedian:0.1.0 .
docker:
	docker build -t verimedian:0.1.0 .