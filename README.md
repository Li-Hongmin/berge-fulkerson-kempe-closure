# Route-coherent Kempe closure and cycle-separating 5-cuts in a minimum counterexample to the Berge–Fulkerson conjecture

[![verify](https://github.com/Li-Hongmin/berge-fulkerson-kempe-closure/actions/workflows/verify.yml/badge.svg)](https://github.com/Li-Hongmin/berge-fulkerson-kempe-closure/actions/workflows/verify.yml) [![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.24054897-blue)](https://doi.org/10.5281/zenodo.24054897)

**Hongmin Li** (Institute of Science Tokyo; The University of Tokyo) · ORCID [0000-0003-0228-0600](https://orcid.org/0000-0003-0228-0600)

Main result of the manuscript: in a minimum counterexample to the Berge–Fulkerson conjecture that is cyclically 5- but not 6-edge-connected, nine of the 13 cases of Máčajová–Mazzuoccolo–Tabarelli for a cycle-separating 5-edge-cut are impossible, leaving only Cases IV, IX, XI and XII; the six computational exclusions come from a route-coherent Kempe fixed point computed by two independent programs.

- Manuscript on rStation: <https://rstation.ai/problems/math/papers/7/v4> (version 4)
- Archived on Zenodo: concept DOI [10.5281/zenodo.24054897](https://doi.org/10.5281/zenodo.24054897) (all versions); this repository mirrors version 4, DOI [10.5281/zenodo.24054912](https://doi.org/10.5281/zenodo.24054912)

## Contents

- `paper/paper.md`, `paper/berge-fulkerson-kempe-closure.pdf` — the manuscript (version 4).
- `verification/` — the supplement of that version, unpacked unchanged; its own README describes each file.
- `.github/workflows/verify.yml` — reruns every check below on each push.

## What the programs check

| Check | Command (run inside `verification/`) |
|---|---|
| Table 1 (Props 5.1, 5.2): greatest fixed point for all 15 sets (~40 min, ~2 GB) | `python run_cases.py > out_run_cases.log` |
| Props 4.1, 4.2, 6.1, 6.2 inputs: route tables and hand cases | `python hand_cases.py > out_hand_cases.log && grep -q HAND_CASES_OK out_hand_cases.log` |
| Theorem 3.3 soundness test on random cubic 5-poles | `python soundness_check.py > out_soundness.log && grep -q 'SOUNDNESS_OK 9' out_soundness.log` |
| Second independent implementation of Table 1 | `python independent_fixpoint.py > independent_results.json` |
| Cross-check of the two implementations | `python compare_implementations.py > out_compare.log && grep -q ALL_MATCH out_compare.log` |

The programs check the finite and exact computations used in the manuscript; the mathematical arguments are those written in the paper.

## Reproducing

```sh
cd verification
sha256sum -c CONTENTS.sha256      # or: shasum -a 256 -c CONTENTS.sha256
python run_cases.py > out_run_cases.log
python hand_cases.py > out_hand_cases.log && grep -q HAND_CASES_OK out_hand_cases.log
python soundness_check.py > out_soundness.log && grep -q 'SOUNDNESS_OK 9' out_soundness.log
python independent_fixpoint.py > independent_results.json
python compare_implementations.py > out_compare.log && grep -q ALL_MATCH out_compare.log
```

Requirements: Python 3.9+. Run the commands from a copy if you want to keep the recorded outputs untouched.

## Cite

```bibtex
@misc{li2026bergefulkersonkempeclosu,
  author    = {Li, Hongmin},
  title     = {Route-coherent Kempe closure and cycle-separating 5-cuts in a minimum counterexample to the Berge–Fulkerson conjecture},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.24054897},
  url       = {https://doi.org/10.5281/zenodo.24054897}
}
```

## License

Manuscript and data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code: MIT (see `LICENSE`).
