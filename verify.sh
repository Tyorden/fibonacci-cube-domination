#!/bin/sh
# Re-check everything in this deposit that can be checked without a SAT solver:
#   1. every file matches MANIFEST.sha256;
#   2. the k = 54 instance matches its recorded sha256;
#   3. the 59-vertex set is a dominating set of Gamma_12 (from-definition verifier).
# Optional (needs python-sat, see README): regenerate the instance and compare hashes.
set -e
cd "$(dirname "$0")"
if command -v sha256sum >/dev/null 2>&1; then SUM="sha256sum"; else SUM="shasum -a 256"; fi
echo "[1/3] manifest"
$SUM -c MANIFEST.sha256
echo "[2/3] instance hash"
( cd sat_k54 && $SUM -c fq1_k54_instance.cnf.sha256 )
echo "[3/3] 59-set verifier"
python3 witness/verify_59set.py
echo "ALL CHECKS PASSED"
