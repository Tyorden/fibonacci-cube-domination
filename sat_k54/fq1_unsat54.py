# DEPOSIT COPY NOTE (2026-09-20): identical to the script that ran, except that one em dash inside a
# print-string (the SAT branch message) was replaced by a hyphen for the public copy. The original
# file's sha256 is 1a053dac098cec229bb416d4972de7682101cbcae00e6e44113a98bc40eb45d3. The CNF built by
# this script is unaffected (see fq1_dump_instance.py and fq1_k54_instance.cnf.sha256).
# FQ1 lower-bound attack: prove NO dominating set of size 54 exists in Gamma_12
# (=> gamma(Gamma_12) >= 55, improving the published LB 54). SAT route:
# covering clauses + seqcounter atmost-54 + lex-leader on the reversal involution.
# Sound for UNSAT: lex-leader keeps at least one member of every solution orbit.
# Fable 5, 2026-08-21. Run: venv_compute/bin/python fq1_unsat54.py <k>
import sys, time, os
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

K = int(sys.argv[1]) if len(sys.argv) > 1 else 54
HERE = os.path.dirname(os.path.abspath(__file__))

# Gamma_12: fibbinary strings of length 12 (no two adjacent 1s); edges = Hamming distance 1
n = 12
verts = [v for v in range(1 << n) if (v & (v << 1)) == 0]
idx = {v: i for i, v in enumerate(verts)}
V = len(verts)
adj = [[] for _ in range(V)]
for v in verts:
    for b in range(n):
        u = v ^ (1 << b)
        if (u & (u << 1)) == 0:
            adj[idx[v]].append(idx[u])
E = sum(len(a) for a in adj) // 2
assert V == 377 and E == 1308, (V, E)

pool = IDPool()
x = [pool.id(("x", i)) for i in range(V)]
cnf = CNF()
for i in range(V):
    cnf.append([x[i]] + [x[j] for j in adj[i]])          # closed-neighborhood cover
card = CardEnc.atmost(lits=x, bound=K, vpool=pool, encoding=EncType.seqcounter)
cnf.extend(card.clauses)

# reversal automorphism sigma: reverse the 12 bits (maps fibbinary to fibbinary)
def rev(v):
    r = 0
    for b in range(n):
        if v >> b & 1: r |= 1 << (n - 1 - b)
    return r
sigma = [idx[rev(v)] for v in verts]
# lex-leader X <=lex X∘sigma over vertex order 0..V-1, standard chain encoding:
# eq_{-1}=T; eq_i <-> eq_{i-1} & (x_i <-> x_{sigma_i}); constraint: eq_{i-1} -> (x_i <= x_{sigma_i})
prev_eq = None
for i in range(V):
    j = sigma[i]
    if j == i:
        continue
    if prev_eq is None:
        cnf.append([-x[i], x[j]])                        # x_i -> x_j  (x_i <= x_j at first diff pos)
    else:
        cnf.append([-prev_eq, -x[i], x[j]])
    e = pool.id(("eq", i))
    # e <-> prev_eq & (x_i <-> x_j)
    if prev_eq is None:
        cnf.append([-e, -x[i], x[j]]); cnf.append([-e, x[i], -x[j]])
        cnf.append([e, x[i], x[j]]); cnf.append([e, -x[i], -x[j]])
    else:
        cnf.append([-e, prev_eq])
        cnf.append([-e, -x[i], x[j]]); cnf.append([-e, x[i], -x[j]])
        cnf.append([e, -prev_eq, x[i], x[j]]); cnf.append([e, -prev_eq, -x[i], -x[j]])
    prev_eq = e

print(f"CNF: {cnf.nv} vars, {len(cnf.clauses)} clauses; K={K}", flush=True)
t0 = time.time()
with Cadical195(bootstrap_with=cnf.clauses) as s:
    res = s.solve()
    dt = time.time() - t0
    if res:
        model = set(l for l in s.get_model() if l > 0)
        ds = [i for i in range(V) if x[i] in model]
        print(f"SAT in {dt:.0f}s: dominating set of size <= {K} EXISTS ({len(ds)} vertices) - LB cannot rise past {K}.")
        with open(os.path.join(HERE, f"domset_{K}.txt"), "w") as f:
            for i in ds: f.write(format(verts[i], "012b") + "\n")
    else:
        print(f"UNSAT in {dt:.0f}s: NO dominating set of size {K}. gamma(Gamma_12) >= {K+1}. RECORD.")
        with open(os.path.join(HERE, f"UNSAT_{K}.txt"), "w") as f:
            f.write(f"UNSAT k={K} in {dt:.0f}s, cadical195, seqcounter, lex-leader reversal\n")
