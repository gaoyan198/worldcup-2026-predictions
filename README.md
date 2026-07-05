# World Cup 2026 Predictions

Two prediction models for the 2026 FIFA World Cup (USA/Canada/Mexico, June 11 – July 19, 2026), plus a live betting log ([BETTING_PLAN.md](BETTING_PLAN.md), $100 SGD via Singapore Pools).

**Status (2026-07-05, R16 in progress):** all four outright tickets (Spain, Argentina, Colombia, Morocco) survived to the R16; Morocco has since beaten Canada and meets France in the quarter-final on July 9. Book: $85 staked, $15 reserved for a Spain-final hedge.

## The two models

| | `predict.py` (Elo Monte Carlo) | `fundamentals_model.py` ("Six Forces") |
|---|---|---|
| Inputs | eloratings.net ratings | Hand-scored judgment, no Elo / odds / rankings |
| Role | **Sanity anchor only** — Elo is public, so it's already in every market price; it carries no edge | **Primary lens** — the edge, if any, lives in what it weights and markets don't |
| Thesis | Results-based strength + Poisson goals | Knockout DNA + environment (NA summer heat, altitude) together outweigh raw talent |
| Track record so far | Over-concentrates on top seeds (had Spain 38.7% on day 2); a 90'-win bet it liked would have died in ET (Argentina–Cape Verde) | Called the Morocco profile: eliminated Netherlands and Canada (two shootout wins); flagged England laboring and heat-soft European sides |

## Usage

```bash
python3 predict.py            # 50,000 sims, full 48-team tournament
python3 predict.py 100000     # custom count
python3 fundamentals_model.py # Six Forces, 200k knockout-gauntlet sims
```

Stdlib only. Refresh Elo before an Elo run:

```bash
curl -s https://www.eloratings.net/World.tsv -o data/world_elo.tsv
```

## Methodology

**Elo Monte Carlo** — Poisson goals `λ = 1.35 × 10^(±Δelo/850)`; hosts +100 Elo in groups, +50 in knockouts; exact 2026 format (12 groups, top 2 + 8 best thirds → R32, official bracket, third-place eligibility via randomized backtracking); ET/pens winner drawn from Elo win expectancy damped ×0.7.

**Six Forces** — each contender scored 0–10 on Talent stock, Peak timing, System/manager, Knockout DNA, Environmental fit, Variance; weights sum to 1.0 with K+E (0.33) deliberately outweighing raw talent (0.26); composite → logistic win probability (steepness 0.62) → Monte Carlo over the knockout gauntlet. Known limitation: the logistic compresses extreme mismatches, so its tail numbers (e.g. Egypt) are less trustworthy than mid-range matchups.

## Current picture (post-R32, bracket-conditional, 500k sims)

Quarter-final bracket: **France–Morocco** (set) · Portugal/Spain–USA/Belgium · Brazil/Norway–Mexico/England · Argentina/Egypt–Switzerland/Colombia.

| | Six Forces | Polymarket (Jul 5) |
|---|---|---|
| France champion | 23.9% | **36.0%** ← model says overpriced |
| Spain champion | 17.9% | 12.7% |
| Argentina champion | 16.3% | 16.8% |
| **Morocco beats France (QF)** | **39.2%** | ~21% ← biggest gap on the board |
| Morocco champion | 10.9% | 2.5% |

The Morocco–France gap is the tournament's one live disagreement worth money: bet #7, $10 on France-eliminated-in-QF @ 4.20, placed 2026-07-05 (first line all tournament to clear the plan's strict 1.15× value threshold). Full bet log, thresholds, and hedge rules: [BETTING_PLAN.md](BETTING_PLAN.md).

## Historical snapshot — day-2 predictions (2026-06-12, 100k Elo sims)

| Team | Champion % | How it aged |
|---|---|---|
| 🇪🇸 Spain | 38.7 | Alive; model concentration overcooked it (market never went above ~17%) |
| 🇦🇷 Argentina | 24.7 | Alive; model's best call vs market's 8.8% |
| 🇫🇷 France | 12.3 | Underrated — now the market favorite at 36% |
| 🏴 England | 6.3 | Alive, laboring (2-1 vs DR Congo in R32) |
| 🇧🇷 Brazil | 3.1 | Alive |
| 🇨🇴 Colombia | 2.9 | Alive — won its group over Portugal |
| 🇳🇱 Netherlands | 1.5 | Out — Morocco, R32, on penalties |

Full day-2 table: `results_100k.txt`. Lesson encoded in both the plan and the model choice above: pure-Elo models over-concentrate (small rating edges compound over 7 rounds) and miss what actually decides July knockouts in North America — heat, altitude, penalties, and squads built to win ugly.
