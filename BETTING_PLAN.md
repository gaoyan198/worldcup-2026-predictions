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

| # | Bet | Stake | Status (all placed 2026-06-12) | Rationale |
|---|---|---|---|---|
| 1 | **Spain outright** | $30 | **PLACED at 4.50** (at threshold; +16% EV on blend) → pays $135 | Both model (#1, 39%) and every market (#1) agree; easy group, soft bracket side |
| 2 | **Argentina outright** | $25 | **PLACED at 6.00** (below 8.00 threshold — SGP clipped vs intl ~10.0; −9% EV on blend, +48% on pure Elo) → pays $150 | Biggest model-vs-market gap: Elo 24.7% vs PM 8.8% — a pure trust-the-model position at this price |
| 3 | **Colombia outright** | $10 | **PLACED at 35** (below 50 threshold; ~fair on pure Elo 2.9%, −EV on blend) → pays $350 | Elo-vs-market gap (2.9% vs PM 1.8%); lottery sizing |
| 4 | **Morocco outright** | $10 | **PLACED 2026-06-12 at 35** (−EV on all signals: Elo ~0%, PM 1.6%; pure lottery ticket / 2022 redux bet) → pays $350 | |
| 5 | **Norway to win in 90 min vs Ivory Coast (1X2)** | $15 | ✅ **WON** (placed 2026-06-28 @1.85; settled 2026-06-30). Returned $27.75, **profit +$12.75.** Was a thin ~58% +EV bet — favourite delivered. | LESSON: always confirm 1X2 vs to-qualify market before betting a knockout favorite |
| 6 | **Reserve — Round of 16 match bets** | **$25** | After R32 (~early July) | Recycled Norway stake ($15) back in + original $10; $12.75 Norway profit BANKED (off the table). Deploy where model beats SGP-implied with cushion |

### Group-stage outcome (as of 2026-06-28)
All four outright teams advanced; three won their groups.
- 🇦🇷 Argentina — won Group J (Messi brace vs Austria); R32 vs Cape Verde (model 95%). Best ticket.
- 🇪🇸 Spain — won Group H (recovered: 4-0 Saudi, 1-0 Uruguay); R32 vs Austria (85%).
- 🇨🇴 Colombia — WON Group K (0-0 vs Portugal); R32 vs Ghana (92%). Dream draw.
- 🇲🇦 Morocco — 2nd in Group C; R32 vs Netherlands (model 36%). ✅ UPSET — drew 1-1, won on penalties. Outright ALIVE. R16 vs Canada.
- 🇳🇴 Norway — R32 ✅ beat Ivory Coast (win-in-90 bet won). R16 vs Brazil (no further Norway bet held).

**Position: $90 staked, $10 reserve.** Updated model (100k sims): Argentina 30.7%, Spain 27.4%, France 22.2% champion (model over-concentrates; market has France 24% / Argentina 20% / Spain 11%).

**Position summary**: $75 staked, $25 reserve. Net outcomes (ignoring reserve):
Spain win **+$60** · Argentina win **+$75** · Colombia win **+$275** · Morocco win **+$275** · all bust **−$75**.
Elo model: ~67% chance Spain, Argentina or Colombia wins; Morocco path is essentially the model being wrong.

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
