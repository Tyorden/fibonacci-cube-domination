#!/usr/bin/env python3
"""Independent re-verification of the size-59 dominating set for Gamma_12.

Fresh code (2026-08-30): does NOT import or reuse any checker from the
2026-08-19 run. Constructs the 12th Fibonacci cube from its definition and
checks the certificate file directly.

Definition used:
  V(Gamma_12) = all binary strings of length 12 with no two consecutive 1s.
  E(Gamma_12) = pairs of vertices at Hamming distance exactly 1.

Asserts |V| = 377 (= F_14) and |E| = 1308, then checks the certificate:
  - exactly 59 distinct strings,
  - each is a valid vertex (length 12, {0,1} only, no "11" substring),
  - every vertex of Gamma_12 is in the set or adjacent to a member.

Exit status 0 iff every check passes.
"""
import sys
from itertools import product

import os
# Deposit copy (2026-09-20): the certificate path is the first command-line argument, or, by
# default, gamma12_domset_59.txt next to this script. The original script hard-coded a local
# path; nothing else was changed (original sha256
# 31922fe88cb30a6d394f5d7b2b7c93b9a81b8b6c833f5b9cbe59af54c99cc37a).
CERT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "gamma12_domset_59.txt")

N = 12

def main():
    # (a) Build Gamma_12 from scratch.
    vertices = ["".join(bits) for bits in product("01", repeat=N)
                if "11" not in "".join(bits)]
    vset = set(vertices)
    assert len(vertices) == 377, f"|V| = {len(vertices)}, expected 377"
    assert len(vset) == 377, "duplicate vertices"

    # Neighbors: flip one bit; keep result iff it is a Fibonacci string.
    def neighbors(v):
        out = []
        for i in range(N):
            w = v[:i] + ("1" if v[i] == "0" else "0") + v[i+1:]
            if w in vset:
                out.append(w)
        return out

    edge_count = sum(len(neighbors(v)) for v in vertices)
    assert edge_count % 2 == 0, "handshake parity violated"
    assert edge_count // 2 == 1308, f"|E| = {edge_count // 2}, expected 1308"

    # (b) Load and validate the certificate.
    with open(CERT) as f:
        lines = [ln.strip() for ln in f
                 if ln.strip() and not ln.lstrip().startswith("#")]
    assert len(lines) == 59, f"certificate has {len(lines)} entries, expected 59"
    domset = set(lines)
    assert len(domset) == 59, "certificate contains duplicates"
    for s in domset:
        assert len(s) == 12 and set(s) <= {"0", "1"} and "11" not in s, \
            f"invalid vertex in certificate: {s!r}"

    # (c) Domination: every vertex is in the set or adjacent to a member.
    uncovered = [v for v in vertices
                 if v not in domset and not any(w in domset for w in neighbors(v))]
    assert not uncovered, f"{len(uncovered)} uncovered vertices, e.g. {uncovered[:5]}"

    print("PASS: |V|=377, |E|=1308, |D|=59, all vertices valid, domination verified.")
    print("Conclusion: gamma(Gamma_12) <= 59.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
