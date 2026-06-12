# World Cup 2026 — $100 SGD Betting Plan (Singapore Pools)

*As of 2026-06-12 (tournament day 2). Legal note: Polymarket is banned in
Singapore (GRA, Jan 2025) — used here as a price signal only. All actual bets
via Singapore Pools.*

## Probability estimates (three sources)

| Team | Elo model (100k sims) | Polymarket ($2.1B vol) | Blend (40% Elo / 60% PM) |
|---|---|---|---|
| Spain | 38.7% | 17.0% | **25.7%** |
| Argentina | 24.7% | 8.8% | **15.1%** |
| France | 12.3% | 16.1% | 14.6% |
| England | 6.3% | 10.5% | 8.8% |
| Portugal | 3.2% | 10.9% | 7.8% |
| Brazil | 3.1% | 8.5% | 6.3% |
| Germany | 1.0% | 5.2% | 3.5% |
| Netherlands | 1.5% | 4.4% | 3.2% |
| Colombia | 2.9% | 1.8% | 2.2% |
| Norway | 0.7% | 2.5% | 1.8% |

Polymarket is near vig-free (outcomes sum ≈ 100%); bookmaker odds carry
~15–25% overround. SG Pools outrights typically price *worse* than
international books — hence the thresholds below.

## Minimum SG Pools decimal odds to bet (break-even = 1/blend prob)

| Team | Fair odds | Bet only if SGP ≥ | Expected SGP range |
|---|---|---|---|
| Spain | 3.9 | **4.50** | 4.5–5.5 |
| Argentina | 6.6 | **8.00** | 9–11 |
| France | 6.8 | **8.00** | 5.5–6.5 ❌ likely no value |
| England | 11.4 | **13.0** | 7.5–9 ❌ likely no value |
| Colombia | 45 | **50** | 40–60 |

(Threshold = fair odds × ~1.15 cushion for model error.)

## The plan: $100 SGD

| # | Bet | Stake | Condition | Rationale |
|---|---|---|---|---|
| 1 | **Spain outright** | $30 | SGP odds ≥ 4.50 | Both model (#1, 39%) and every market (#1) agree; easy group, soft bracket side |
| 2 | **Argentina outright** | $25 | SGP odds ≥ 8.00 | Biggest model-vs-market gap: Elo 24.7% vs PM 8.8% — market over-discounts the aging core, Elo says results don't show decline |
| 3 | **Colombia outright** | $10 | **PLACED 2026-06-12 at 35** (below the 50 threshold — fair on pure Elo at 2.9%, −EV on the blend; placed anyway, let it ride, pays $350) | Elo-vs-market gap (2.9% vs PM 1.8%); lottery sizing |
| 4 | **Reserve — knockout match bets** | **$35** | After group stage (~June 28) | Re-run `predict.py` with updated Elo; bet individual R32/R16 matches where model prob beats SGP implied by >8 pts. Match markets have lower margin than outrights and the model is sharpest head-to-head |

**Skip**: France, England, Portugal, Brazil outrights — Polymarket already prices
them at or above our blend; SG Pools' margin makes them −EV.

**Hedge option**: if Spain and Argentina both reach the final (model says 24%
chance of that final), bets 1+2 guarantee a profit — do nothing. If Spain
reaches the final vs anyone else, consider cashing emotion-free: $30 at 5.0 =
$150 returned only on a win; a live hedge on the opponent can lock ~$40–60.

## Rules

- Total exposure capped at $100; no chasing, no top-ups.
- These are quarter-Kelly-ish sizes on the blend probabilities for a $100
  bankroll treated as 100% entertainment budget.
- Re-check Polymarket before betting — prices move fast in-tournament:
  `curl -s "https://gamma-api.polymarket.com/events?slug=world-cup-winner"`.
