#!/usr/bin/env python3
"""Checks of the hand arguments (Propositions 4.1, 4.2, 6.1, 6.2)."""
from mmt_cases import CASES
from kempe_fixpoint import parse, btype, ends, pairings, switch, name
from soundness_check import support

F = frozenset
H = {k: parse(v) for k, v in CASES.items()}

# Proposition 4.1
B = tuple(F((0, i)) for i in range(1, 6))
assert btype(B) == "A" and "A" in H["XIII_R"]
p = F((0, 2))
assert ends(B, p) == (0, 2, 3, 4)
for r in pairings(ends(B, p)):
    ts = {btype(switch(B, p, path)) for path in r}
    assert len(ts) == 1
    t = ts.pop()
    print("XIII route", [tuple(i + 1 for i in q) for q in r], "->", name(t), "in R*:", t in H["XIII_R"])
    assert t not in H["XIII_R"]

# Proposition 4.2
B = (F((0, 1)), F((0, 2)), F((1, 3)), F((1, 4)), F((0, 5)))
assert btype(B) == ((2, 5), (3, 4))
for case in ("III", "VI"):
    S = H[case]
    assert ((2, 5), (3, 4)) in S
    dom = {}
    for pr in ((0, 3), (1, 2), (1, 5)):
        p = F(pr)
        dom[pr] = []
        for r in pairings(ends(B, p)):
            ts = {btype(switch(B, p, path)) for path in r}
            assert len(ts) == 1
            t = ts.pop()
            print(case, pr, [tuple(i + 1 for i in q) for q in r], "->", name(t), t in S)
            if t in S: dom[pr].append(r)
    assert len(dom[(0, 3)]) == 2 and len(dom[(1, 2)]) == 1 and len(dom[(1, 5)]) == 1
    A_, B_ = dom[(0, 3)]
    def two(r1, p1, r2, p2):
        out = set()
        for a in r1:
            for b in r2:
                out.add(btype(switch(switch(B, F(p1), a), F(p2), b)))
        return out
    tA = two(A_, (0, 3), dom[(1, 2)][0], (1, 2)); tB = two(B_, (0, 3), dom[(1, 5)][0], (1, 5))
    print(case, "A+{1,2} ->", [name(t) for t in tA], " B+{1,5} ->", [name(t) for t in tB])
    assert [name(t) for t in tA] == ["(14)(35)"] and [name(t) for t in tB] == ["[24]"]
    assert not (tA & S) and not (tB & S)

# 5-cycle pole: dangling edge i at cycle vertex i-1, cycle edges (i,i+1)
cyc = support([0, 1, 2, 3, 4], [(i, (i + 1) % 5) for i in range(5)], 5)
assert cyc == H["CYCLE_R"], "5-cycle admissible set differs from MMT R*"
print("5-cycle admissible set equals R* of Cases I-XII:", len(cyc), "types")

# Proposition 6.1/6.2 inputs
Sp = {(1, 3), (1, 4), (2, 4), (2, 5), (3, 5)}
loops = {t[0] for t in H["XII"] if t != "A" and t[0] == t[1]}
assert loops == Sp
for c in ("IV", "IX", "XI", "XII"):
    assert not (H[c] & H["CYCLE_R"]), c
print("L* of IV, IX, XI, XII are disjoint from R*; loops of XII =", sorted(loops))
print("HAND_CASES_OK")
