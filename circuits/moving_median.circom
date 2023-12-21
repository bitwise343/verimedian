// (c) Justin Beaurone
pragma circom 2.0.3;

include "../node_modules/circomlib/circuits/comparators.circom";
include "../node_modules/circomlib/circuits/poseidon.circom";
include "../node_modules/circomlib-matrix/circuits/matMul.circom";
include "../node_modules/circomlib-matrix/circuits/matElemSum.circom";

template HashChain(n) {
    signal input values[n];
    signal input initialHash;
    signal output hash;

    component hashers[n];

    for (var i = 0; i < n; i++) {
        hashers[i] = Poseidon(2);
        hashers[i].inputs[0] <== i == 0 ? initialHash : hashers[i-1].out;
        hashers[i].inputs[1] <== values[i];
    }

    hash <== hashers[n-1].out;
}

template MovingMedian(n) {
    signal input valuesHash;
    signal input initialHash;
    signal input values[n];
    signal input sortingKey[n][n];
    signal input median;

    component hashChain = HashChain(n);
    hashChain.initialHash <== initialHash;
    for (var i = 0; i < n; i++) {
        hashChain.values[i] <== values[i];
    }
    hashChain.hash === valuesHash;

    component rowSum[n];
    component columnSum[n];
    for (var i = 0; i < n; i++) {
        rowSum[i] = matElemSum(1, n);
        columnSum[i] = matElemSum(1, n);

        for (var j = 0; j < n; j++) {
            sortingKey[i][j] * (1 - sortingKey[i][j]) === 0;
            rowSum[i].a[0][j] <== sortingKey[i][j];
            columnSum[i].a[0][j] <== sortingKey[j][i];
        }

        rowSum[i].out * rowSum[i].out === 1;
        columnSum[i].out * columnSum[i].out === 1;
    }

    component matrixMultiplier = matMul(n, n, 1);
    for (var i = 0; i < n; i++) {
        matrixMultiplier.b[i][0] <== values[i];
        for (var j = 0; j < n; j++) {
            matrixMultiplier.a[i][j] <== sortingKey[i][j];
        }
    }

    component isSorted[n-1];
    for (var i = 0; i < n - 1; i++) {
        isSorted[i] = LessEqThan(252);
        isSorted[i].in[0] <== matrixMultiplier.out[i][0];
        isSorted[i].in[1] <== matrixMultiplier.out[i + 1][0];
        isSorted[i].out === 1;
    }

    median === matrixMultiplier.out[n\2][0];
}

component main {public [valuesHash, initialHash, median]} = MovingMedian(77);