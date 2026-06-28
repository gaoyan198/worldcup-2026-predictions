#!/usr/bin/env python3
"""
THE FIRST-PRINCIPLES MODEL  ("Six Forces")
==========================================
No Elo. No betting odds. No FIFA ranking. Nothing borrowed.

Premise: a World Cup is not won by the "best team on paper." It is won by the
team that survives SEVEN matches in a specific environment under specific
pressure. So instead of one rating, I decompose championship capacity into the
six forces I believe actually decide it, score every contender myself, then
let the tournament's brutal arithmetic (you must win ~7 in a row) amplify small
edges the way it does in reality.

The six forces (and why each, in my own words):

  1. TALENT STOCK (T) ......... depth of genuinely elite players, not just a
     star XI. Tournaments expose squads through injury/suspension/fatigue.
  2. PEAK TIMING (P) .......... are the key players ON the 25-29 prime curve
     RIGHT NOW, or side of it? Aging champions decline non-linearly over 7 games.
  3. SYSTEM & MANAGER (S) ..... a settled, coherent tactical identity beats
     assembled talent. Chaos loses in June.
  4. KNOCKOUT DNA (K) ......... penalties, game-state management, the proven
     ability to win ugly 1-0. Heavily weighted: knockouts, not group play,
     crown champions.
  5. ENVIRONMENTAL FIT (E) .... *** my edge over every standard model ***
     2026 is played in extreme NA summer heat + altitude (Mexico City 2240m,
     Guadalajara 1560m, Monterrey/Dallas/Houston furnace) across huge travel
     distances. The June-2025 Club World Cup already showed European sides
     wilting. Standard models weight this at ZERO. I don't.
  6. PATH & VARIANCE (V) ...... draw luck + a team's inherent result variance
     (some squads are high-floor, some are coin-flips).

Each scored 0-10 by me. Weights reflect my belief about what converts talent
into a trophy. Composite -> per-match win probability via logistic ->
Monte Carlo the 7-game gauntlet over the real field.
"""

import math
import random
from collections import defaultdict

random.seed(2026)
N = 200_000

# Weights — my judgement of what wins a World Cup (sum = 1.0).
# Note knockout DNA (.18) + environment (.15) together outweigh raw talent (.26):
# that is the whole thesis. Talent gets you to the quarters; the rest wins it.
W = {"T": 0.26, "P": 0.12, "S": 0.18, "K": 0.18, "E": 0.15, "V": 0.11}

# ---- MY scores. Reasoned per team, not pulled from any rating system. ----
# Columns:                 T    P    S    K    E    V
TEAMS = {
    # --- Top tier ---
    "Spain":        dict(T=9.5, P=9.5, S=9.0, K=7.5, E=8.0, V=7.5),  # young Euro champs, deep, heat-ok
    "France":       dict(T=10.0,P=8.5, S=8.0, K=9.0, E=7.0, V=8.0),  # deepest pool, proven KO, Deschamps last dance
    "Argentina":    dict(T=8.0, P=6.0, S=9.0, K=9.5, E=9.5, V=7.0),  # holders; KO+heat elite but Messi 38, core aged
    "Brazil":       dict(T=8.5, P=8.0, S=6.5, K=6.0, E=9.5, V=6.0),  # talent+climate, but scarred & unstable bench
    "England":      dict(T=9.5, P=9.0, S=7.0, K=6.5, E=6.5, V=6.5),  # talent glut, Tuchel upgrade, KO scar tissue
    # --- Second tier ---
    "Portugal":     dict(T=8.5, P=7.0, S=7.0, K=7.0, E=7.5, V=6.5),  # great cast, Ronaldo 41 drag
    "Germany":      dict(T=8.5, P=8.5, S=7.5, K=6.5, E=6.5, V=6.5),  # Musiala/Wirtz rising, heat-soft
    "Netherlands":  dict(T=8.0, P=7.5, S=7.0, K=6.0, E=6.5, V=6.0),
    # --- Dark / value tier (where my model diverges most) ---
    "Morocco":      dict(T=7.0, P=8.0, S=8.5, K=8.0, E=9.0, V=6.5),  # 2022 SF was no fluke: system+KO+heat
    "Uruguay":      dict(T=7.5, P=7.0, S=8.0, K=7.5, E=9.0, V=6.0),  # Bielsa, SA climate edge, nasty in KO
    "Colombia":     dict(T=7.5, P=7.5, S=7.5, K=6.5, E=9.0, V=6.0),  # long unbeaten runs, climate-built
    "Croatia":      dict(T=7.0, P=5.5, S=8.5, K=9.0, E=6.5, V=6.0),  # KO machine but ancient midfield
    "Belgium":      dict(T=7.5, P=7.0, S=6.5, K=6.0, E=6.5, V=6.0),
    "USA":          dict(T=6.5, P=8.0, S=6.5, K=6.0, E=8.5, V=6.0),  # home crowd+climate, young
    "Mexico":       dict(T=6.0, P=7.0, S=6.5, K=6.0, E=9.5, V=6.0),  # altitude home fortress, low ceiling
    "Japan":        dict(T=7.0, P=8.0, S=8.0, K=6.5, E=6.5, V=6.5),  # best-organised non-elite, heat-ok
    "Switzerland":  dict(T=6.5, P=6.5, S=7.0, K=7.0, E=6.5, V=5.5),
    "Senegal":      dict(T=7.0, P=8.0, S=7.0, K=6.5, E=8.5, V=6.0),
}

FILLER = 3.2  # composite for the ~30 non-contenders that fill the 48-team field

def composite(s):
    return sum(W[k] * s[k] for k in W)

COMP = {t: composite(s) for t, s in TEAMS.items()}

# logistic steepness: calibrated so a 0.2-composite edge ~ 53%, a top side vs
# filler ~ 92%. K-stage variance is real, so I keep it deliberately un-steep.
KSTEEP = 0.62

def win_prob(a, b):
    return 1.0 / (1.0 + math.exp(-KSTEEP * (a - b)))

def play(a, b, ca, cb):
    return a if random.random() < win_prob(ca, cb) else b

def simulate():
    # Build a realistic 32-slot knockout field: all contenders advance (they
    # do, in reality, ~always), padded with filler teams, random bracket.
    field = list(TEAMS)
    pad = 32 - len(field)
    fillers = [f"F{i}" for i in range(pad)]
    comp = dict(COMP)
    for f in fillers:
        # filler strength jittered a little so they aren't identical
        comp[f] = FILLER + random.uniform(-0.3, 0.5)
    bracket = field + fillers
    random.shuffle(bracket)
    # single elimination, 32 -> champion (5 rounds == the knockout gauntlet)
    while len(bracket) > 1:
        nxt = []
        for i in range(0, len(bracket), 2):
            a, b = bracket[i], bracket[i + 1]
            nxt.append(play(a, b, comp[a], comp[b]))
        bracket = nxt
    return bracket[0]

def main():
    champs = defaultdict(int)
    for _ in range(N):
        champs[simulate()] += 1
    rows = [(t, champs[t] / N) for t in TEAMS]
    rows.sort(key=lambda r: r[1], reverse=True)

    print(f"FIRST-PRINCIPLES 'Six Forces' model — {N:,} simulated tournaments\n")
    print(f"{'Team':<13}{'Champ%':>8}  {'Comp':>5} | "
          f"{'T':>4}{'P':>4}{'S':>4}{'K':>4}{'E':>4}{'V':>4}")
    print("-" * 60)
    for t, p in rows:
        s = TEAMS[t]
        print(f"{t:<13}{100*p:>7.1f}  {COMP[t]:>5.2f} | "
              f"{s['T']:>4}{s['P']:>4}{s['S']:>4}{s['K']:>4}{s['E']:>4}{s['V']:>4}")
    field_p = 1 - sum(p for _, p in rows)
    print("-" * 60)
    print(f"{'(field)':<13}{100*field_p:>7.1f}   <- all non-contender teams combined")

if __name__ == "__main__":
    main()
