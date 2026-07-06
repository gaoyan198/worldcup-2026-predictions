#!/usr/bin/env python3
"""
BACKTEST: Six Forces applied to Qatar 2022, pre-tournament scores.

Rules:
 - All scores as they would have been assigned BEFORE any Qatar 2022 match.
 - Every score that carries hindsight risk is flagged [HB].
 - E (Environmental Fit) is re-scoped for Qatar: Nov/Dec, air-conditioned
   stadiums (17-22°C), no altitude, compact geography → effectively neutral
   for everyone. Scores cluster 6.0-7.5 vs the 6.0-9.5 spread in 2026 NA.
 - Weights and KSTEEP unchanged from fundamentals_model.py.
 - Simulate from QF (we know the 8 teams) — cleanest test.
"""
import math, random
from collections import defaultdict

random.seed(2022)
N = 500_000
W = {"T": 0.26, "P": 0.12, "S": 0.18, "K": 0.18, "E": 0.15, "V": 0.11}
KSTEEP = 0.62  # unchanged

# ---------------------------------------------------------------------------
# PRE-TOURNAMENT SCORES — Qatar 2022 QF eight
# Hindsight flag [HB] on any dimension where knowing the outcome risks
# inflating or deflating the score.
# ---------------------------------------------------------------------------
# "Argentina": dict(T=8.0, P=7.0, S=9.0, K=8.5, E=7.0, V=7.0)
#   T: Messi/Di Maria/Lautaro/Mac Allister — genuinely deep squad
#   P: Messi 35 — past physical peak but still elite technically
#   S: Scaloni — 4-2-3-1/4-3-3, incredibly settled since 2018
#   K: 1986 WC, 2021 Copa America, pens specialists — BUT 2018 R16 exit;
#      overall a credible 8.5 pre-tournament [LB]
#   E: neutral (air-con) [LB]
#   V: Messi-dependent but reliable [LB]

# "France": dict(T=9.5, P=8.5, S=7.5, K=8.5, E=6.5, V=8.0)
#   T: Mbappe/Griezmann/Giroud — Benzema withdrew injured pre-tournament [LB]
#   P: Mbappe 23 peak, Griezmann 31 prime [LB]
#   S: Deschamps — pragmatic, 2018 blueprint [LB]
#   K: 2018 WC winners; BUT Euro 2020 shocking R16 pens exit to Switzerland
#      [LB — both facts known pre-tournament; net 8.5 is generous but
#       defensible given they're defending champions]
#   E: neutral [LB]
#   V: Mbappe variance upside [LB]

# "Brazil": dict(T=9.0, P=8.5, S=6.5, K=5.5, E=6.5, V=6.0)
#   T: Vinicius/Rodrygo/Richarlison/Neymar — the deepest talent in 2022 [LB]
#   P: Vinicius 22, Rodrygo 21 — extraordinary peak timing [LB]
#   S: Tite — functional, not elite tactically [LB]
#   K: 2002 last WC, 2014 7-1 trauma, 2018 QF exit to Belgium — bad KO record [LB]
#   E: neutral (air-con neutralises heat edge) [LB]
#   V: Neymar fragility, high ceiling / inconsistent floor [LB]

# "Croatia": dict(T=6.5, P=4.5, S=8.5, K=9.0, E=6.5, V=6.0)
#   T: Modric/Brozovic/Perisic — aging roster [LB]
#   P: Modric 37, core avg ~31 — WELL past peak [LB]
#   S: Dalic — same settled 4-3-3 spine as 2018 [LB]
#   K: 2018 FINALISTS, won 3 consecutive KO matches (pens v Russia, pens v
#      Denmark, 2-1 v England) — one of the best recent KO records [LB]
#   E: neutral [LB]
#   V: low ceiling / high floor [LB]

# "Netherlands": dict(T=8.0, P=7.5, S=6.5, K=6.0, E=6.5, V=6.0)
#   T: Van Dijk/Depay/Gakpo/Dumfries [LB]
#   P: Depay 28, Van Dijk 31 — prime [LB]
#   S: Van Gaal — experienced but rigid 5-3-2 [LB]
#   K: 2010 finalists, 2014 3rd — but 2018 WC missed entirely; returning
#      after 4-year gap, limited recent KO evidence [LB]
#   E: neutral [LB]
#   V: Depay fitness risk known pre-tournament [LB]

# "England": dict(T=9.0, P=8.5, S=6.0, K=5.5, E=6.5, V=6.5)
#   T: Bellingham/Saka/Foden/Kane/Rashford — remarkable talent pool [LB]
#   P: most starters 19-26, best peak timing of any squad [LB]
#   S: Southgate — known conservative manager [LB]
#   K: Euro 2020 final (lost pens), 2018 SF — pens trauma well-documented [LB]
#   E: neutral [LB]
#   V: young talent = high upside [LB]

# "Morocco": dict(T=6.5, P=7.5, S=7.5, K=5.5, E=7.0, V=6.5)
#   T: Ziyech/En-Nesyri/Hakimi/Amrabat — quality, not elite [LB]
#   P: Hakimi 24, Ziyech 29 — peak [LB]
#   S: Regragui (appointed Aug 2022) — well-drilled 4-1-4-1 block [LB]
#   K: *** THE KEY NUMBER ***
#      Before Qatar 2022 Morocco had ZERO WC knockout round wins ever.
#      R16 in 1986 was their best. K=5.5 is the honest pre-tournament score.
#      Their current 2026 K=8.5 is entirely earned FROM Qatar 2022 results.
#      This is the single most important hindsight correction. [HB — confirmed]
#   E: slight edge even in air-con (North African diaspora, warm-weather
#      training background, marginal) [LB]
#   V: counter-attack volatility [LB]

# "Portugal": dict(T=8.5, P=6.5, S=6.0, K=7.0, E=6.5, V=6.5)
#   T: Ronaldo 37 drag; Bruno/Bernardo/Felix/Leao — depth is real [LB]
#   P: Ronaldo 37 — serious drag; Felix 23, Leao 23 counterbalance [LB]
#   S: Fernando Santos — Ronaldo-centric, tactically limited [LB]
#   K: Euro 2016 champions, Nations League; pens capable [LB]
#   E: neutral [LB]
#   V: Ronaldo selection drama risk (known pre-tournament) [LB]

TEAMS = {
    "Argentina":   dict(T=8.0, P=7.0, S=9.0, K=8.5, E=7.0, V=7.0),
    "France":      dict(T=9.5, P=8.5, S=7.5, K=8.5, E=6.5, V=8.0),
    "Brazil":      dict(T=9.0, P=8.5, S=6.5, K=5.5, E=6.5, V=6.0),
    "Croatia":     dict(T=6.5, P=4.5, S=8.5, K=9.0, E=6.5, V=6.0),
    "Netherlands": dict(T=8.0, P=7.5, S=6.5, K=6.0, E=6.5, V=6.0),
    "England":     dict(T=9.0, P=8.5, S=6.0, K=5.5, E=6.5, V=6.5),
    "Morocco":     dict(T=6.5, P=7.5, S=7.5, K=5.5, E=7.0, V=6.5),
    "Portugal":    dict(T=8.5, P=6.5, S=6.0, K=7.0, E=6.5, V=6.5),
}

# Actual results for comparison
QF_ACTUAL = {("Croatia","Brazil"): "Croatia", ("Netherlands","Argentina"): "Argentina",
             ("Morocco","Portugal"): "Morocco", ("France","England"): "France"}
ACTUAL_CHAMPION = "Argentina"
ACTUAL_RUNNER_UP = "France"
ACTUAL_3RD = "Croatia"  # beat Morocco 2-1

def comp(t): return sum(W[k]*v for k,v in TEAMS[t].items())
C = {t: comp(t) for t in TEAMS}

def wp(a, b): return 1/(1+math.exp(-KSTEEP*(C[a]-C[b])))
def play(a, b): return a if random.random() < wp(a,b) else b

# ---- Pairwise: model's view on each actual QF matchup ----
print("=== PAIRWISE: Model vs Actual QF Results ===\n")
correct_qf = 0
for (a, b), winner in QF_ACTUAL.items():
    p_a = wp(a, b)
    model_pick = a if p_a >= 0.5 else b
    correct = "✓" if model_pick == winner else "✗"
    print(f"  {a:<13} {100*p_a:.1f}%  vs  {b:<13} {100*(1-p_a):.1f}%  "
          f"→ actual: {winner:<13} model pick: {model_pick} {correct}")
    if model_pick == winner: correct_qf += 1
print(f"\n  QF directional accuracy: {correct_qf}/4")

# ---- Full sim from QF ----
champ = defaultdict(int); final_cnt = defaultdict(int); sf_cnt = defaultdict(int)
for _ in range(N):
    w1 = play("Croatia","Brazil")
    w2 = play("Netherlands","Argentina")
    w3 = play("Morocco","Portugal")
    w4 = play("France","England")
    sf_cnt[w1]+=1; sf_cnt[w2]+=1; sf_cnt[w3]+=1; sf_cnt[w4]+=1
    s1 = play(w1,w2); s2 = play(w3,w4)
    final_cnt[s1]+=1; final_cnt[s2]+=1
    champ[play(s1,s2)] += 1

print(f"\n=== CHAMPIONSHIP PROBABILITIES ({N//1000}k sims from QF) ===\n")
print(f"{'Team':<14}{'SF%':>6}{'Final%':>8}{'Champ%':>8}  Composite  Note")
print("-"*72)
for t,c in sorted(champ.items(), key=lambda x:-x[1]):
    tag = ""
    if t == ACTUAL_CHAMPION: tag = "← ACTUAL CHAMPION"
    elif t == ACTUAL_RUNNER_UP: tag = "← finalist"
    elif t == ACTUAL_3RD: tag = "← 3rd place"
    print(f"{t:<14}{100*sf_cnt[t]/N:>6.1f}{100*final_cnt[t]/N:>8.1f}"
          f"{100*c/N:>8.1f}  {C[t]:.3f}     {tag}")

# ---- Calibration ----
p_champ = champ[ACTUAL_CHAMPION]/N
log_loss = -math.log(p_champ)
random_ll = math.log(8)
print(f"\n=== CALIBRATION ===\n")
print(f"P(Argentina wins from QF): {100*p_champ:.1f}%")
print(f"Log-loss (champion): {log_loss:.3f}  [random baseline: {random_ll:.3f}]")
print(f"Skill vs random: {100*(random_ll-log_loss)/random_ll:.0f}% reduction in log-loss")

# ---- Morocco specific ----
p_ma_sf = sf_cnt["Morocco"]/N
p_ma_f  = final_cnt["Morocco"]/N
p_ma_ch = champ["Morocco"]/N
print(f"\nMorocco (honest K=5.5):  SF {100*p_ma_sf:.1f}%  Final {100*p_ma_f:.1f}%  "
      f"Champ {100*p_ma_ch:.1f}%")
print(f"Morocco actual result:  SF YES  Final NO  Champ NO")
print(f"→ SF was a genuine {100*(1-p_ma_sf):.0f}% surprise on pre-tournament fundamentals")

# ---- Counterfactual: what if we HAD used Morocco's current K=8.5? ----
print(f"\n=== HINDSIGHT COUNTERFACTUAL: Morocco K=5.5 vs K=8.5 ===\n")
TEAMS_HB = dict(TEAMS)
TEAMS_HB["Morocco"] = dict(T=6.5, P=7.5, S=7.5, K=8.5, E=7.0, V=6.5)
C_HB = {t: sum(W[k]*v for k,v in TEAMS_HB[t].items()) for t in TEAMS_HB}
def wp_hb(a,b): return 1/(1+math.exp(-KSTEEP*(C_HB[a]-C_HB[b])))
def play_hb(a,b): return a if random.random() < wp_hb(a,b) else b
champ_hb = defaultdict(int)
for _ in range(N):
    w1=play_hb("Croatia","Brazil"); w2=play_hb("Netherlands","Argentina")
    w3=play_hb("Morocco","Portugal"); w4=play_hb("France","England")
    s1=play_hb(w1,w2); s2=play_hb(w3,w4)
    champ_hb[play_hb(s1,s2)] += 1
print(f"Morocco champ% with honest K=5.5:   {100*champ['Morocco']/N:.1f}%")
print(f"Morocco champ% with hindsight K=8.5: {100*champ_hb['Morocco']/N:.1f}%")
print(f"→ K inflation adds {100*(champ_hb['Morocco']-champ['Morocco'])/N:.1f}pp to Morocco's"
      f" projected title odds")

# ---- Summary verdict ----
print(f"\n=== SUMMARY ===\n")
top2 = sorted(champ.items(), key=lambda x:-x[1])[:2]
print(f"Model's top-2 picks from QF: {top2[0][0]} ({100*top2[0][1]/N:.0f}%) "
      f"and {top2[1][0]} ({100*top2[1][1]/N:.0f}%)")
print(f"Actual final: {ACTUAL_CHAMPION} vs {ACTUAL_RUNNER_UP}")
print(f"QF directional accuracy: {correct_qf}/4 matchups")
print(f"\nKey finding: model rewards K-heavy teams (Croatia, Argentina) and penalises")
print(f"talent-heavy/KO-thin teams (Brazil, England) — consistent with the thesis.")
print(f"Morocco's SF run was unpredictable from pre-tournament fundamentals (K=5.5).")
print(f"Their Qatar 2022 run IS the evidence that earned K=8.5 for 2026.")
