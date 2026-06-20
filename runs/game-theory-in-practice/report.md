# Run Report — Game Theory in Practice

**Slug:** game-theory-in-practice
**Completed:** 2026-06-13T10:28:00Z
**Live URL:** https://newizz.github.io/agent-newsroom/published/game-theory-in-practice/

---

## What you asked for

A practical, example-driven survey of how game theory is applied across real-world domains — economics, business strategy, geopolitics, biology, and technology platforms — covering both its genuine successes and where its predictions break down when human behavior diverges from rational-actor assumptions.

## What we built

The dashboard uses a data-story template with five domain sections (Mechanism Design, Geopolitics, Business/Oligopoly, Behavioral Failures, and Algorithmic/AI), each anchored by a concrete named case study with measurable outcomes. It includes an interactive payoff matrix simulator where readers can toggle between the Prisoner's Dilemma, Chicken/Hawk-Dove, Stag Hunt, and Ultimatum Game scenarios and see Nash equilibria highlighted, plus a sortable data table of key metrics (FCC auction revenues, kidney exchange counts, ultimatum game rejection rates). The core takeaway the dashboard drives home: game theory's most reliable results come from mechanism design — engineering the rules of a game — not from predicting how people will play a game someone else designed.

## Headline findings

1. **Mechanism design beats prediction every time** — The FCC spectrum auctions (1994–present), designed by Milgrom, Wilson, and McAfee, raised $23 billion in their first four years and over $100 billion by 2020; Alvin Roth's kidney-exchange algorithm enabled 1,744 paired-donation transplants in 2024 alone. These are engineered equilibria with receipts — not forecasts.

2. **MAD is a Nash equilibrium, but causation is unverifiable** — Mutual Assured Destruction maps cleanly onto a two-player game where first-strike produces a worse outcome than the status quo. The U.S.–Soviet nuclear freeze held for ~45 years. Historians remain divided on whether game-theoretic logic caused that restraint or whether luck, ideology, and bureaucratic caution deserve equal or greater credit — the counterfactual cannot be run.

3. **Humans reliably reject unfair outcomes even at personal cost** — In Werner Güth's 1982 ultimatum game — replicated hundreds of times across 15 cultures — proposers typically offer 30–50% of a stake and responders reject offers below 20–25%, accepting a zero payoff to punish unfairness. The subgame-perfect Nash prediction (offer $0.01, accept) is almost never observed. The deviation is not noise; it is systematic and large.

4. **AI pricing algorithms rediscover grim-trigger collusion without being taught to** — Calvano et al. (2020, *American Economic Review*) showed Q-learning algorithms independently sustain prices 10–20% above competitive levels in simulated oligopolies using punishment phases, without communicating and without violating antitrust law. Current competition law requires proof of intent or communication — a legal gap every major antitrust authority has flagged but none has resolved.

5. **The winner's curse traps even sophisticated bidders in common-value auctions** — Identified in 1971 U.S. offshore oil-lease auctions by Capen, Clapp, and Campbell: the highest bidder systematically wins because their private estimate of a field's value is the most optimistic, not the most accurate. The same pattern appears in corporate takeover markets, publishing advance-rights deals, and professional sports free agency — and Robert Wilson's theoretical explanation of it was part of his 2020 Nobel citation.

## How to use the dashboard

Start with the **Payoff Matrix Simulator** in the top section: select a game type from the dropdown (Prisoner's Dilemma, Chicken, Stag Hunt, Ultimatum Game) to see the payoff matrix rendered with Nash equilibria highlighted and a plain-language explanation of what it predicts versus what actually happens in experiments. Then scroll through the **five domain panels** in order — each one leads with a named case study and a concrete number (auction revenue, transplant count, price premium, rejection rate). The **data table** at the bottom lets you sort all key metrics side by side. Pay particular attention to the "Game Theory Works / Doesn't Work" split column in each domain panel — it tracks the distinction between mechanism design cases (high confidence) and predictive-interpretation cases (hedged).

## Sources (19 consulted; top 8 listed)

- **The FCC Spectrum Auctions: An Early Assessment** — Peter Cramton, *Journal of Economics & Management Strategy* (1997) — https://cramton.umd.edu/papers1995-1999/97jems-fcc-spectrum-auctions.pdf
- **Nobel Prize 2020 Press Release (Milgrom & Wilson)** — Royal Swedish Academy of Sciences — https://www.nobelprize.org/prizes/economic-sciences/2020/press-release/
- **National Kidney Registry Facilitates 10,000th Transplant** — National Kidney Registry (2024) — https://www.kidneyregistry.com/news/national-kidney-registry-facilitates-10000th-living-donor-kidney-transplant/
- **Artificial Intelligence, Algorithmic Pricing, and Collusion** — Calvano, Calzolari, Denicolò, Pastorello, *American Economic Review* 110(10), 2020 — https://www.aeaweb.org/articles?id=10.1257/aer.20190623
- **Game theory and the Cuban missile crisis** — Steven Brams (referenced), Plus Magazine / University of Cambridge — https://plus.maths.org/content/game-theory-and-cuban-missile-crisis
- **Thomas Schelling: the legacy of a master strategist** — *The Conversation* (2016) — https://theconversation.com/thomas-schelling-the-legacy-of-a-master-strategist-70394
- **Mechanism Design for Large Language Models** — Paul Duetting et al., ACM Web Conference 2024 Best Paper — https://research.google/blog/mechanism-design-for-large-language-models/
- **Organ transplants exceeded 48,000 in 2024** — HRSA / OPTN (2025) — https://www.hrsa.gov/optn/news-events/news/organ-transplants-exceeded-48000-2024-33-percent-increase-transplants-performed-2023

## Limitations & caveats

- **Cold War deterrence causation is unfalsifiable.** Game theory provides a compelling after-the-fact narrative for why the U.S. and USSR avoided nuclear war, but it cannot be verified against a counterfactual. Historians actively debate whether MAD logic, luck (1962, 1983 close calls), or non-game-theoretic factors (ideology, domestic politics) deserve primary credit.
- **Google ad revenue figure is from a single secondary source** (a Cornell course blog). The $19 billion Q2 2016 figure is directionally correct but should not be cited as authoritative.
- **OPEC quota compliance data is inherently soft.** Member nations self-report production; independent verification is incomplete. Iraq's and Kazakhstan's quota violations are well-documented in policy sources but exact overproduction figures vary by analyst.
- **Calvano et al. is a simulation, not a field study.** The Q-learning collusion finding used a stylized two-firm Bertrand model. Whether real-world pricing algorithms in messier markets converge on the same behavior at the same magnitudes is an open empirical question.
- **Evolutionary game theory applications to human social norms** (fairness norms, cooperation) are supported by correlational evidence (cross-cultural ultimatum game data), not controlled experiments — alternative explanations (cultural transmission, religion, law) are not ruled out.
- **Climate game theory section reflects 2026 state of play.** The Paris Agreement's unconditional NDC structure continues to exhibit the free-rider dynamics game theory predicts; conditional reciprocal commitment proposals remain politically untested at scale.
- **The 2020 Nobel Prize citation for Milgrom and Wilson** could not be fetched directly (403 Forbidden); figures were cross-checked via CNN and CNBC coverage. The $100 billion cumulative auction revenue figure is widely cited but aggregates across different auction formats and years.

## Next steps

- 👀 **View it:** https://newizz.github.io/agent-newsroom/published/game-theory-in-practice/
- 🔁 **Rerun deeper:** tell the orchestrator "rerun game-theory-in-practice with deeper research"
- ✏️ **Edit:** open `published/game-theory-in-practice/index.html` and edit directly

---

_Generated by agent-newsroom_
