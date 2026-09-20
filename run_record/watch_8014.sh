#!/bin/zsh
# Watcher for the FQ1 k=54 solver (PID 8014), started 2026-09-11 by the main session (own-goal 63 lesson).
# Polls once a minute; when the process is gone it records the moment, the log, and any result file.
cd "$(dirname "$0")"
while kill -0 8014 2>/dev/null; do sleep 60; done
{
  echo "ENDED_AT $(date '+%Y-%m-%d %H:%M:%S %Z')  (watcher noticed within 60 s)"
  echo "LOG_TAIL:"; tail -5 run_unsat54.log
  echo "RESULT_FILES:"; ls -la UNSAT_54.txt domset_54.txt 2>/dev/null || echo "  none (process died without an answer: killed, reboot, or crash)"
  echo "UPTIME: $(uptime)"
} >> ENDED_8014.txt 2>&1
