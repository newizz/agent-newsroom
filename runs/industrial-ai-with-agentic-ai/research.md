# Research: Industrial AI with Agentic AI

**Slug:** industrial-ai-with-agentic-ai
**Brief:** runs/industrial-ai-with-agentic-ai/brief.md
**Research date:** 2026-06-11
**Confidence:** medium

> Note: Market-size figures vary widely across research firms; ranges and sources are cited explicitly throughout. Use-case status (pilot vs. production) is tagged where verifiable. Vendor-sourced claims are marked accordingly.

---

## TL;DR

Agentic AI — systems that set their own sub-goals, use tools, and loop on feedback without constant human prompting — marks a qualitative shift from the predictive and prescriptive Industrial AI tools that have dominated since the 2010s. As of mid-2026, the most mature industrial deployments are in supply chain orchestration (General Mills, Walmart), oil-and-gas operational safety (Aker BP via ABB/Cognite), and pharma quality management (AstraZeneca), while autonomous process control of physical equipment remains largely at pilot or pre-production stage. Gartner (April 2026) forecasts supply chain management software with agentic AI growing from under $2 billion in 2025 to $53 billion by 2030; Mordor Intelligence pegs the energy-and-utilities agentic AI segment alone at $0.87 billion in 2026, expanding at a 36% CAGR. The dominant barrier to production rollout is not model capability but the absence of industrial-grade verification and validation frameworks for non-deterministic agents operating near physical assets — a gap that ISO/IEC TS 22440 is beginning to address but that will take several years to close at scale.

---

## Key findings

1. **Agentic AI clears the "multi-step autonomy" bar that traditional Industrial AI cannot** — Traditional predictive maintenance or quality-inspection AI issues a recommendation and waits; an agentic system receives the same sensor signal, cross-checks maintenance history, locates the nearest certified technician, drafts a work order, checks for spare-part availability, and schedules the shutdown window — all without human intervention. Siemens (Automate 2025) describes this as a shift from AI that "responds to queries" to AI that "independently executes complete industrial workflows." [^1][^2]

2. **Supply chain is the furthest-along vertical in production-grade agentic deployments** — General Mills confirmed its supply chain optimization agent assesses 5,000+ daily shipments autonomously and has delivered $20M+ in savings since FY2024. [^3] Walmart deployed an agentic end-to-end supply chain workflow that anticipates demand and moves orders before shifts begin. [^4] Gartner (April 2026) projects 60% of SCM software users will have adopted agentic AI features by 2030, up from 5% in 2025. [^5]

3. **Oil-and-gas and energy are accelerating — from Aker BP to grid self-healing** — Cognite and ABB (May 2026) signed Aker BP as first customer for agent-to-agent orchestration between ABB Ability SafetyInsight and Cognite Data Fusion, targeting 525,000 boe/day production efficiency. [^6][^37] Mordor Intelligence values the agentic AI in energy-and-utilities market at $0.87 billion in 2026, growing to $4.11 billion by 2031 (36.35% CAGR). [^7] The grid-operations-and-self-healing segment held the largest use-case share (24.6%) in 2025. [^7]

4. **Pharma quality management is moving from pilot to validated production via "draft-and-review" mode** — 67% of life sciences firms ran agentic AI pilots as of Q1 2026. [^8] Early adopters report 40–50% reductions in deviation investigation cycle times and 60–75% compression in batch record review. [^8] AstraZeneca's AIDA framework (presented at ARC Forum, February 2026) orchestrates flows from API to coated tablet while keeping humans in the loop for strategic reviews. [^9] All production deployments in validated pharma environments operate in "draft-and-review" mode, not fully autonomous execution. [^8]

5. **The dominant technology stack combines LLM-based agents, domain-specific data fabrics, digital twins, and OT-native protocols** — Orchestration layers consume OPC UA and MQTT streams from the edge, feed semantic data fabrics (Cognite Data Fusion, Palantir Foundry Ontology), and route tasks to specialized agents backed by LLMs. NVIDIA Omniverse provides the physically-accurate digital twin layer for pre-deployment simulation; the Siemens-NVIDIA partnership (announced 2025, first live instance at Erlangen 2026) aims to be the reference architecture for AI-driven adaptive manufacturing. [^10][^11]

6. **Gartner identifies a sobering counter-signal: >40% of agentic AI projects will be cancelled by end of 2027** — Primary causes are escalating costs, unclear business value, and inadequate risk controls. [^12] An independent academic study of 12 industrial companies (arXiv, May 2026) found only one operating at multi-agent orchestration level; four others had experimental capability but could not deploy it due to missing output-verification mechanisms — labeled "the capability-deployment verification gap." [^13]

7. **Safety standards are catching up but remain 1–2 years behind deployment pace** — IEC 61508:2025 updated to explicitly address AI scope and human factors. [^14] ISO/IEC TS 22440 (Parts 1–3, currently in CD stage) is the first standard specifically designed to qualify AI functional safety requirements, covering reliability, explainability, and V&V lifecycle integration. [^15] Until TS 22440 is ratified and adopted, human-in-the-loop review remains the only trusted verification mechanism that satisfies safety regulators. [^13]

---

## Background / context

Traditional Industrial AI — predictive maintenance models, visual quality inspection, process optimization algorithms — emerged commercially in the 2010s and reached broad deployment through platforms like GE Predix, Siemens MindSphere, and Honeywell Forge. These systems share a common structure: ingest sensor data, run a model, output a recommendation or alert. A human (or a hard-coded rule) converts that output into action. The AI is, in the terminology of ISO 22440, "advisory" rather than "executive."

Agentic AI breaks this architecture. An agent holds a goal, plans a sequence of steps to achieve it, executes those steps using tools (APIs, databases, actuators), observes results, and loops until the goal is achieved or it escalates. This loop can run in milliseconds across dozens of systems simultaneously. The distinction matters because industrial operations generate continuous streams of exceptions — equipment deviations, supply disruptions, quality escapes — that today consume most of the cognitive bandwidth of skilled engineers. Agentic systems are designed to resolve the routine exceptions autonomously, escalating only the genuinely novel.

The preconditions for industrial agentic AI — large language models capable of multi-step reasoning, mature API ecosystems around OT platforms, and affordable GPU inference at the edge — converged around 2024. The market response has been rapid: Gartner named agentic AI its top strategic technology trend for 2025; Siemens unveiled its AI-agent architecture at Automate 2025; and by early 2026 every major automation incumbent had announced or partnered on an agentic offering.

However, industrial AI deployments face constraints that consumer or enterprise SaaS deployments do not: physical safety consequences, regulatory qualification requirements (21 CFR Part 11, IEC 61508, EU AI Act), decades of proprietary protocols (Modbus, PROFINET, OPC UA), and cultural norms built around human accountability for process outcomes. These constraints mean that the hype cycle for industrial agentic AI is running about 18–24 months behind the enterprise IT hype cycle — and the distance between "demonstrated in a booth" and "running unsupervised on a live process line" remains considerable.

---

## Deep dive

### Agentic AI vs. Traditional Industrial AI

The functional distinction between conventional Industrial AI/ML and agentic AI rests on four properties:

| Property | Traditional Industrial AI | Agentic AI |
|---|---|---|
| Trigger | Event-driven (sensor threshold, scheduled batch) | Goal-driven (pursue objective until achieved) |
| Action | Single-output recommendation or alert | Multi-step tool-calling sequence |
| Memory | Stateless or short-window inference | Persistent working memory across sessions |
| Feedback | Human validates output, decides action | System observes action result and adapts |

A predictive maintenance model on a rotating asset is traditional Industrial AI: it outputs "bearing likely to fail in 14 days." An agentic maintenance system responds to the same signal by interrogating the CMMS for maintenance history, checking the MRO stock database for bearing availability, searching technician schedules for qualified personnel, drafting and submitting a work order, and confirming the scheduled shutdown — all in one autonomous loop. [^1][^16]

The word "agentic" itself remains loosely defined in vendor literature. A practical working definition for industrial operators: an agentic system must demonstrate (a) goal-directed planning over at least three sequential steps, (b) tool use against external systems, (c) feedback integration — adjusting behavior based on observed outcomes, and (d) exception escalation — surfacing unresolvable situations to humans rather than failing silently. Systems meeting only (a) and (b) are better characterized as "workflow automation" than true agentic AI.

### Industrial Verticals and Use Cases

**Manufacturing** is the broadest vertical and the most heterogeneous in deployment maturity:

- *Quality control automation*: Vision AI agents continuously inspect production lines and, in agentic implementations, autonomously flag, quarantine, and root-cause defective batches — triggering process parameter adjustments without human intervention. Husqvarna deploys AI vision companions for chainsaw production quality inspection. [^16]
- *Agentic maintenance orchestration*: Siemens' Senseye predictive maintenance agent (generally available) has delivered 25% average reduction in reactive maintenance time for early customers (vendor claim). [^1]
- *Production planning*: Danfoss automated 80% of order-processing decisions through agentic AI; Suzano reported 95% reduction in SAP query time via natural language agents. [^17]
- *Shop-floor operations*: Rockwell Automation's FactoryTalk Plex introduced six initial AI agents in 2025 for automated quality checks and analytics recommendations, with a roadmap for user-defined goal-driven agents. [^18] The Elastic MES platform processes over 11 billion daily transactions. [^18]

**Energy and Utilities** shows the clearest progression toward autonomous grid operations:

- Self-healing grid agents continuously detect faults, isolate affected segments, reroute power flows, and dispatch inspection drones to GPS coordinates — reducing outage durations by up to 80% in documented utility pilots (as of 2025). [^19]
- Demand-response AI agents (fastest-growing segment at 40.73% CAGR per Mordor, 2026–2031) dynamically balance load across distributed assets, coordinating millions of IoT endpoints in real time. [^7]
- Agentic AI in energy-and-utilities market was $0.87 billion in 2026 (Mordor Intelligence estimate). [^7]
- In March 2026, Tata Power announced a strategic partnership with Salesforce to deploy Agentforce AI for renewable energy operations. [^20]

**Oil and Gas** is experiencing an inflection from AI-assisted to AI-orchestrated operations:

- BCG (2025) estimated that firms fully integrating AI agents into O&G operations can generate 30–70% incremental EBIT-equivalent improvements over five years, compressing processes from months to weeks (vendor/consultant claim; no independent verification found). [^21]
- XMPro reports seismic analysis processing times reduced from 6–12 months to 8–12 weeks via agentic AI; drilling efficiency improvements of 25–35%. [^16]
- Aker BP/ABB/Cognite (May 2026): first production-grade agent-to-agent orchestration deployment in an O&G context, integrating ABB Ability SafetyInsight and AlarmInsight with Cognite's data platform for autonomous risk assessment and alarm rationalization. [^6]

**Logistics and Supply Chain** is the most advanced vertical by volume of production deployments:

- General Mills: 5,000+ daily shipment assessments, $20M+ savings since FY2024. [^3]
- Walmart: Agentic end-to-end supply chain workflow confirmed in production. [^4]
- Palantir-NVIDIA partnership: Lowe's deployed a digital twin of its global logistics network, with agents continuously optimizing routes, adjusting inventory, and balancing supplier performance in real time (announced October 2025). [^22]
- The agentic logistics/supply-chain segment was estimated at $8.67 billion in 2025, projected to $16.84 billion by 2030. [^23]

**Pharmaceuticals** represents the clearest case where regulatory environment is simultaneously accelerating (by creating clear compliance incentives) and constraining (by demanding validated, auditable autonomy) deployment:

- AstraZeneca's AIDA framework (ARC Forum, February 2026): AI agents orchestrate development flows from API to coated tablet; 26 global manufacturing sites; edge computing reduces latency for real-time production decisions. [^9]
- Deviation investigations: 40–50% cycle time reduction; batch record review: 60–75% compression; change control assessments: 3–5 days to 4–8 hours — from early industry deployments as of Q1 2026. [^8]
- All production deployments operate in "draft-and-review" mode. No fully autonomous execution in GMP-regulated environments confirmed as of mid-2026. [^8]

### Technology Stack

A typical industrial agentic AI architecture comprises four layers:

**Edge and OT Layer:** Real-time sensor data and control signals travel over OPC UA (for machine-level interoperability), MQTT (for lightweight pub/sub messaging), and DDS (for latency-critical applications). Edge compute (NVIDIA Jetson, Intel OpenVINO hardware) handles local inference for sub-100ms response requirements. ISA-95 and ISA-99/IEC 62443 govern security architecture at this layer.

**Data Fabric / Industrial Knowledge Layer:** Platforms like Cognite Data Fusion, Palantir Foundry Ontology, and OSIsoft PI (AVEVA) aggregate and semantically model OT+IT+engineering data. This layer is the primary bottleneck for agentic readiness — agents require event-driven data streams and machine-interpretable semantic models, not just flat APIs. Eight in ten companies cite data limitations as a roadblock to scaling agentic AI (McKinsey, 2025). [^24]

**Orchestration and Agent Layer:** Large language models (most commonly frontier models via private deployment or secure APIs) serve as orchestrators and as the reasoning engine within specialized task agents. Multi-agent frameworks coordinate domain agents (process optimization, maintenance scheduling, quality management) and task agents (data retrieval, anomaly detection, work-order creation). Key emerging standards: Google's Agent2Agent (A2A) Protocol for cross-vendor agent communication; Anthropic's Model Context Protocol (MCP) for connecting agents to real-time data sources. Platforms: Siemens Xcelerator AI agent marketplace (announced), Cognite Atlas AI (no-code industrial agent workbench), XMPro MAGS (Type 4–5 multi-agent generative systems), Microsoft Copilot Studio (Type 1–2, broader enterprise).

**Simulation and Digital Twin Layer:** NVIDIA Omniverse (with OpenUSD and PhysicsNeMo) provides physically-accurate facility digital twins for pre-deployment simulation. The Siemens-NVIDIA Industrial AI Operating System partnership (Erlangen factory live 2026) is the most ambitious production reference architecture. Samsung's strategy to transition global manufacturing into AI-driven factories by 2030 relies on digital twin-based simulations and specialized AI agents for quality control, production, and logistics. [^25]

### Vendor Landscape

**Established automation incumbents** are broadly categorized by their approach:

- **Siemens**: Most complete announced agentic portfolio. Industrial Copilot ecosystem (Design, Engineering, Planning, Operations, Maintenance copilots) extended to full AI agents at Automate 2025; partnership with NVIDIA to build the "Industrial AI Operating System"; Erlangen factory the first production blueprint. [^1][^10] Productivity target: up to 50% for industrial customers (vendor claim). [^1]
- **Rockwell Automation**: FactoryTalk Plex agents (6 initial agents, quality and analytics); Elastic MES; roadmap includes user-defined goal-driven agents and Plex Agent Composer for IT/OT environments. Customers include Texas Instruments (energy reduction) and GE (OTTO robots). [^18]
- **ABB**: Strategic partnership with Cognite (May 2026) for agent-to-agent industrial orchestration, initially in energy applications. Broader ABB Ability™ platform integrating agentic layer. [^6]
- **Honeywell**: Partnership with Google Cloud (announced October 2024, solutions available 2025) to deploy Gemini-backed AI agents on Honeywell Forge IoT platform across industrial sectors. [^26]
- **GE Vernova**: CSense platform moving toward autonomous operations; partnership with ANYbotics for AI-powered legged robotics inspection (2025). [^27]
- **Schneider Electric**: Cited in energy-and-utilities market analyses as a major platform provider; specific agentic product releases not independently verified in this research.

**Data and AI platform providers** that supply the orchestration layer:

- **Cognite**: Atlas AI workbench for industrial agents; Cognite Data Fusion as the semantic data layer; industry presence at major energy and process operators (ExxonMobil, Aker BP, Koch, Idemitsu among Impact 2025 speakers). [^28]
- **Palantir**: AIP platform with industrial ontology; MES-connected agents that reduce operator cognitive load; demonstrated supply chain digital twin with NVIDIA. [^22]
- **C3.ai**: C3 Agentic AI Platform (GA April 2026) including C3 Code for autonomous engineering; industry-specific SaaS applications. [^29]
- **XMPro**: Purpose-built multi-agent generative systems (MAGS) for mining, oil-and-gas, utilities; processes up to 50 million monitoring events daily (vendor claim). [^16]

**Hyperscalers** increasingly serve as orchestration infrastructure:

- **NVIDIA**: Omniverse simulation platform; CUDA-X AI libraries; partnerships with Siemens, Palantir, and virtually every major industrial vendor; showcased AI manufacturing at Hannover Messe April 2026. [^11]
- **Microsoft**: Azure OpenAI integration; Copilot Studio as the entry-level industrial agent builder; named launch partner for AI Apps and Agents category with Cognite. [^28]
- **Google Cloud**: Vertex AI/Gemini backing for Honeywell and others; agent frameworks (A2A Protocol). [^26]

### Adoption Barriers

The five most consistently cited barriers across research and practitioner sources, roughly in order of reported frequency:

1. **Data architecture gaps** (cited by ~80% of companies in McKinsey survey [^24]): Industrial data lives in fragmented, batch-oriented ERP, MES, LIMS, DCS, and SCADA systems with inconsistent data models. Agentic AI requires event-driven, semantically coherent data streams — an infrastructure investment that precedes agent deployment by 12–24 months at most organizations.

2. **Verification and validation absence** (primary finding in arXiv industry study [^13]): No standardized method exists to verify that an agent's outputs are semantically correct, regulatory-compliant, and safe to act on. Human-in-the-loop is currently the only trusted verification mechanism, but it does not scale with output volume. ISO/IEC TS 22440 aims to close this gap but is not yet ratified.

3. **Non-determinism incompatibility with safety-critical environments**: LLM-based agents produce probabilistic outputs that cannot be guaranteed to be deterministic across identical inputs — a direct conflict with IEC 61508 safety integrity level requirements. "If you want to use a tool you need to know what are the bugs" — practitioner quote from arXiv study. [^13]

4. **OT/IT integration complexity**: Legacy OT systems predate modern API paradigms; proprietary industrial protocols (Modbus, PROFINET, EtherNet/IP) are not natively accessible to LLM agents. Context window constraints mean that industrial codebases with millions of lines exceed current model capacity; RAG partially mitigates this but remains difficult to scale. [^13]

5. **Organizational and cultural resistance**: Workers in process industries frequently perceive autonomous agents as surveillance tools or as threats to skilled positions. Deloitte (2026) identified delegating decision-making to autonomous systems as "unfamiliar in traditionally conservative industries." [^30] Gartner predicts over 40% of agentic AI projects will be cancelled by end of 2027 due to unclear business value and inadequate risk controls. [^12]

**Secondary barriers** include: data confidentiality concerns with cloud LLM providers; talent scarcity combining AI expertise with domain knowledge; EU AI Act high-risk classification requirements (up to €35M penalties); and insufficient cybersecurity for agentic OT access (OT ransomware attacks surged 87% YoY in 2025). [^31]

### Safety and Human-in-the-Loop

The challenge of safety in agentic industrial AI is qualitatively different from traditional software safety. Traditional functional safety standards (IEC 61508, IEC 62443, ISA-99) assume that system behavior is deterministic and that failure modes can be enumerated. Agentic AI — adaptive, probabilistic, capable of emergent reasoning — violates both assumptions.

The emerging response has three pillars:

**1. Graduated autonomy frameworks.** Production deployments consistently implement "progressive autonomy": agents begin in observe-only mode, advance to recommendation mode (human approves actions), then to supervised autonomous execution (humans can intervene), and only in mature, well-bounded use cases reach fully autonomous mode. This is exemplified by pharma industry practice [^8], XMPro's deployment methodology [^16], and Deloitte's recommended supply chain implementation model [^30].

**2. Human-on-the-loop architectures.** Rather than a human approving every agent action (human-in-the-loop, which eliminates most efficiency gains), industrial operators are moving to human-on-the-loop designs: agents operate autonomously within defined guardrails, with exception escalation and real-time monitoring dashboards. The practical constraint: "production agents typically execute at most 10 steps before requiring human intervention" (large-scale study of 306 practitioners, 26 domains). [^3]

**3. Standards and regulatory alignment.** ISO/IEC TS 22440 (Parts 1–3, currently Committee Draft stage) is the first international standard specifically designed to integrate AI into functional safety lifecycles — covering reliability, robustness, explainability, and V&V. [^15] IEC 61508-1:2025 was updated to clarify scope in relation to AI and extends requirements to cover human factors. [^14] The EU AI Act classifies AI in safety-critical industrial control systems as high-risk, requiring conformity assessments. In pharma, FDA has not issued AI-specific guidance but applies 21 CFR Part 11 (audit trails, electronic signatures); industry consensus (GAMP 5 risk-based approach adapted for agentic systems) is emerging. [^8]

**OT cybersecurity** adds a distinct safety dimension: autonomous agents with write access to PLCs and DCS controllers represent a significantly expanded attack surface. With 11% of surveyed OT devices carrying known exploitable vulnerabilities and ransomware targeting OT growing 87% YoY in 2025, security architects are requiring zero-trust identity and access management for all agent-to-OT interactions. [^31][^45]

### 2026–2028 Outlook

The 2025 timelines in the original brief are now in the past and largely confirmed: Gartner's prediction that 25% of GenAI enterprises would deploy autonomous agents in 2025 (cited by Deloitte) appears broadly consistent with the 20–30% of manufacturers reported as deploying autonomous systems. Looking ahead to 2026–2028:

**Uses cases most likely to cross from pilot to production (2026–2027):**
- Supply chain orchestration agents (already in production at General Mills, Walmart; Gartner projects 50% SCM adoption by 2030)
- Predictive maintenance orchestration in energy and utilities (energy/utilities market to $4.11B by 2031)
- Pharma quality/deviation management in draft-and-review mode (67% of life sciences in pilot Q1 2026; EU AI Act enforcement timeline accelerating formalization)
- AI-assisted process optimization in O&G (Aker BP/ABB/Cognite now in production)

**Uses cases likely to remain pilot-stage through 2028:**
- Fully autonomous process control of physical assets (e.g., autonomous DCS setpoint adjustment without human override) — blocked by lack of IEC 61508-compatible verification frameworks for non-deterministic agents
- "Lights-out" manufacturing — Samsung's 2030 target; Siemens Erlangen factory launching 2026 is the leading reference, but full lights-out requires robotics maturity beyond current AI agent scope

**Market size estimates (as of mid-2026; ranges reflect differing methodologies):**
- Agentic AI overall (all industries): $7.3–10.8B in 2025/2026, projected $139–156B by 2034 (Fortune Business Insights; various). [^32]
- Agentic AI energy and utilities: $0.87B in 2026, $4.11B by 2031 (Mordor Intelligence [^7]); Precedence Research independently estimates $0.66B in 2025 growing to $14.9B by 2035 at 36.65% CAGR [^38] — scope and end-year differ but 2025 base and CAGR are consistent across both firms.
- SCM software with agentic AI: <$2B in 2025 → $53B by 2030 (Gartner, April 2026). [^5]
- SCM logistics/supply chain agents: $8.67B in 2025 → $16.84B by 2030. [^23]
- McKinsey economic value of AI agents across all business use cases: $2.6–4.4 trillion annually (broad estimate, not industrial-specific). [^33]
- McKinsey advanced industries (automotive, manufacturing, aerospace): $450–650B additional annual revenue potential by 2030 from agentic AI (fetch timed out; from search snippet). [^44]

**The key swing variable is verification and safety standardization.** If ISO/IEC TS 22440 reaches published standard status by 2027 and regulators (FDA, EU AI Act national authorities) provide clear compliance pathways, the number of industrial use cases cleared for unsupervised autonomous action could expand rapidly. If that timeline slips, the "human-in-the-loop as only verification mechanism" constraint will suppress unit economics for the most impactful use cases through 2028.

---

## Data / numbers

| Metric | Value | Year | Source |
|---|---|---|---|
| Agentic AI energy/utilities market size | $0.64B (2025), $0.87B (2026) | 2026 | Mordor Intelligence [^7]; cross-check Precedence Research $0.66B (2025) [^38] |
| Agentic AI energy/utilities CAGR | 36.35% (Mordor, 2026–2031); 36.65% (Precedence, 2025–2035) | 2026 | Mordor Intelligence [^7]; Precedence Research [^38] |
| Agentic AI energy/utilities market by 2031/2035 | $4.11B by 2031; $14.9B by 2035 | 2026 | Mordor Intelligence [^7]; Precedence Research [^38] |
| SCM software with agentic AI, current | <$2B | 2025 | Gartner [^5] |
| SCM software with agentic AI, forecast | $53B | 2030 | Gartner [^5] |
| SCM agentic AI adoption rate | 5% → 60% of SCM users | 2025→2030 | Gartner [^5] |
| Enterprise apps with task-specific AI agents | <5% → 40% | 2025→2026 | Gartner [^34] |
| Agentic AI projects likely cancelled | >40% by end 2027 | 2025 | Gartner [^12] |
| Enterprise AI agents adoption within 2 years | 60%+ plan to deploy | 2026 | Gartner [^34] |
| Deloitte: GenAI enterprises deploying agents | 25% (2025), 50% (2027) | 2025 | Deloitte [^16] |
| Manufacturing organizations deploying autonomous systems | 20–30% | 2026 | Various [^35] |
| Manufacturing agentic AI adoption (2025→2026) | 6% → 24% projected | 2026 | Deloitte (via Dataiku) [^35] |
| McKinsey: companies with real AI ROI | ~5.5% | 2025 | McKinsey [^24] |
| McKinsey: companies that have scaled AI to value | <10% | 2025 | McKinsey [^24] |
| General Mills supply chain savings | $20M+ since FY2024 | 2026 | Case study [^3] |
| General Mills daily shipments assessed autonomously | 5,000+ | 2026 | Case study [^3] |
| Pharma life sciences firms running agentic pilots | 67% | Q1 2026 | Sakara Digital [^8] |
| Pharma deviation investigation cycle time reduction | 40–50% | 2026 | Sakara Digital [^8] |
| Pharma batch record review compression | 60–75% | 2026 | Sakara Digital [^8] |
| Siemens projected productivity increase (vendor claim) | Up to 50% | 2025 | Siemens [^1] |
| Siemens reactive maintenance time reduction | 25% average | 2025 | Siemens [^1] |
| Mining: productivity increase from AI agents | 30–40% | 2025 | XMPro [^16] |
| Mining: safety incident reduction | 60–70% | 2025 | XMPro [^16] |
| Grid fault management: outage duration reduction | Up to 80% | 2025 | Various [^19] |
| Utility: SAIDI/SAIFI improvement from advanced distribution automation | Up to 40% | 2025 | IEEE (via XMPro) [^16] |
| O&G seismic analysis: time reduction | 6–12 months → 8–12 weeks | 2025 | XMPro [^16] |
| McKinsey: AI value in pharma R&D and manufacturing | $18–30B annually | 2026 | McKinsey (via Sakara) [^8] |
| OT devices with known exploitable vulnerabilities | 11% of 1M surveyed | 2025 | Threat intel report [^31] |
| OT ransomware attack increase | 87% YoY | 2025 | Threat intel report [^31] |
| Logistics/supply chain agentic AI market | $8.67B (2025) → $16.84B (2030) | 2026 | Market reports [^23] |
| McKinsey: advanced industries AI revenue uplift potential | $450–650B annually by 2030 | 2025 | McKinsey [^44] (note: fetch unavailable; from search snippet) |

> Disclaimer: Market-size estimates from different firms use divergent scope definitions and methodologies. Figures should be read as order-of-magnitude indicators, not precise forecasts. Vendor-sourced performance claims (Siemens, XMPro) have not been independently verified.

---

## Worked examples

### Example 1: Autonomous Maintenance Orchestration (Manufacturing)
A bearing sensor on a CNC machining center shows rising vibration at 2:47 AM. A traditional Industrial AI system pages an on-call technician with an alert. An agentic system wakes autonomously: it queries CMMS history (last bearing replacement: 14 months ago, 3 months past schedule); checks MRO inventory (2 replacement bearings in stock, same plant); searches technician schedules (qualified technician available from 6 AM); drafts and submits a preventive work order; blocks the affected spindle for a 2-hour maintenance window starting 6:15 AM; and sends a production planning agent a notification to reallocate the affected job to a parallel spindle. The planning agent confirms the reallocation. Total autonomous action: 11 minutes from sensor alert to confirmed work order. No human involved until the technician receives the work order on their mobile device.

### Example 2: Self-Healing Power Grid (Utilities)
A storm causes a line fault on a distribution segment serving 3,200 customers. A grid AI agent detects the fault signature, automatically isolates the affected 400-meter segment using smart switches (OT write action, within pre-authorized autonomy boundary), reroutes power through an adjacent feeder (restoring 2,800 customers within 4 minutes), dispatches an inspection drone to the GPS coordinates of the estimated fault location, and creates a maintenance ticket. Human operator sees a dashboard notification, confirms the agent's actions, and monitors drone video feed. Outage for the remaining 400 customers is bounded to the physical fault repair time rather than the full detection-to-dispatch cycle. This scenario is at production stage in selected advanced utilities as of 2025. [^19]

### Example 3: Pharma Deviation Investigation (Draft-and-Review Mode)
A batch processing deviation is triggered in a biologic fill-finish line. An agentic system autonomously pulls data across batch records, environmental monitoring, equipment history, and the historical deviation database (data assembly compressed from 4–8 hours to 15–45 minutes [^8]); synthesizes a draft investigation report identifying the root-cause hypothesis (a temperature excursion during a 12-minute CIP validation cycle); cross-references the regulatory submission history for similar prior events; and flags the draft for QA review. The QA lead reviews and approves in 45 minutes, then the agent generates the CAPA record and schedules the corrective action. The agent does not submit anything to a regulatory authority or execute any physical action autonomously. Total cycle: 6 hours vs. a pre-agent baseline of 3–5 days.

### Example 4: O&G Agent-to-Agent Orchestration (Aker BP / ABB / Cognite — Production)
ABB Ability AlarmInsight identifies a cluster of correlated alarms on a offshore platform. Rather than presenting the operator with a list of 47 raw alarms, the ABB agent queries the Cognite Data Fusion semantic layer for contextual process data, which passes the enriched context to a risk-assessment agent that cross-references with ABB Ability SafetyInsight process safety data. The combined output is a prioritized, contextualized "Top 3 actions" recommendation delivered to the operator's console. The operator approves the priority ranking and executes the first action. Time-to-decision compressed from 30+ minutes (reading all 47 alarms individually) to under 5 minutes. This deployment at Aker BP is the first publicly confirmed production instance of agent-to-agent orchestration in an O&G operating environment (as of May 2026). [^6]

---

## Open questions / limitations

1. **Production verification**: For most vendor-cited use cases, the boundary between "extended pilot," "limited production," and "full production" is not independently verifiable. Self-reported metrics (Siemens 25% maintenance reduction, XMPro 30–40% mining productivity) are vendor claims without third-party audit.

2. **Safety standard timeline**: ISO/IEC TS 22440 is in Committee Draft stage as of mid-2026. The date of publication as a Technical Specification and subsequent regulatory adoption timeline is uncertain. Until it is ratified and operationalized in industrial qualification practices, the "verification gap" documented in the arXiv study [^13] will continue to constrain production deployments.

3. **Market size divergence**: Analyst firms disagree by factors of 2–5x on overall agentic AI market size (compare $7.3B vs. $10.8B in 2025/2026 estimates for the broad market). Industrial-vertical-specific figures are more defensible but still methodology-dependent. All market size numbers in this report should be treated as directional, not precise.

4. **Lights-out manufacturing**: Whether the Siemens Erlangen reference factory (launching 2026) demonstrates meaningful lights-out autonomous operation or represents a heavily instrumented showcase is not yet verifiable from public reporting.

5. **Regulatory uncertainty**: The EU AI Act's enforcement mechanism for industrial AI agents (specifically the classification of process control agents as "high-risk") remains under interpretation by national competent authorities. This creates planning uncertainty for European industrial operators.

6. **Cybersecurity and adversarial risk**: The documented 87% YoY increase in OT ransomware and the demonstrated ability of AI agents to exploit OT vulnerabilities faster than human defenders can patch (Dragos OT CTF 2025) represents an existential deployment risk that is under-addressed in most vendor marketing literature. [^31]

---

## Glossary

**Agentic AI**: AI systems capable of autonomous, multi-step goal pursuit using tools and feedback loops, without constant human prompting at each step.

**Agent2Agent (A2A) Protocol**: Google-led open standard enabling AI agents from different developers to communicate and collaborate.

**Digital Twin**: A virtual representation of a physical asset, process, or system that is continuously updated from real-world data.

**DCS (Distributed Control System)**: Process control system used in continuous industrial processes (oil refining, chemical production, power generation).

**Draft-and-Review Mode**: Deployment pattern where AI agents prepare outputs (work orders, reports, recommendations) for human approval before execution; mandatory in regulated environments.

**Human-in-the-Loop (HITL)**: Design pattern where a human approves every agent action before it is executed.

**Human-on-the-Loop (HOTL)**: Design pattern where agents operate autonomously within guardrails, with humans monitoring and retaining override capability.

**IEC 61508**: International standard for functional safety of electrical/electronic/programmable safety-related systems; updated in 2025 to address AI scope.

**IEC 62443 / ISA-99**: Standards for cybersecurity of industrial automation and control systems.

**ISO/IEC TS 22440**: Forthcoming international Technical Specification providing requirements and guidance for integrating AI into functional safety lifecycles.

**LLM (Large Language Model)**: Foundation model trained on text that provides natural language understanding and multi-step reasoning capability for AI agents.

**MCP (Model Context Protocol)**: Anthropic-developed open protocol for connecting AI agents to real-time data sources.

**MES (Manufacturing Execution System)**: Software system that connects and monitors machines and work centers on the factory floor.

**MQTT / OPC UA**: Industry-standard protocols for machine-to-machine communication and data exchange in industrial IoT environments.

**Multi-Agent System (MAS)**: Architecture where multiple specialized AI agents collaborate, with one orchestrator agent coordinating sub-agents for complex tasks.

**OpenUSD**: Pixar/NVIDIA-developed universal scene description format for digital twin and simulation interoperability.

**OT (Operational Technology)**: Hardware and software that controls physical devices and processes (PLCs, SCADA, DCS), as distinguished from IT systems.

**PLC (Programmable Logic Controller)**: Industrial computer used to automate electromechanical processes.

**RAG (Retrieval-Augmented Generation)**: Technique combining LLM generation with retrieval of relevant documents to ground responses in domain-specific knowledge.

**SCADA (Supervisory Control and Data Acquisition)**: Industrial control system used for monitoring and controlling infrastructure (power grids, pipelines, water treatment).

**SIL (Safety Integrity Level)**: Discrete level (1–4) specifying the reliability requirements for a safety function under IEC 61508.
