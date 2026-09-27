# fibonacci-cube-domination

Archived on Zenodo: DOI [10.5281/zenodo.22985212](https://doi.org/10.5281/zenodo.22985212) (concept DOI 10.5281/zenodo.22985187, always the newest version). Cite the DOI for this deposit.


A documented attempt, not a result. This repository deposits, for anyone who wants to build on
it, exactly three things about the domination number of the 12th Fibonacci cube: a verified
59-vertex dominating set (which is already public on OEIS A291295), the exact SAT instance for
the question "is there a dominating set of at most 54 vertices?", and the record of a 30-day
solver run on that instance that ended without a decision. Nothing here moves a bound.

## 1. The question

The n-th Fibonacci cube Gamma_n has as vertices the binary strings of length n with no two
consecutive 1s, two strings being adjacent when they differ in exactly one position. Gamma_12 has
377 vertices (the Fibonacci number F(14)) and 1308 edges. A dominating set is a set D of vertices
such that every vertex is in D or adjacent to a member of D; the domination number gamma(Gamma_12)
is the size of a smallest dominating set. OEIS A291295 lists gamma(Gamma_n) for n = 1..11
(1, 1, 2, 3, 4, 5, 8, 12, 17, 25, 39); the exact value for n = 12 is not known.

## 2. The published bracket: 54 <= gamma(Gamma_12) <= 61

Jernej Azarija, Sandi Klavžar, Yoomi Rho and Seungbo Sim, "On domination-type invariants of
Fibonacci cubes and hypercubes", Ars Mathematica Contemporanea 14 (2018), no. 2, pages 387-395,
doi:10.26493/1855-3974.1172.bae (published online 2017-10-28). Their table of bounds gives
54 <= gamma(Gamma_12) <= 61. The citation fields (authors, title, journal, volume, issue, pages,
DOI) were checked on 2026-09-20 against the Crossref record and the journal landing page; both
fetches are saved verbatim under `docs/reference_fetch_2026-09-20/`.

## 3. The upper bound 59: a verified dominating set, published on OEIS A291295

`witness/gamma12_domset_59.txt` lists 59 vertices of Gamma_12, one 12-character binary string per
line (leftmost character = position 1). Every vertex of Gamma_12 is in the set or adjacent to a
member of it, so gamma(Gamma_12) <= 59, improving the published upper bound 61 by two. The lower
bound 54 is the published one and is not touched by anything here.

The set was found by CP-SAT search on 2026-08-19 and is published as the a-file of OEIS A291295
(`https://oeis.org/A291295/a291295.txt`); the entry's comment, quoted verbatim from the fetch of
2026-09-20 saved in `docs/oeis_fetch_2026-09-20/` (entry revision #20, Sep 07 2026), reads:

> a(12) is in the interval [54, 59]: the bounds 54 <= a(12) <= 61 are from Azarija, Klavzar, Rho, and Sim (2018), and the upper bound improves to 59 by an explicit dominating set of size 59 in the 12th Fibonacci cube (see the a-file), found by CP-SAT search assisted by Claude (Anthropic) and independently verified by three separate programs, including a solver-free from-definition check. - _Tyler Satchel Orden_, Sep 06 2026

The 59 vertex lines of the published a-file are identical to `witness/gamma12_domset_59.txt`
(checked 2026-09-20 with `diff` after dropping the a-file's comment lines).

### Verifier and how to run it

`witness/verify_59set.py` is a from-definition checker written on 2026-08-30 with no code shared
with the search that produced the set. It rebuilds Gamma_12 from the definition (asserting 377
vertices and 1308 edges), reads the certificate, asserts 59 distinct valid vertices, and asserts
that every vertex is dominated. It needs only Python 3 (no packages). Run it from the repository
root:

```
python3 witness/verify_59set.py
```

Output on 2026-09-20 (Python 3.13.1, macOS, exit status 0):

```
PASS: |V|=377, |E|=1308, |D|=59, all vertices valid, domination verified.
Conclusion: gamma(Gamma_12) <= 59.
```

It also accepts a path: `python3 witness/verify_59set.py <file>`; comment lines beginning with
`#` are skipped, so it can be pointed at the published a-file directly. Run on
`docs/oeis_fetch_2026-09-20/A291295_afile_a291295_2026-09-20T015017-0700.txt` on 2026-09-20: the
same PASS output, exit status 0.

`verify.sh` runs the manifest check, the instance hash check and this verifier in one go.

## 4. The k = 54 SAT attempt

### Encoding

`sat_k54/fq1_unsat54.py` builds, for a bound k, a CNF formula that is satisfiable if and only if
Gamma_12 has a dominating set of at most k vertices, up to the symmetry breaking described below:

- one Boolean variable x_v per vertex v (377 variables);
- one closed-neighbourhood clause per vertex: x_v OR (x_u for every neighbour u of v);
- an at-most-k cardinality constraint over the 377 vertex variables, sequential-counter encoding
  (PySAT `CardEnc.atmost`, `EncType.seqcounter`);
- lex-leader symmetry breaking on the bit-reversal involution of Gamma_12 (reversing a string with
  no two consecutive 1s gives another such string, and reversal preserves adjacency), by the
  standard chain encoding: the assignment must be lexicographically no larger than its image
  under reversal, in vertex order 0..376.

Soundness for UNSAT: every dominating set has an orbit under reversal of size 1 or 2, and the
lex-leader constraint keeps at least one member of every orbit, so if the formula with the
symmetry-breaking clauses is unsatisfiable then no dominating set of at most k vertices exists.
A SAT answer gives a witness directly.

### The exact instance

`sat_k54/fq1_k54_instance.cnf` is the DIMACS file for k = 54: header `p cnf 18183 37713`,
620,332 bytes, sha256

```
cc5880ac28d3d9af4b0fb54f913cf0464e2229c276595e905312c904b5549f96
```

(also in `sat_k54/fq1_k54_instance.cnf.sha256`). It was written on 2026-09-11 by
`sat_k54/fq1_dump_instance.py`, which is the encoder with the solve block replaced by a DIMACS
dump; its variable and clause counts equal the counts the running solver process printed at
launch on 2026-08-21 (`run_record/run_unsat54.log`). On 2026-09-20 the dump script was run again
from this repository's copy (PySAT 1.9.dev15) and produced a byte-identical file with the same
sha256. The variable numbering is PySAT's: variables 1..377 are the vertex variables in the order
the encoder enumerates the vertices (increasing integer value of the string read as an ordinary
binary number, leftmost character most significant; the script writes strings with Python's
`format(v, "012b")`), then the sequential-counter auxiliaries, then the lex-leader chain
variables.

Reproducing the instance needs `python-sat` (`pip install python-sat`); the runs used PySAT
1.9.dev15 with its bundled CaDiCaL 1.9.5. Then:

```
cd sat_k54
python3 fq1_dump_instance.py 54
shasum -a 256 -c fq1_k54_instance.cnf.sha256
```

### Encoding sanity check

Before the k = 54 run was launched on 2026-08-21, the same encoder was run with k = 70: CaDiCaL
returned SAT in 33 seconds and the witness was independently re-verified as a dominating set
(0 uncovered vertices). This is recorded in `run_record/RUN_PLAN.md` (the pre-registered plan)
and in the project ledger. The k = 70 witness file itself (`domset_70.txt`, which the script
writes next to itself) is not on disk any more and is therefore not in this deposit; the
sanity check is reported here from the plan's record, not from a file you can re-check.

### Run record

CaDiCaL 1.9.5 via PySAT 1.9.dev15, one process on one core, no proof logging, started
Fri 2026-08-21 03:12:50 PDT on the author's machine (macOS, Python 3.13.1) and terminated with SIGTERM
at the author's instruction on Sun 2026-09-20 01:45:35 PDT, after an elapsed time of 29 days
22 hours 32 minutes and 45 seconds and 42,622 minutes 50.76 seconds of CPU time (710.4 CPU-hours),
resident set 4.14 GB at the end. It produced NO decision: no SAT, no UNSAT, no witness, no proof
log. The solver prints nothing until it decides, so the log (`run_record/run_unsat54.log`) holds
only the two launch lines (the first launch was killed with its terminal session and relaunched
detached; the `setsid: command not found` line is the relaunch shell's, harmless) and the
watcher's end-of-run note (`run_record/ENDED_8014.txt`) records "none (process died without an
answer)". `run_record/final_ps_8014.txt` is the last `ps` line (PID, elapsed, CPU time, RSS in
KB).

An interrupted CDCL run proves nothing. 710 CPU-hours without a decision is a fact about this
encoding and this solver on this machine, not evidence about the answer in either direction
(CDCL run times are heavy-tailed). This deposit changes no bound: 54 <= gamma(Gamma_12) <= 59
stands exactly as on A291295, with the 54 from the 2018 paper and the 59 from section 3.

The rest of `run_record/`: `RUN_PLAN.md` (the plan written before launch; its CNF size figures
describe an earlier encoding, see the note at its end), `KEEP_DECISION_2026-09-11.md` (the day-21
decision to keep the run going, with the identity of the instance and the watcher),
`watch_8014.sh` (the watcher), `CLOSEOUT_2026-09-20.md` (the termination record). Four public
copies carry a small documented edit, each with the original file's sha256 in the file itself:
`sat_k54/fq1_unsat54.py` (one em dash in a print string replaced by a hyphen),
`run_record/RUN_PLAN.md` (same, in the title line), `run_record/KEEP_DECISION_2026-09-11.md`
(one local absolute path replaced by a placeholder) and `witness/verify_59set.py` (the
certificate path is now an argument instead of a hard-coded local path). Everything else is
byte-identical to the project files.

## 5. What a checkable continuation would look like

The run above had two defects that a continuation should fix: nothing persisted between the
start and the end, and even an UNSAT answer would not have been independently checkable because
no proof was logged. The recommended form (from `run_record/KEEP_DECISION_2026-09-11.md`,
section 5) is cube-and-conquer with DRAT proof logging:

1. Take `sat_k54/fq1_k54_instance.cnf` (check the hash first).
2. Split it into cubes with a lookahead splitter (march_cu, or CaDiCaL's own cubing mode),
   writing the cube list to disk.
3. Solve the cubes one at a time (or in parallel), each with a proof log (CaDiCaL with a DRAT
   output, or any solver that emits DRAT/LRAT), appending each cube's verdict and its checked
   proof status to a results file as it finishes. Progress then lives on disk: a reboot loses
   only the cube in flight.
4. UNSAT of every cube, each with a proof checked by drat-trim or cake_lpr, is a checkable proof
   that no dominating set of at most 54 vertices exists (gamma(Gamma_12) >= 55). Any SAT cube
   gives a 54-vertex witness, to be re-verified with the from-definition checker in
   `witness/verify_59set.py` (it accepts any certificate file; it asserts 59 lines, so change
   that one assertion to 54, or better, write a fresh checker).

Nothing in this repository has done any of this. The cube depth, the order and the per-cube time
cap would need their own plan before such a run is started.

## 6. Layout

```
README.md                      this file
LICENSE                        MIT for code, CC BY 4.0 for data, run records and text
LICENSE-CC-BY-4.0.txt          the CC BY 4.0 legal text
CITATION.cff, .zenodo.json     citation metadata
MANIFEST.sha256                sha256 of every other file (sha256sum -c MANIFEST.sha256)
verify.sh                      manifest + instance hash + 59-set verifier
witness/gamma12_domset_59.txt  the 59-vertex dominating set (sha256 ebc0c788...)
witness/verify_59set.py        from-definition verifier
sat_k54/fq1_unsat54.py         encoder + solver script (as run, one print string edited)
sat_k54/fq1_dump_instance.py   encoder with the solve replaced by a DIMACS dump
sat_k54/fq1_k54_instance.cnf   the exact k = 54 instance (sha256 cc5880ac...)
sat_k54/fq1_k54_instance.cnf.sha256
run_record/                    log, watcher note, final ps line, plan, decision, closeout
docs/oeis_fetch_2026-09-20/    verbatim fetches of A291295 (text format) and its a-file
docs/reference_fetch_2026-09-20/  Crossref record and journal landing page of the 2018 paper
```

## 7. Disclosure

Code and text in this repository were prepared with Claude (Anthropic) under Tyler Satchel Orden's
direction; the computations were run on his machine. Every number quoted above traces to a file in
this repository or to the fetches saved under `docs/`.

## 8. License

Code (`*.py`, `*.sh`): MIT. Data, run records and text (the CNF instance, the witness, the
`*.md`, `*.txt`, `*.log` and `*.sha256` files): CC BY 4.0. See `LICENSE`. `CITATION.cff` and
`.zenodo.json` carry the single SPDX identifier MIT, which is the code license; the data license
is stated here and in `LICENSE`. The fetched OEIS files keep the OEIS End-User License Agreement.

## 9. Citing

See `CITATION.cff`. For the 59-set, cite OEIS A291295 (the a-file and the comment of Sep 06 2026).
For the 2018 bounds, cite Azarija, Klavžar, Rho and Sim as in section 2.
