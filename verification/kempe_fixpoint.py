#!/usr/bin/env python3
"""Greatest-fixed-point test for boundary Kempe actions on cubic 5-poles.

A boundary is a 5-tuple of 2-subsets of the colour set {0,...,5}.  A state is
a boundary together with a routing: for every colour pair {a,b} whose
endpoint set (positions where exactly one of a,b occurs) is nonempty, a
perfect pairing of that endpoint set.  States are labelled (no colour or
position canonicalisation).  Transitions: switching {a,b} on one route path
must lead to a state of the switched boundary that keeps the {a,b}-route
and the routes of all colour pairs disjoint from {a,b}.
Standard library only.
"""
import itertools, re, sys, json

COL = range(6)
PAIRS = [frozenset(p) for p in itertools.combinations(COL, 2)]

def parse(text):
    out = set()
    for tok in re.findall(r"\(\d\d\)\(\d\d\)|\[\d\d\]|\(12345\)", text):
        if tok == "(12345)": out.add("A"); continue
        d = list(map(int, re.findall(r"\d", tok)))
        if len(d) == 2: d = d + d
        p, q = tuple(sorted(d[:2])), tuple(sorted(d[2:]))
        out.add(tuple(sorted((p, q))))
    return frozenset(out)

def btype(B):
    cnt = [sum(c in L for L in B) for c in COL]
    s = sorted(cnt)
    if s == [1, 1, 1, 1, 1, 5]: return "A"
    if s != [1, 1, 1, 1, 3, 3]: return None
    tri = [c for c in COL if cnt[c] == 3]
    miss = [tuple(i + 1 for i in range(5) if c not in B[i]) for c in tri]
    return tuple(sorted(miss))

def ends(B, p):
    a, b = tuple(p)
    return tuple(i for i in range(5) if (a in B[i]) != (b in B[i]))

def pairings(E):
    if len(E) == 2: return [((E[0], E[1]),)]
    a, b, c, d = E
    return [((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))]

def switch(B, p, path):
    a, b = tuple(p)
    out = list(B)
    for i in path:
        L = set(out[i])
        if a in L: L.remove(a); L.add(b)
        else: L.remove(b); L.add(a)
        out[i] = frozenset(L)
    return tuple(out)

ALL_BOUNDARIES = None
def all_boundaries():
    global ALL_BOUNDARIES
    if ALL_BOUNDARIES is None:
        labs = PAIRS
        ALL_BOUNDARIES = [B for B in itertools.product(labs, repeat=5) if btype(B) is not None]
    return ALL_BOUNDARIES

def fixpoint(H, verbose=False):
    """Greatest fixed point.  Returns (fibre size per type, stats)."""
    H = frozenset(H)
    bset = [B for B in all_boundaries() if btype(B) in H]
    states = {}           # boundary -> list of routings (tuple over active pairs)
    active = {}
    for B in bset:
        act = [p for p in PAIRS if ends(B, p)]
        doms = []
        for p in act:
            ok = [r for r in pairings(ends(B, p))
                  if all(btype(switch(B, p, path)) in H for path in r)]
            doms.append(ok)
        active[B] = act
        states[B] = [dict(zip(act, combo)) for combo in itertools.product(*doms)]
    disj = {p: [q for q in PAIRS if not (p & q)] for p in PAIRS}
    stats = {"labelled_boundaries": len(bset),
             "initial_states": sum(len(v) for v in states.values()), "deleted_per_round": []}
    while True:
        # projections available at each boundary for each switched pair
        proj = {}
        for B, rs in states.items():
            for p in active[B]:
                keys = tuple(q for q in [p] + disj[p] if q in rs[0]) if rs else ()
                proj[(B, p)] = {tuple(R[q] for q in keys) for R in rs}
        removed = 0
        new = {}
        for B, rs in states.items():
            keep = []
            for R in rs:
                alive = True
                for p, r in R.items():
                    key = tuple(R[q] for q in [p] + disj[p] if q in R)
                    for path in r:
                        if key not in proj.get((switch(B, p, path), p), ()):
                            alive = False; break
                    if not alive: break
                if alive: keep.append(R)
                else: removed += 1
            new[B] = keep
        states = new
        if removed == 0: break
        stats["deleted_per_round"].append(removed)
        if verbose: print("  removed", removed, file=sys.stderr)
    fib = {t: 0 for t in H}
    for B, rs in states.items(): fib[btype(B)] += len(rs)
    stats["final_states"] = sum(fib.values())
    return fib, stats

def name(t):
    if t == "A": return "(12345)"
    p, q = t
    return f"[{p[0]}{p[1]}]" if p == q else f"({p[0]}{p[1]})({q[0]}{q[1]})"
