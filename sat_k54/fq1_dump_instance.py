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

# --- instance-of-record dump (2026-09-11, main session): identical encoding, no solving
import hashlib, pysat
out = os.path.join(HERE, f"fq1_k{K}_instance.cnf")
cnf.to_file(out)
h = hashlib.sha256(open(out,'rb').read()).hexdigest()
print("DIMACS", out, "sha256", h, "vars", cnf.nv, "clauses", len(cnf.clauses), "pysat", pysat.__version__)
