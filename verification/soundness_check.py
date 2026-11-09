#!/usr/bin/env python3
"""Soundness check: for random cubic 5-poles (multigraphs allowed, no loops),
compute the complete set of BF boundary types by exhaustive search and verify
that every type has a nonempty surviving fibre in the fixed point."""
import random, itertools, sys, json
from kempe_fixpoint import fixpoint, btype, name, PAIRS

def random_pole(n, rng):
    # n odd vertices, 5 semiedges at distinct vertices; inner edges pair the remaining stubs
    while True:
        stubs = [v for v in range(n) for _ in range(3)]
        rng.shuffle(stubs)
        term = []
        seen = set()
        rest = []
        for v in stubs:
            if len(term) < 5 and v not in seen:
                term.append(v); seen.add(v)
            else: rest.append(v)
        if len(term) < 5: continue
        rng.shuffle(rest)
        edges = [(rest[i], rest[i+1]) for i in range(0, len(rest), 2)]
        if any(a == b for a, b in edges): continue
        # connected
        adj = {v: set() for v in range(n)}
        for a, b in edges: adj[a].add(b); adj[b].add(a)
        st, comp = [0], {0}
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in comp: comp.add(y); st.append(y)
        if len(comp) == n: return term, edges

def support(term, edges, n):
    """All boundary types of BF colourings = 6-multisets of perfect matchings
    (semiedges allowed) covering every edge and semiedge exactly twice."""
    items = [("s", i, (term[i],)) for i in range(5)] + [("e", j, e) for j, e in enumerate(edges)]
    m = len(items)
    pms = []
    def rec(v, used, chosen):
        while v < n and v in used: v += 1
        if v == n:
            pms.append(frozenset(chosen)); return
        for k, (_, _, ends) in enumerate(items):
            if v in ends and not any(u in used for u in ends):
                rec(v, used | set(ends), chosen + [k])
    rec(0, set(), [])
    types = set()
    load = [0] * m
    pick = []
    def dfs(start):
        if len(pick) == 6:
            if all(x == 2 for x in load):
                B = tuple(frozenset(c for c, M in enumerate(pick) if i in pms_idx[M]) for i in range(5))
                types.add(btype(B))
            return
        rem = 6 - len(pick)
        for idx in range(start, len(pms)):
            M = pms[idx]
            if any(load[k] >= 2 for k in M): continue
            for k in M: load[k] += 1
            pick.append(idx)
            # prune: every item must still be coverable by the remaining (rem - 1) matchings
            if all(load[k] + (rem - 1) >= 2 for k in range(m)):
                dfs(idx)
            pick.pop()
            for k in M: load[k] -= 1
    pms_idx = pms
    dfs(0)
    types.discard(None)
    return frozenset(types)

if __name__ == "__main__":
    rng = random.Random(20261105)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    out = []
    checked = 0
    seen_supports = set()
    while checked < N:
        n = rng.choice([7, 9, 9, 11])
        term, edges = random_pole(n, rng)
        S = support(term, edges, n)
        if not S or S in seen_supports: continue
        seen_supports.add(S)
        fib, rnd = fixpoint(S)
        bad = [name(t) for t, c in fib.items() if c == 0]
        out.append({"n": n, "terminals": term, "edges": edges, "support_size": len(S), "empty": bad})
        print(n, len(S), "OK" if not bad else ("UNSOUND", bad), flush=True)
        assert not bad
        checked += 1
    json.dump(out, open("soundness_results.json", "w"))
    print("SOUNDNESS_OK", checked)
