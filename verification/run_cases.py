#!/usr/bin/env python3
import json, time
from mmt_cases import CASES
from kempe_fixpoint import parse, fixpoint, name
res = {}
for k, v in CASES.items():
    t0 = time.time()
    fib, st = fixpoint(parse(v))
    empty = sorted(name(t) for t, n in fib.items() if n == 0)
    res[k] = {"types": len(fib), **st, "empty_fibres": empty,
              "excluded": bool(empty)}
    print(k, len(fib), st["labelled_boundaries"], st["initial_states"], st["deleted_per_round"], st["final_states"], "EXCLUDED" if empty else "survives", empty, f"{time.time()-t0:.1f}s", flush=True)
json.dump(res, open("case_results.json", "w"), indent=1)
