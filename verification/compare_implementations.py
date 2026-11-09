#!/usr/bin/env python3
"""Compare case_results.json (labelled implementation) with independent_results.json."""
import json
d = json.load(open('independent_results.json'))['cases']; a = json.load(open('case_results.json'))
m = {'XIII-R': 'XIII_R', 'XIII-L': 'XIII_L', 'C5': 'CYCLE_R'}
ok = True
for k, x in d.items():
    y = a[m.get(k, k)]
    lhs = (x['labelled_boundaries'], x['labelled_initial_states'], [v for v in x['labelled_deleted_per_round'] if v], x['labelled_final_states'], sorted(x['empty_fibres']))
    rhs = (y['labelled_boundaries'], y['initial_states'], y['deleted_per_round'], y['final_states'], sorted(y['empty_fibres']))
    print(k, lhs == rhs); ok &= lhs == rhs
print("ALL_MATCH" if ok else "MISMATCH")
