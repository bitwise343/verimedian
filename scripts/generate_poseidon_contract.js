const fs = require('fs')
const {createCode, generateABI} = require("circomlibjs").poseidonContract

const creationCode = createCode(2)
const abi = generateABI(2)

fs.writeFileSync(
    "build/poseidon.json",
    JSON.stringify({creationCode, abi})
)