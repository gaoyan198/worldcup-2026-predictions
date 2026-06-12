# World Cup 2026 Predictions

Monte Carlo simulator for the 2026 FIFA World Cup (USA/Canada/Mexico, June 11 – July 19, 2026).

## Usage

```bash
python3 predict.py            # 50,000 simulations
python3 predict.py 100000     # custom count
```

No dependencies beyond the Python 3 stdlib. Refresh ratings before a run:

```bash
curl -s https://www.eloratings.net/World.tsv -o data/world_elo.tsv
```

## Methodology

- **Strength**: World Football Elo Ratings ([eloratings.net](https://www.eloratings.net)).
- **Goals**: Poisson, `λ = 1.35 × 10^(±Δelo/850)` — gives realistic W/D/L splits and goal differences for group tiebreaks.
- **Home advantage**: hosts (US/MX/CA) +100 Elo in group stage, +50 in knockouts.
- **Format**: exact 2026 format — 12 groups of 4, top 2 + 8 best thirds → round of 32, official FIFA bracket (matches 73–104), third-place slot eligibility solved by randomized backtracking.
- **Knockout draws**: extra-time/shootout winner drawn from Elo win expectancy with margin damped ×0.7.

Approximation: when a qualified-thirds combination isn't exactly coverable by the eligibility sets, assignment is relaxed greedily (rare). FIFA's exact 495-combination allocation table is not reproduced.

## Results — 100,000 sims (Elo as of 2026-06-12, tournament day 2)

| Team | Champion % | Final % | SF % |
|---|---|---|---|
| 🇪🇸 Spain | **38.7** | 54.9 | 69.2 |
| 🇦🇷 Argentina | 24.7 | 44.1 | 59.3 |
| 🇫🇷 France | 12.3 | 23.3 | 49.6 |
| 🏴 England | 6.3 | 15.7 | 33.3 |
| 🇵🇹 Portugal | 3.2 | 9.2 | 17.6 |
| 🇧🇷 Brazil | 3.1 | 8.7 | 22.3 |
| 🇨🇴 Colombia | 2.9 | 8.3 | 16.4 |
| 🇳🇱 Netherlands | 1.5 | 4.8 | 16.5 |

Full table: `results_100k.txt`.

## Cross-check vs betting market (BetMGM, June 11, 2026, de-vigged ~1.21 overround)

| Team | Elo model | Market | 50/50 blend |
|---|---|---|---|
| Spain | 38.7% | ~15.0% | **~27%** |
| Argentina | 24.7% | ~8.3% | ~16% |
| France | 12.3% | ~13.8% | ~13% |
| England | 6.3% | ~10.3% | ~8% |
| Brazil | 3.1% | ~9.2% | ~6% |
| Portugal | 3.2% | ~8.3% | ~6% |
| Germany | 1.0% | ~5.5% | ~3% |

Pure-Elo models concentrate probability on the top-rated team (small rating edges compound over 7 rounds); markets price in squad depth, injuries and variance. Both agree on the headline: **Spain is the most likely champion**, with Argentina/France next. The model is notably higher than the market on Argentina (Elo #2 on results; market discounts an aging core) and lower on Brazil/Portugal.
