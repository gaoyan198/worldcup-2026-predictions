#!/usr/bin/env python3
"""
2026 FIFA World Cup Monte Carlo tournament simulator.

Model:
  - Team strength = World Football Elo Ratings (eloratings.net), data/world_elo.tsv
  - Hosts (US, MX, CA) get +100 Elo in group stage (all home games), +50 in knockouts
  - Goals per match drawn from Poisson with rates derived from Elo difference
    (lambda = BASE_GOALS * 10^(+/- d / GOAL_SCALE)), which yields realistic
    win/draw/loss splits and goal differences for tiebreaks
  - Real 2026 format: 12 groups of 4 -> top 2 + 8 best 3rds -> round of 32
    with the official FIFA bracket (matches 73-104) and third-place
    eligibility sets per match (assignment solved by randomized backtracking)
  - Knockouts: Poisson goals; if level after 90', winner drawn from Elo win
    expectancy with the margin damped (extra time / shootout randomness)
"""

import csv
import math
import random
import sys
from collections import defaultdict

N_SIMS = int(sys.argv[1]) if len(sys.argv) > 1 else 50_000
random.seed(2026)

HOSTS = {"US", "MX", "CA"}
HOME_ELO_GROUP = 100
HOME_ELO_KO = 50
BASE_GOALS = 1.35
GOAL_SCALE = 850
KO_DAMP = 0.7  # damping of Elo edge in ET/shootout

GROUPS = {
    "A": ["MX", "ZA", "KR", "CZ"],
    "B": ["CA", "BA", "QA", "CH"],
    "C": ["BR", "MA", "HT", "SQ"],
    "D": ["US", "PY", "AU", "TR"],
    "E": ["DE", "CW", "CI", "EC"],
    "F": ["NL", "JP", "SE", "TN"],
    "G": ["BE", "EG", "IR", "NZ"],
    "H": ["ES", "CV", "SA", "UY"],
    "I": ["FR", "SN", "IQ", "NO"],
    "J": ["AR", "DZ", "AT", "JO"],
    "K": ["PT", "CD", "UZ", "CO"],
    "L": ["EN", "HR", "GH", "PA"],
}

# Round of 32 (official matches 73-88).
# ("W", g) = group winner, ("R", g) = runner-up, ("T", groups) = best 3rd from set
R32 = {
    73: (("R", "A"), ("R", "B")),
    74: (("W", "E"), ("T", "ABCDF")),
    75: (("W", "F"), ("R", "C")),
    76: (("W", "C"), ("R", "F")),
    77: (("W", "I"), ("T", "CDFGH")),
    78: (("R", "E"), ("R", "I")),
    79: (("W", "A"), ("T", "CEFHI")),
    80: (("W", "L"), ("T", "EHIJK")),
    81: (("W", "D"), ("T", "BEFIJ")),
    82: (("W", "G"), ("T", "AEHIJ")),
    83: (("R", "K"), ("R", "L")),
    84: (("W", "H"), ("R", "J")),
    85: (("W", "B"), ("T", "EFGIJ")),
    86: (("W", "J"), ("R", "H")),
    87: (("W", "K"), ("T", "DEIJL")),
    88: (("R", "D"), ("R", "G")),
}
R16 = {89: (74, 77), 90: (73, 75), 91: (76, 78), 92: (79, 80),
       93: (83, 84), 94: (81, 82), 95: (86, 88), 96: (85, 87)}
QF = {97: (89, 90), 98: (93, 94), 99: (91, 92), 100: (95, 96)}
SF = {101: (97, 98), 102: (99, 100)}

THIRD_SLOTS = [(m, set(R32[m][1][1])) for m in (74, 77, 79, 80, 81, 82, 85, 87)]


def load_data():
    names = {}
    with open("data/teams.tsv") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2:
                names[row[0]] = row[1]
    elo = {}
    with open("data/world_elo.tsv") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 4:
                elo[row[2]] = int(row[3])
    return names, elo


def match_goals(elo_a, elo_b):
    d = elo_a - elo_b
    la = BASE_GOALS * 10 ** (d / GOAL_SCALE)
    lb = BASE_GOALS * 10 ** (-d / GOAL_SCALE)
    return poisson(la), poisson(lb)


def poisson(lam):
    # Knuth
    L = math.exp(-lam)
    k, p = 0, 1.0
    while True:
        p *= random.random()
        if p <= L:
            return k
        k += 1


def eff_elo(team, elo, knockout):
    bonus = (HOME_ELO_KO if knockout else HOME_ELO_GROUP) if team in HOSTS else 0
    return elo[team] + bonus


def sim_group(teams, elo):
    pts = defaultdict(int)
    gd = defaultdict(int)
    gf = defaultdict(int)
    for i in range(4):
        for j in range(i + 1, 4):
            a, b = teams[i], teams[j]
            ga, gb = match_goals(eff_elo(a, elo, False), eff_elo(b, elo, False))
            gd[a] += ga - gb
            gd[b] += gb - ga
            gf[a] += ga
            gf[b] += gb
            if ga > gb:
                pts[a] += 3
            elif gb > ga:
                pts[b] += 3
            else:
                pts[a] += 1
                pts[b] += 1
    return sorted(teams, key=lambda t: (pts[t], gd[t], gf[t], random.random()),
                  reverse=True), pts, gd, gf


def assign_thirds(third_by_group):
    """third_by_group: dict group_letter -> team for the 8 qualified 3rds.
    Randomized backtracking over the official eligibility sets."""
    slots = THIRD_SLOTS[:]
    groups = list(third_by_group)

    def bt(i, used):
        if i == len(slots):
            return {}
        m, allowed = slots[i]
        cands = [g for g in groups if g not in used and g in allowed]
        random.shuffle(cands)
        for g in cands:
            rest = bt(i + 1, used | {g})
            if rest is not None:
                rest[m] = third_by_group[g]
                return rest
        return None

    res = bt(0, frozenset())
    if res is None:  # combination not coverable by sets; relax (rare)
        res, pool = {}, dict(third_by_group)
        for m, allowed in slots:
            g = next((g for g in pool if g in allowed), next(iter(pool)))
            res[m] = pool.pop(g)
    return res


def sim_ko_match(a, b, elo):
    ea, eb = eff_elo(a, elo, True), eff_elo(b, elo, True)
    ga, gb = match_goals(ea, eb)
    if ga != gb:
        return a if ga > gb else b
    we = 1 / (1 + 10 ** (-KO_DAMP * (ea - eb) / 400))
    return a if random.random() < we else b


def sim_tournament(elo, counters):
    winners, runners = {}, {}
    thirds = []  # (group, team, pts, gd, gf)
    for g, teams in GROUPS.items():
        order, pts, gd, gf = sim_group(teams, elo)
        winners[g], runners[g] = order[0], order[1]
        t = order[2]
        thirds.append((g, t, pts[t], gd[t], gf[t]))
    thirds.sort(key=lambda x: (x[2], x[3], x[4], random.random()), reverse=True)
    best8 = {g: t for g, t, *_ in thirds[:8]}
    third_slot = assign_thirds(best8)

    r32_teams = {}
    for m, (s1, s2) in R32.items():
        t1 = winners[s1[1]] if s1[0] == "W" else runners[s1[1]] if s1[0] == "R" else third_slot[m]
        t2 = winners[s2[1]] if s2[0] == "W" else runners[s2[1]] if s2[0] == "R" else third_slot[m]
        r32_teams[m] = (t1, t2)

    for t1, t2 in r32_teams.values():
        counters["r32"][t1] += 1
        counters["r32"][t2] += 1

    res = {m: sim_ko_match(t1, t2, elo) for m, (t1, t2) in r32_teams.items()}
    for stage, rnd in (("r16", R16), ("qf", QF), ("sf", SF)):
        nxt = {}
        for m, (m1, m2) in rnd.items():
            counters[stage][res[m1]] += 1
            counters[stage][res[m2]] += 1
            nxt[m] = sim_ko_match(res[m1], res[m2], elo)
        res = nxt
    f1, f2 = res[101], res[102]
    counters["final"][f1] += 1
    counters["final"][f2] += 1
    counters["champion"][sim_ko_match(f1, f2, elo)] += 1


def main():
    names, elo = load_data()
    missing = [t for g in GROUPS.values() for t in g if t not in elo]
    if missing:
        sys.exit(f"missing Elo for: {missing}")

    counters = {k: defaultdict(int) for k in ("r32", "r16", "qf", "sf", "final", "champion")}
    for _ in range(N_SIMS):
        sim_tournament(elo, counters)

    rows = []
    for g, teams in GROUPS.items():
        for t in teams:
            rows.append((t, g))
    rows.sort(key=lambda r: counters["champion"][r[0]], reverse=True)

    print(f"2026 World Cup — {N_SIMS:,} Monte Carlo simulations (Elo as of run date)\n")
    print(f"{'Team':<22}{'Grp':<5}{'Elo':>5} {'R32%':>7}{'R16%':>7}{'QF%':>7}{'SF%':>7}{'Final%':>8}{'Champ%':>8}")
    for t, g in rows:
        n = names.get(t, t)
        print(f"{n:<22}{g:<5}{elo[t]:>5}"
              f"{100*counters['r32'][t]/N_SIMS:>7.1f}{100*counters['r16'][t]/N_SIMS:>7.1f}"
              f"{100*counters['qf'][t]/N_SIMS:>7.1f}{100*counters['sf'][t]/N_SIMS:>7.1f}"
              f"{100*counters['final'][t]/N_SIMS:>8.1f}{100*counters['champion'][t]/N_SIMS:>8.2f}")


if __name__ == "__main__":
    main()
