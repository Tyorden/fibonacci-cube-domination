# FQ1 run 2026-08-21 - lower-bound attack k=54 (pre-registered)
GOAL: UNSAT for "dominating set of size <= 54 in Gamma_12" => gamma >= 55, the
first improvement of the published lower bound (Azarija et al. 2018 Table 3:
54-61; our verified UB is 59). Any UNSAT here is a genuine publishable-progress
step; full closure needs UNSAT at 58.
METHOD: CaDiCaL 1.9.5 via pysat; closed-neighborhood covering clauses; seqcounter
atmost-54; lex-leader symmetry breaking on the bit-reversal involution (sound for
UNSAT: every solution orbit retains its lex-leader). ENCODING SANITY PASSED:
K=70 SAT in 33s and the witness independently re-verified as dominating
(0 uncovered). CNF: 22,231 vars / ~45,700 clauses.
KILL: none pre-set; solver runs until decided or manually stopped (multi-day
expected; the 2018 authors could not close n=13 totals in "real time" either).
If SAT at 54 (a 54-set exists!): that would MATCH the LB and shrink the bracket
from above-below simultaneously - immediately re-verify the witness independently.

(Deposit copy note, 2026-09-20: verbatim except one em dash in the title line replaced by a hyphen; original sha256 8c84a1789229565bffc773355a9df81de26af5bcae4b7690e7ec62e4c664aee9. The CNF figures quoted above, 22,231 vars / ~45,700 clauses, describe an earlier encoding; the run's own log line and the instance of record are 18183 vars / 37713 clauses.)
