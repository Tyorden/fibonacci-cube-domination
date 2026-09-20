# FQ1 k = 54 run: KEEP decision and loss protection (written 2026-09-11 01:11 PDT, main session, Claude Fable 5.1)

Tyler's ruling, Sep 11 2026 about 01:05 PDT: "keep but make sure you document where we are so we
don't lose it." This file is that record. Companion: DECISION_BRIEF_2026-09-11.md (what the run
is and the three options), run_2026-08-21/RUN_PLAN.md (the pre-registered plan), STATUS.md.

## 1. What "where we are" can and cannot mean
The solver is CaDiCaL 1.9.5 inside PySAT 1.9.dev15, one process, one core. It keeps its search
state (learned clauses, phases, restarts) in memory only. Neither CaDiCaL nor PySAT can write
that state to disk and read it back, so THERE IS NO MID-RUN STATE TO SAVE. What can be recorded,
and is recorded below, is everything needed to (a) know the exact question being decided,
(b) notice the moment it ends and capture the answer, and (c) restart the identical question, or
a resumable form of it, if the process is lost.

## 2. Identity of the run (measured 2026-09-11 01:11 PDT)
- Process: PID 8014, started Fri Aug 21 03:12:50 PDT 2026, working directory run_2026-08-21/,
  stdout and stderr both to run_2026-08-21/run_unsat54.log (lsof), stdin /dev/null.
- Command: venv_compute/bin/python fq1_unsat54.py 54 (the process line shows the venv's
  underlying Homebrew Python 3.13.1 binary; pysat is installed only in
  <MathProofs>/venv_compute).
- Elapsed 20 d 21 h 57 m; CPU time 29,961 min (499.4 h); 98 percent of one core; 1.5 GB resident.
- Instance printed by the process at launch: "CNF: 18183 vars, 37713 clauses; K=54".
- Instance of record, regenerated today with the same encoder and the same venv, no solving
  (run_2026-08-21/fq1_dump_instance.py = the launch script with the solve block replaced by a
  DIMACS dump): run_2026-08-21/fq1_k54_instance.cnf, header "p cnf 18183 37713", 620,332 bytes,
  sha256 cc5880ac28d3d9af4b0fb54f913cf0464e2229c276595e905312c904b5549f96
  (run_2026-08-21/fq1_k54_instance.cnf.sha256). Variable and clause counts match the running
  process's own line, so this file is the question PID 8014 is deciding. (The RUN_PLAN's
  "22,231 vars / ~45,700 clauses" describes an earlier encoding; the log and this file are
  authoritative.)
- Encoding (from the script): closed-neighbourhood covering clauses for the 377 vertices of
  Gamma_12; sequential-counter at-most-54 over the 377 vertex variables; lex-leader
  symmetry breaking on the bit-reversal involution (sound for UNSAT). Sanity at launch: K = 70
  SAT in 33 s, witness re-verified as dominating.
- Answer files the script writes when it ends: UNSAT_54.txt (UNSAT) or domset_54.txt (SAT,
  the 54-set as 12-bit strings), plus the final log line "UNSAT in …s" or "SAT in …s".

## 3. What now watches it
- run_2026-08-21/watch_8014.sh, started 2026-09-11 01:11 PDT detached (nohup, PID 89522): polls kill -0 8014
  once a minute; when the process is gone it appends to run_2026-08-21/ENDED_8014.txt the
  time, the last five log lines, the answer files if any (or "none: process died without an
  answer"), and uptime (a fresh uptime means a reboot killed it).
- The watcher itself dies on reboot; that is fine, because a reboot also kills the solver and
  the next session's state check reads both. On any resume: ps -p 8014 -o etime,time and
  cat run_2026-08-21/ENDED_8014.txt.
- Power facts (pmset, Sep 11 01:01 PDT): hibernatemode 3, so sleep pauses the process and it
  resumes on wake; restart, shutdown or a drained battery kills it. The Mac was on battery at
  95 percent at that moment; keep it plugged in.

## 4. If it ends with an answer
Say "fq1 ended". Claude: (1) copies the log and answer file into results/ with the date;
(2) UNSAT: there is no DRAT proof log (the run was started without one), so the statement is
"CaDiCaL 1.9.5 reports UNSAT for the instance with sha256 cc5880ac…" and the honest A291295
follow-up text in staging_2026-08-30/STAGING_NOTES.md applies (bracket [55, 59]); an
independent re-run WITH proof logging (section 6, variant A) is the way to make it checkable;
(3) SAT: verify domset_54.txt independently (every vertex dominated, size 54), then a(12) = 54
exactly and the A291295 DATA edit follows.

## 5. If it is lost (ENDED_8014.txt says no answer, or the PID is gone after a reboot)
Say "fq1 relaunch". Two choices, both from the instance of record:
- Same question, same solver, now with a proof log so an UNSAT is checkable:
    cd paper_prep/FQ1_fibonacci_cube_domination/run_2026-08-21
    shasum -a 256 -c fq1_k54_instance.cnf.sha256
    nohup nice -n 5 ../../../venv_compute/bin/python -c "from pysat.solvers import Cadical195; from pysat.formula import CNF; c=CNF(from_file='fq1_k54_instance.cnf'); s=Cadical195(bootstrap_with=c.clauses, with_proof=True); print('res', s.solve(), flush=True); open('proof_k54.drat','w').write('\n'.join(s.get_proof()))" > relaunch_k54.log 2>&1 &
  (a DRAT proof for a multi-week run can be very large; check free disk first.)
- Resumable form (recommended for a relaunch): cube-and-conquer. Split the instance into
  cubes with a lookahead splitter (march_cu or CaDiCaL's own "cube" mode), write the cube list
  to disk, then solve cubes one at a time, appending each cube's verdict to a results file as it
  finishes. Progress then lives on disk: a reboot loses only the cube in flight. UNSAT of every
  cube = UNSAT of the instance; any SAT cube gives the witness. This needs its own RUN_PLAN
  (cube depth, order, per-cube time cap) before launch, per the campaign rule.

## 6. Nothing else depends on this run
The published bound 54 <= a(12) <= 59 on A291295 (rev. 20, Sep 6) stands either way. No paper,
dashboard card or agent waits on the result. Dashboard: Queue tab, card "FQ1 solver", state WATCH.

(Deposit copy note, 2026-09-20: verbatim except one local absolute path replaced by <MathProofs>/venv_compute; original sha256 cff274f1b0de93f831bd1b83c7d373a92bdce6074b6c83da49569114c519cf11.)
