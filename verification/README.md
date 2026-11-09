# Supplement: route-coherent Kempe closure for the cycle-separating 5-cut cases

All programs use only the Python 3 standard library (tested with Python 3.12 / 3.13). Run them from this directory.

| file | purpose |
|---|---|
| `mmt_cases.py` | Verbatim transcription of the type sets of the Appendix of Máčajová–Mazzuoccolo–Tabarelli, Ars Math. Contemp. 26 (2026) #P2.03: `L*` of Cases I–XII, `R*` of Case XIII, `L*` of Case XIII, and the common `R*` of Cases I–XII (`CYCLE_R`). |
| `kempe_fixpoint.py` | Library: boundaries, types, routes, Kempe switches on boundaries, and the greatest fixed point of the operator Gamma of Definition 3.1 on fully labelled states (no symmetry reduction). |
| `run_cases.py` → `run_cases.log`, `case_results.json` | Computes Table 1 (Propositions 5.1 and 5.2). Runtime about 40 minutes, peak memory about 2 GB. |
| `hand_cases.py` → `hand_cases.log` | Checks the route tables and double-switch outcomes of Propositions 4.1 and 4.2, that the 5-cycle pole has admissible set `CYCLE_R`, that the loops of Case XII are the pentagon S, and that `L*` of Cases IV, IX, XI, XII is disjoint from `CYCLE_R` (inputs to Propositions 6.1 and 6.2). Ends with `HAND_CASES_OK`. |
| `soundness_check.py` → `soundness.log`, `soundness_results.json` | Test of Theorem 3.3: random connected loopless cubic 5-poles (seed 20261105) of orders 7, 9, 11; the exact admissible set is computed by enumerating perfect matchings and all 6-multisets of perfect matchings with every edge and dangling edge of load two; the fixed point is checked to have no empty fibre. Ends with `SOUNDNESS_OK 9`. |
| `independent_fixpoint.py` → `independent_results.json` | A second implementation written independently of the above (own transcription of the Appendix, one colour-normalised boundary per type, colour symmetry only). Its counts times the orbit sizes 720/360/90 reproduce all 15 rows of Table 1 (`L*` of Cases I–XII, `R*` and `L*` of Case XIII, and `CYCLE_R`); it also records the type-level closure test of [4, Section 4.1] (`weak_closure_failures`). |
| `compare_implementations.py` → `compare_implementations.log` | Checks that both implementations give identical labelled counts and empty fibres for all 15 sets of Table 1. Ends with `ALL_MATCH`. |
| `CONTENTS.sha256` | SHA-256 of every other file. |

Reproduce:

```
python3 run_cases.py > run_cases.log
python3 hand_cases.py > hand_cases.log
python3 soundness_check.py > soundness.log
python3 independent_fixpoint.py > independent_results.json
python3 compare_implementations.py > compare_implementations.log
sha256sum -c CONTENTS.sha256     # or: shasum -a 256 -c CONTENTS.sha256
```

Conventions: colours 0–5, positions 1–5 in printed types; a boundary is a 5-tuple of 2-subsets of the colours in which every colour occurs an odd number of times. A case is excluded when some type of the set has an empty fibre in the greatest fixed point; this is a necessary-condition test (Theorem 3.3), so a nonempty fixed point does not imply that the set is realised by a pole.
