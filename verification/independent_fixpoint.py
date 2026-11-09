"""Independent standard-library implementation of Definition 3.1.

Run: python3 independent_fixpoint.py > independent_results.json
Positions are 1..5; colours are 0..5. Only colour symmetry is used.
"""

import itertools
import json
import re
from functools import lru_cache


TRANSCRIPTIONS = {
    'I': '''
    (12)(35) (13)(35) (15)(35) (23)(35) (25)(35) [35]
    (12)(25) (15)(25) (13)(25) (14)(25) (23)(25) (24)(25) [25]
    (12)(24) (13)(24) (15)(24) (23)(24)
    (12)(14) (14)(23) (14)(15) (13)(14)
    (12)(13) (13)(15) (13)(23) [13]''',
    'II': '''
    (12)(35) (13)(35) (15)(35) (23)(35) (25)(35) [35]
    (12)(25) (13)(25) (14)(25) (15)(25) (23)(25) (24)(25) [25]
    (12)(24) (13)(24) (14)(24) (15)(24) (23)(24) [24]
    (12)(14) (13)(14) (14)(15) (14)(23) [14]
    (12)(13) (13)(15) (13)(23) [13]''',
    'IV': '''
    (12)(35) (13)(35) (15)(35) (23)(35) (24)(35) (25)(35) (34)(35)
    (12)(25) (13)(25) (14)(25) (15)(25) (23)(25) (24)(25) (25)(34) [25]
    (12)(24) (13)(24) (14)(24) (15)(24) (23)(24) (24)(34) [24]
    (12)(14) (13)(14) (14)(15) (14)(23) (14)(34)
    (12)(13) (13)(15) (13)(23) (13)(34) [13]''',
    'XII': '''
    (12)(35) (13)(35) (25)(35) (14)(35) (15)(35) (23)(35) (24)(35) (34)(35) (35)(45) [35]
    (12)(25) (13)(25) (14)(25) (15)(25) (23)(25) (24)(25) (25)(34) (25)(45) [25]
    (12)(24) (13)(24) (14)(24) (15)(24) (23)(24) (24)(34) (24)(45) [24]
    (12)(14) (13)(14) (14)(15) (14)(23) (14)(34) (14)(45) [14]
    (12)(13) (13)(15) (13)(23) (13)(34) (13)(45) [13]''',
    'XIII-R': '''
    (12)(35) (15)(35) (23)(35) (25)(35) (34)(35)
    (12)(45) (15)(45) (23)(45) (25)(45) (34)(45)
    (12)(24) (15)(24) (23)(24) (24)(25) (24)(34)
    (12)(13) (13)(15) (13)(23) (13)(25) (13)(34)
    (12)(14) (14)(15) (14)(23) (14)(25) (14)(34)
    (12345)''',
    'XIII-L': '''
    (13)(35) (14)(35) (24)(35) (35)(45) [35]
    (13)(45) (14)(45) (24)(45) [45]
    (13)(24) (14)(24) [24]
    (13)(14) [14]
    [13]
    (12)(15) (12)(23) (12)(34) (12)(45) [12]
    (15)(23) (23)(34) (23)(45) [23]
    (15)(34) (34)(45) [34]
    (15)(45) [45]
    [15]''',
    'C5': '''
    (12)(15) (12)(23) (12)(34) (12)(45) [12]
    (15)(23) (23)(34) (23)(45) [23]
    (15)(34) (34)(45) [34]
    (15)(45) [45] [15] (12345)''',
}


def parse(text):
    tokens = re.findall(r'\(12345\)|\[\d\d\]|\(\d\d\)\(\d\d\)', text)
    result = set()
    for token in tokens:
        if token == '(12345)':
            result.add(token)
        elif token.startswith('['):
            result.add(token)
        else:
            first, second = sorted(re.findall(r'\d\d', token))
            result.add(f'({first})({second})')
    # In [4, Appendix, p. 22], XIII L* lists [45] in both 5-cliques (30 tokens, 29 distinct types).
    assert len(tokens) == len(result) or (tokens.count('[45]') == 2 and len(tokens) == len(result) + 1)
    return result


def case_sets():
    cases = {name: parse(text) for name, text in TRANSCRIPTIONS.items()}
    cases['III'] = cases['IV'] - {'[24]'} | {'[14]'}
    cases['V'] = cases['IV'] | {'[14]'}
    cases['VI'] = cases['V'] - {'[24]'} | {'[35]'}
    cases['VII'] = cases['V'] | {'[35]'}
    cases['VIII'] = cases['XII'] - {'[35]', '[24]', '[14]', '(14)(24)'}
    cases['IX'] = cases['VIII'] | {'[35]'}
    cases['X'] = cases['XII'] - {'[35]', '[24]'}
    cases['XI'] = cases['XII'] - {'[35]'}
    return cases


PAIRS = tuple(itertools.combinations(range(6), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
PRESERVED = tuple(tuple(index for index, other in enumerate(PAIRS)
                        if pair == other or set(pair).isdisjoint(other))
                  for pair in PAIRS)


def boundary_type(boundary):
    supports = [tuple(position + 1 for position, label in enumerate(boundary)
                      if colour in label) for colour in range(6)]
    assert sorted(map(len, supports)) in ([1, 1, 1, 1, 1, 5], [1, 1, 1, 1, 3, 3])
    if any(len(support) == 5 for support in supports):
        return '(12345)'
    missing = sorted(''.join(str(position) for position in range(1, 6)
                             if position not in support)
                     for support in supports if len(support) == 3)
    return f'[{missing[0]}]' if missing[0] == missing[1] else f'({missing[0]})({missing[1]})'


@lru_cache(None)
def normalize(boundary):
    masks = [sum(1 << position for position, label in enumerate(boundary)
                 if colour in label) for colour in range(6)]
    order = sorted(range(6), key=lambda colour: (masks[colour], colour))
    mapping = tuple(order.index(colour) for colour in range(6))
    normalized = tuple(tuple(sorted(mapping[colour] for colour in label))
                       for label in boundary)
    return normalized, mapping


def representative(type_name):
    if type_name == '(12345)':
        boundary = tuple((0, colour) for colour in range(1, 6))
    else:
        missing = re.findall(r'\d\d', type_name)
        if type_name.startswith('['):
            missing *= 2
        labels = [[colour for colour in range(2) if str(position) not in missing[colour]]
                  for position in range(1, 6)]
        next_colour = 2
        for label in labels:
            while len(label) < 2:
                label.append(next_colour)
                next_colour += 1
        assert next_colour == 6
        boundary = tuple(tuple(label) for label in labels)
    boundary = normalize(boundary)[0]
    assert boundary_type(boundary) == type_name
    return boundary


def endpoint_set(boundary, pair):
    return tuple(position for position, label in enumerate(boundary)
                 if len(set(label).intersection(pair)) == 1)


def matchings(endpoints):
    if not endpoints:
        return ((),)
    first, *remaining = endpoints
    result = []
    for partner in remaining:
        rest = tuple(position for position in remaining if position != partner)
        for matching in matchings(rest):
            result.append(tuple(sorted(((first, partner),) + matching)))
    return tuple(result)


def switch(boundary, pair, block):
    first, second = pair
    return tuple(tuple(sorted(second if colour == first else first if colour == second else colour
                              for colour in label)) if position in block else label
                 for position, label in enumerate(boundary))


def compute(types):
    boundaries = {type_name: representative(type_name) for type_name in sorted(types)}
    states = {}
    actions = {}
    initial_counts = {}
    for type_name, boundary in boundaries.items():
        options = []
        for pair_index, pair in enumerate(PAIRS):
            allowed = []
            for matching in matchings(endpoint_set(boundary, pair)):
                if all(boundary_type(switch(boundary, pair, block)) in types for block in matching):
                    allowed.append(matching)
                    for block in matching:
                        target, mapping = normalize(switch(boundary, pair, block))
                        target_type = boundary_type(target)
                        assert target == boundaries[target_type]
                        mapped_pair = PAIR_INDEX[tuple(sorted(mapping[colour] for colour in pair))]
                        source_indices = tuple(PAIR_INDEX[tuple(sorted(mapping.index(colour) for colour in PAIRS[index]))]
                                               for index in PRESERVED[mapped_pair])
                        actions[type_name, pair_index, block] = (target_type, mapped_pair, source_indices)
            options.append(allowed)
        states[type_name] = set(itertools.product(*options))
        initial_counts[type_name] = len(states[type_name])
    rounds = []
    labelled_rounds = []
    empty_by_round = [sorted(type_name for type_name, family in states.items() if not family)]
    weights = {}
    for type_name, boundary in boundaries.items():
        masks = [sum(1 << position for position, label in enumerate(boundary)
                     if colour in label) for colour in range(6)]
        stabilizer = 1
        for mask in set(masks):
            for factor in range(2, masks.count(mask) + 1):
                stabilizer *= factor
        weights[type_name] = 720 // stabilizer
    while True:
        projections = {(type_name, pair_index):
                       {tuple(state[index] for index in PRESERVED[pair_index]) for state in family}
                       for type_name, family in states.items() for pair_index in range(15)}
        next_states = {}
        for type_name, family in states.items():
            survivors = set()
            for state in family:
                valid = True
                for pair_index, matching in enumerate(state):
                    for block in matching:
                        target_type, mapped_pair, source_indices = actions[type_name, pair_index, block]
                        required = tuple(state[index] for index in source_indices)
                        if required not in projections[target_type, mapped_pair]:
                            valid = False
                            break
                    if not valid:
                        break
                if valid:
                    survivors.add(state)
            next_states[type_name] = survivors
        deleted = sum(map(len, states.values())) - sum(map(len, next_states.values()))
        labelled_rounds.append(sum(weights[type_name] * (len(states[type_name]) - len(next_states[type_name]))
                                   for type_name in types))
        rounds.append(deleted)
        states = next_states
        empty_by_round.append(sorted(type_name for type_name, family in states.items() if not family))
        if not deleted:
            break
    return {'type_count': len(types), 'initial_states': sum(initial_counts.values()),
            'deleted_per_round': rounds, 'final_states': sum(map(len, states.values())),
            'empty_fibres': sorted(type_name for type_name, family in states.items() if not family),
            'initial_per_type': initial_counts,
            'labelled_boundaries': sum(weights.values()),
            'labelled_initial_states': sum(weights[type_name] * initial_counts[type_name] for type_name in types),
            'labelled_deleted_per_round': labelled_rounds,
            'labelled_final_states': sum(weights[type_name] * len(states[type_name]) for type_name in types),
            'empty_by_round': empty_by_round,
            'final_per_type': {type_name: len(family) for type_name, family in states.items()}}


def check_hand_calculations():
    boundary = ((0, 1), (0, 2), (1, 3), (1, 4), (0, 5))
    table = []
    for pair in ((0, 3), (1, 2), (1, 5)):
        for route in matchings(endpoint_set(boundary, pair)):
            outcomes = [boundary_type(switch(boundary, pair, block)) for block in route]
            assert outcomes[0] == outcomes[1]
            table.append({'pair': pair, 'route': [[position + 1 for position in block] for block in route],
                          'outcome': outcomes[0]})
    doubles = []
    for first_route, second_pair, second_route in (
            (((0, 2), (1, 4)), (1, 2), ((0, 3), (1, 2))),
            (((0, 4), (1, 2)), (1, 5), ((0, 2), (3, 4)))):
        outcomes = sorted({boundary_type(switch(switch(boundary, (0, 3), first), second_pair, second))
                           for first in first_route for second in second_route})
        doubles.append(outcomes)
    assert doubles == [['(14)(35)'], ['[24]']]
    return {'route_table': table, 'double_outcomes': doubles}


def self_checks():
    observed = {}
    for boundary in itertools.product(tuple(itertools.combinations(range(6), 2)), repeat=5):
        counts = [sum(colour in label for label in boundary) for colour in range(6)]
        if any(count % 2 == 0 for count in counts):
            continue
        type_name = boundary_type(boundary)
        normalized = normalize(boundary)[0]
        assert normalized == representative(type_name)
        observed[type_name] = observed.get(type_name, 0) + 1
    assert len(observed) == 56
    normalize.cache_clear()
    return {'labelled_boundary_counts': observed,
            'labelled_boundary_total': sum(observed.values()),
            'all_56_types_single_colour_orbits': True}


def cycle_check():
    labels = tuple(itertools.combinations(range(6), 2))
    disjoint = {label: tuple(other for other in labels if set(label).isdisjoint(other)) for label in labels}
    found = set()
    colourings = 0
    for first in labels:
        for second in disjoint[first]:
            for third in disjoint[second]:
                for fourth in disjoint[third]:
                    for fifth in disjoint[fourth]:
                        if not set(fifth).isdisjoint(first):
                            continue
                        internal = (first, second, third, fourth, fifth)
                        boundary = tuple(tuple(colour for colour in range(6)
                                               if colour not in internal[position - 1] and colour not in internal[position])
                                         for position in range(5))
                        found.add(boundary_type(boundary))
                        colourings += 1
    assert found == case_sets()['C5']
    return {'colourings': colourings, 'types': sorted(found)}


def weak_closure_check(types):
    failures = 0
    for type_name in sorted(types):
        boundary = representative(type_name)
        active = [pair for pair in PAIRS if endpoint_set(boundary, pair)]
        for first in active:
            first_blocks = [route[0] for route in matchings(endpoint_set(boundary, first))]
            if not any(boundary_type(switch(boundary, first, block)) in types for block in first_blocks):
                failures += 1
            for second in active:
                if not set(first).isdisjoint(second):
                    continue
                second_blocks = [route[0] for route in matchings(endpoint_set(boundary, second))]
                valid = False
                for first_block, second_block in itertools.product(first_blocks, second_blocks):
                    changed = switch(boundary, first, first_block)
                    alone = switch(boundary, second, second_block)
                    twice = switch(changed, second, second_block)
                    if all(boundary_type(candidate) in types for candidate in (changed, alone, twice)):
                        valid = True
                        break
                if not valid:
                    failures += 1
    return failures


if __name__ == '__main__':
    result = {'self_checks': self_checks(), 'hand_checks': check_hand_calculations(),
              'cycle_check': cycle_check(), 'cases': {}}
    result['weak_closure_failures'] = {name: weak_closure_check(case_sets()[name])
                                       for name in ('I', 'II', 'III', 'VI', 'XIII-R', 'XIII-L')}
    for name, types in case_sets().items():
        result['cases'][name] = compute(types)
    print(json.dumps(result, indent=2))
