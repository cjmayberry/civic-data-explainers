# Nightly State + Capital Automation — Plan (2026-08-11)

Goal: every night **10:00p–12:00a CDT (03:00–05:00 UTC)** the platform adds
**one new state section + its capital city section**, fully built and
deployed, with a report that feeds the morning/daily debrief. Compounding
toward the vision: every country, state, city, and public/civic data source
we can connect to.

## Architecture (reuses the existing adaptive pipeline)

| Piece | File | Role |
|---|---|---|
| Source registry | `data/jurisdictions.json` | Ordered queue: `{id, level, name, portal_url, platform, country}`. Nightly job pops next state + its capital. |
| Nightly orchestrator | `pipeline/nightly_add.py` | Runs the whole add headless for {state, capital}. |
| Nightly cron | `0 3 * * *` (10p CDT) | Fires the orchestrator; bounded to the 2h window. |
| Build report | `Ocean/outputs/reports/civic-nightly-build-latest.md` + `civic-nightly-ledger.md` | What was added / failed / next. Read by the debrief. |

For each of {state, capital}, the orchestrator runs the existing stages
in the load-bearing order: **extract** (auto-detect platform: ArcGIS Hub
RSS/DCAT, Socrata discovery, CKAN, OpenDataSoft) → **scaffold** →
**build_manifest** → **introspect** (live schema) → **redraft** (LLM,
deepseek) → **placeholder covers** → wire `cities.json` + layouts →
**hugo build** → **git commit + push** (Pages auto-deploys).

## Bounding (keeps it inside 2h, honest curation)
- **Cap per section:** ~120 datasets (state) / ~60 (capital). Collapse
  year-series, drop test/feed/internal junk, cap by `min_score`.
- **LLM drafting** of ~180 pages/night is cheap on deepseek promo but real;
  the cap is load-bearing. Web rate limits handled with retry/backoff.
- **Curation honesty:** a brand-new unfamiliar state may not get a perfect
  12-category map on night one. Add a generic **title-keyword→category
  fallback** to minimize Default/Other, and flag leftovers `needs_review`
  rather than force-fitting. Zero-Default/Other is a *review* outcome, not
  an auto-guarantee for freshly added states.

## Permissions (limited, exactly what's needed)
- Local filesystem write (repo + Ocean report paths)
- Git commit + push to `cjmayberry/civic-data-explainers` (SSH, already configured)
- Network: data portals + LLM API (keys in `.env`)
- **No admin, no other accounts, no approval gate** — the cron runs in a
  fresh headless session using the plain-python path (proven to run the
  build/commit/push without the interactive terminal approval prompt).
  No curl to arbitrary hosts that trips the gate; use requests/web_extract.

## Failure handling (never leave the repo broken)
- Non-fatal per city: if the capital fails, the state still ships; the
  error goes in the report.
- Commit/push **only after a successful build**; on failure `git revert`
  the partial work and log it for the next night.
- Hard 2h timeout: ship what's clean, defer the rest.
- Source unavailable / no portal: mark `unavailable` in the registry and
  **skip to the next candidate** rather than stalling the nightly.

## Debrief integration
- The nightly add (03:00–05:00 UTC) completes **after** the `daily-debrief`
  (02:40 UTC). Design: the orchestrator writes the build report; the
  debrief reads `civic-nightly-build-latest.md` on its next run and
  summarizes: state + capital added, dataset counts, platform, deploy URL,
  failures, next-up. One-day lag by design (the 10p add is reviewed in the
  next day's review). If the user wants a same-morning readout, add a
  dedicated **morning brief** cron (~07:30 CDT) that delivers the overnight
  build summary — decided on preference.

## Phased rollout
- **Phase 1 — validate headless (this week):** seed registry; build
  `nightly_add.py`; run ONE unattended test on a live pair (e.g. Kansas +
  Topeka, or New Mexico + Santa Fe) to prove the full chain builds, commits,
  pushes, and writes the report without a user in the loop.
- **Phase 2 — steady state:** cron `0 3 * * *` active; nightly adds; debrief
  summaries; failures auto-notified in the report.
- **Phase 3 — widen:** countries + more platform families (OpenDataSoft, EU
  portals); a freshness agent reading `monitoring.json` (from the v4 spec).

## Open decisions for the user
1. First test pair (Kansas/Topeka vs New Mexico/Santa Fe vs other)?
2. Same-morning brief (07:30 CDT) or is the next-evening debrief enough?
3. Confirmed the nightly LLM-draft token cost is acceptable (cheap, but
   nonzero and recurring every night)?
