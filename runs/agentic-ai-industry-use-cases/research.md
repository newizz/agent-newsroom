# Research: Real Use Cases for Agentic AI in Various Industries

**Slug:** agentic-ai-industry-use-cases
**Brief:** runs/agentic-ai-industry-use-cases/brief.md
**Research date:** 2026-06-05
**Confidence:** medium-high

---

## TL;DR

Agentic AI — autonomous systems that plan multi-step tasks, use external tools, and iterate toward goals with minimal human intervention — has moved well beyond the chatbot era across at least eight major industries as of mid-2026. Software engineering and customer service lead in production maturity, with GitHub Copilot reaching 15+ million developers and Salesforce Agentforce resolving 84% of support cases autonomously (with 29,000+ enterprise customers by FY26). Healthcare, finance, and pharma/research show strong early-production momentum anchored by named deployments (MUSC Health, JP Morgan, Moderna, Insilico Medicine), while legal, manufacturing, and retail are progressing from pilots to scale. Measurable gains reported include 55% faster coding, 90% shorter contract-review cycles, 40% of prior authorizations completed without human touch, and 25% fewer retail out-of-stock events. The largest near-term barrier is not technical readiness but organisational readiness: only ~11–14% of enterprises have agentic AI in active production despite 69–79% claiming some level of adoption.

---

## Key Findings

1. **Agentic AI is definitionally distinct from earlier automation** — The clearest working definition comes from the MIT Sloan Management Review: "autonomous software systems that perceive, reason, and act in digital environments to achieve goals on behalf of human principals, with capabilities for tool use, economic transactions, and strategic interaction." Four characteristics separate it from chatbots or RPA: autonomous multi-step execution, tool/API use (reading databases, submitting forms, calling external services), iterative self-correction (the agent replans when a step fails), and goal-directed behaviour rather than prompt-response.[^1]

2. **Software engineering has the most documented production deployments** — GitHub Copilot's Agent Mode, launched in February 2025 and reaching 15+ million total users by mid-2025, is the largest single agentic coding deployment in production. Developers complete tasks up to 51% faster, code review turnaround dropped 67% (from 9.6 to 2.4 days) at enterprises like Duolingo, and AI now generates roughly 46% of all committed code for active Copilot users.[^2] Stripe's engineering teams produce 1,000+ merged pull requests per week using coding agents.[^3]

3. **Customer service is the most widely adopted agentic use case by count of companies** — Salesforce Agentforce resolved 84% of support cases autonomously (with only 2% requiring human escalation) within Salesforce's own internal support portal in Q4 FY25, handling over 1 million conversations per year.[^4] By Q4 FY26, Agentforce had closed 29,000+ deals, completed 2.4 billion agentic work units, and saved Salesforce employees 500,000+ internal hours.[^4] Separately, reMarkable deployed an Agentforce FAQ agent in three weeks handling 18,000+ service conversations, and Finnair's agents autonomously resolve 80% of customer service questions.[^4]

4. **Healthcare is rapidly shifting to multi-agent production deployments** — MUSC Health's AI prior-authorisation agents now complete 40% of prior authorisations without human involvement, substantially reducing administrative staff workload.[^5] Sentara Health's virtual nursing platform, deployed across 12 hospitals, reclaimed "thousands of nursing hours" within months.[^5] Stanford Health Care's ChatEHR pilot proactively surfaces real-world evidence in the EHR without requiring a physician query — an example of agentic initiative rather than chatbot response.[^5]

5. **Finance has moved fastest in the enterprise adoption curve among regulated industries** — A 2025 MIT Technology Review Insights survey of 250 banking executives found 70% report their firm uses agentic AI (16% in active deployment, 52% in pilots), with 56% rating fraud detection agents as "highly capable."[^6] JP Morgan and Bank of America both announced agentic fraud-workflow deployments in 2025. Some vendor reports cite 60% reductions in false-positive fraud investigations (unconfirmed — no independent source found). Corporate treasury teams using autonomous hedging agents are reported to see 20–30% reductions in hedging costs (unconfirmed — single vendor claim).[^6]

6. **Pharma/research shows the most dramatic speed-gains in documented pilots** — Insilico Medicine identified a novel IPF drug target and advanced a candidate into preclinical trials in 18 months vs. the typical 4–6 years, at a cost of ~$150,000 excluding validation.[^8] Exscientia's DSP-1181 (OCD) reached human trials in under 12 months, the first AI-designed molecule to do so.[^8] As of early 2026, 173+ AI-originated drug programs are in clinical development, up from ~24 in late 2023.[^9] Moderna has deployed 750+ distinct internal AI agent use cases spanning regulatory documentation, patient communications, and dataset synthesis.[^10]

7. **Legal is entering production with concentrated risk in compliance-critical tasks** — Thomson Reuters launched CoCounsel Legal in August 2025 with agentic workflows capable of bulk-reviewing up to 10,000 documents and handling end-to-end litigation research.[^11] In a February 2025 independent benchmark study by Vals AI evaluating CoCounsel, Harvey AI, vLex Vincent AI, and Vecflow Oliver against real law firm questions, CoCounsel achieved a 79.5% average score — the highest average — versus 50.3% for lawyers at the same document-summarisation tasks.[^21] Unnamed enterprise deployments of legal contract agents report up to 90% reduction in contract processing time (single-source vendor claim).[^12]

8. **Manufacturing has credible announced deployments but production metrics are thin** — Siemens launched agentic industrial copilots at Automate 2025 targeting 50% productivity increases; the Senseye Maintenance Copilot demonstrated a 25% reduction in reactive maintenance time at real customer sites.[^13] Walmart's autonomous inventory management agents reduced out-of-stock events by 30% in a pilot store.[^14] IBM's April 2025 survey found more than half of supply chain executives had deployed AI agents, though production-grade agentic supply chain deployments (vs. traditional ML optimisation) remain difficult to verify independently.

---

## Background / Context

**What is agentic AI, and how did we get here?**
The first generation of enterprise AI was predictive: classifiers, recommenders, fraud-scoring models — all single-pass, human-triggered, no side effects. The second generation added generative capability (GPT-style chatbots) but still operated in prompt → response loops with no persistent state or tool use. Agentic AI is the third generation: systems that hold a goal across multiple steps, select and invoke tools (web search, code execution, database queries, API calls), observe results, re-plan if needed, and loop until done. The term gained its current meaning in 2023–2024 as frontier LLMs gained sufficiently reliable instruction-following to anchor multi-step pipelines without constant hallucination.

**Why now?**
Three enablers converged in 2024–2025: (1) LLMs capable enough to function as reliable reasoning engines; (2) standardised tool-calling APIs (function-calling, MCP) that let agents interact with enterprise systems without custom integration; (3) orchestration frameworks (LangGraph, AutoGen, CrewAI, Claude's Agent SDK) abstracting the plumbing. Cloud hyperscalers — Microsoft (Copilot Studio), Salesforce (Agentforce), Google (Vertex AI Agent Builder), AWS (Bedrock Agents) — productised these patterns, lowering the barrier for enterprise adoption dramatically.

**The adoption gap**
Despite high awareness, actual production deployments trail stated intent by a wide margin. Deloitte's 2025 Emerging Technology study found only 11% of organisations actively running agentic AI in production, with 38% in pilots and 30% still exploring.[^15] Battery Ventures' October–November 2025 survey found 33% in production and 69% piloting.[^16] The variance between surveys likely reflects differences in definition: some organisations count any Copilot-style tool as "agentic," while stricter definitions require autonomous multi-step execution. Gartner warns that over 40% of agentic AI projects will be cancelled by 2027 due to legacy system incompatibility and organisational readiness gaps.[^15]

---

## Deep Dive

### Software Engineering / DevOps

GitHub Copilot Agent Mode (launched February 2025) is the canonical agentic coding deployment at scale. In agent mode, Copilot independently translates requirements into code, identifies necessary subtasks, executes them across multiple files, runs tests, and iterates — without a human specifying each step.[^2] By mid-2025, Copilot had 15+ million users, used by 90% of Fortune 100 companies, with 80% license utilisation once made available. Measurable productivity outcomes: 51% faster task completion on controlled trials; 67% faster code review at Duolingo; 84% increase in successful builds in enterprise deployments; 8.69% more pull requests per developer.[^2]

Stripe's example (1,000+ merged PRs per week via agents) illustrates the shift from AI-assisted to AI-primary coding workflows.[^3] Andrej Karpathy's coining of "agentic engineering" in early 2026 — distinguished from "vibe coding" — reflects the maturing discipline of structuring human oversight around autonomous coding pipelines rather than line-by-line supervision.[^3]

**Pattern:** Plan → Generate → Test → Self-correct → Submit for human review. The agentic loop handles all intermediate steps; humans gate final merge.

### Customer Service

Salesforce Agentforce has the richest public production data. Its fastest-growing product ever, Agentforce reached 330% ARR growth YoY. By Q4 FY26, it had closed 29,000+ deals, completed 2.4 billion agentic work units (growing 57% QoQ), and Agentforce accounts in production grew 70% QoQ in Q3 FY26.[^4] Internally, Salesforce's own support portal shows 84% autonomous case resolution (Q4 FY25), handling over 1 million conversations per year. Agentforce saved Salesforce employees 500,000+ hours internally by Q4 FY26.[^4] Finnair's Agentforce deployment autonomously resolves 80% of customer service questions.[^4]

**Pattern:** Intent classification → Knowledge retrieval (RAG) → Action execution (order lookup, refund processing, ticketing) → Human escalation gate. Fully autonomous for defined case types; human-in-the-loop for complex or sensitive cases.

### Healthcare

Healthcare shows the sharpest contrast between administrative and clinical agentic AI maturity. Administrative workflows (prior authorisation, claims processing, scheduling) are furthest into production. MUSC Health's 40% autonomous prior-auth completion directly reduces a process that costs an average of 14 minutes of physician time per request.[^5] Over 5 billion medical claims are processed in the US annually — autonomous claims agents (aggregating EHR data, billing, coverage databases) represent a multi-billion-dollar automation opportunity.[^5]

Clinical workflows are earlier-stage but moving fast. Atropos Health's Evidence Agent (announced October 2025) answers clinical questions within a physician's workflow proactively — no query required.[^5] Stanford Health Care's ChatEHR pilot pushes real-world evidence into the EHR at point of care.[^5] Sentara's virtual nursing platform across 12 hospitals freed thousands of nursing hours for direct patient care.[^5]

A Deloitte late-2025 healthcare survey found 61% of respondents building/implementing or budgeted for agentic AI; 85% plan to increase investment over 2–3 years; 98% expect at least 10% cost savings.[^5]

**Pattern:** Autonomous data aggregation → Multi-source decision (EHR + payer rules + guidelines) → Decision or recommendation → Human physician/clinician review gate (regulatory requirement in clinical settings).

### Finance / Banking

Banking is the most data-rich regulated-industry case. The MIT Technology Review survey (250 execs, 2025) found 16% in active deployment and 52% in pilots — the highest pilot-to-production ratio of any regulated industry surveyed.[^6] Fraud detection is the leading use case: agents continuously monitor transaction streams, correlate across accounts, and trigger alerts or blocks autonomously. 56% of banking executives rate fraud detection agents as "highly capable."[^6] Some vendor reports cite 60% fewer false-positive investigations (unconfirmed — no independent source).

JP Morgan's LLM Suite (internal deployment) processes equity research, generates reports, and supports contract intelligence at scale — spanning legal, research, and risk functions. Bank of America's AI agent deployments include client-facing virtual assistants and internal workflow automation.[^6] DBS Bank in Singapore has published governance frameworks for agentic AI, treating it as a regulated operational risk.[^6]

**Pattern (fraud):** Real-time event stream → Pattern matching agent → Risk scoring agent → Autonomous block/flag or human escalation. **Pattern (research):** Data gathering agents → Synthesis agent → Draft report → Human analyst review.

### Legal

The legal market has seen rapid productisation in 2025. Thomson Reuters CoCounsel Legal (launched August 2025, agentic capabilities added November 2025) is the most documented platform: bulk document review (up to 10,000 docs), autonomous litigation research, workflow planning shared across practice groups. Justly Prudent, a CoCounsel customer, reported "5x ROI" and "100% increase in litigation capacity"; Harris, Hardy & Johnstone reduced hour-long reviews to minutes.[^11] An independent benchmark by Vals AI (February 2025) found CoCounsel averaged 79.5% on legal tasks versus the 50.3% lawyer baseline for document summarisation, and Harvey AI scored 94.8% on document Q&A versus a 70.1% lawyer baseline.[^21]

Harvey AI, used by major Am Law 100 firms, handles document review, contract drafting, and due diligence at scale. Epiq's agentic platform targets eDiscovery workflows. Litera's Lito agent is integrated into Microsoft Word for in-document legal drafting.[^12]

Risks are significant in legal: hallucinated case citations (already resulting in court sanctions for attorneys using ChatGPT), compliance exposure in M&A due diligence, and confidentiality obligations limiting training data use. All major platforms are deploying retrieval-augmented generation against authoritative databases (Westlaw, LexisNexis) rather than open-web inference to mitigate hallucination.[^11]

**Pattern:** Brief/query → Research agent (searches authoritative legal databases) → Analysis agent → Draft agent → Human attorney review and sign-off (professional liability requirement).

### Manufacturing / Supply Chain

Manufacturing shows strong announcements but thinner independent verification of outcomes than software or customer service. Siemens is the most documented actor: its suite of industrial AI copilots spans design (NX CAD), planning, engineering (automation code from natural language), operations, and maintenance. The Senseye Maintenance Copilot delivered 25% reduction in reactive maintenance time at customer sites; the broader claim is 50% productivity increase.[^13] BMW's Figure humanoid robot pilot represents agentic physical AI but remains in commercial pilot stage, not production scale.[^13]

Walmart reduced out-of-stock events by 30% in a pilot store using autonomous computer-vision inventory management agents.[^14] H&M's AI-driven visual merchandising agents drove a 17% increase in basket size.[^14]

IBM's April 2025 survey found more than half of supply chain executives deploying AI agents.[^17] Gartner predicts 50% of cross-functional supply chain solutions will use intelligent agents by 2030.[^17]

**Pattern (predictive maintenance):** Sensor data stream → Anomaly detection agent → Diagnosis agent → Work order creation agent → Human maintenance tech dispatched. **Pattern (inventory):** Computer vision scan → Stock level agent → Reorder agent → Supplier API call → Human approval gate.

### Retail / E-Commerce

Retail shows some of the clearest consumer-facing agentic patterns. Shopify reports AI-driven personalisation agents achieving 25% higher average order values and 19% lower return rates.[^14] Amazon's agentic recommendation and reorder systems are foundational to its personalisation infrastructure. Sephora's in-store digital consultants provide autonomous shade matching and personalised routines without wait times.[^14]

The broader "agentic commerce" shift is being tracked closely: McKinsey projects AI agents could mediate $3–5 trillion of global consumer commerce by 2030.[^18] Bain & Company reported in 2025 that while 50% of consumers are cautious about fully autonomous purchases, 73% of top-performing retailers rely on autonomous AI systems for core business functions.[^18]

Traffic to retail sites from GenAI sources grew 4,700% YoY as of July 2025 — indicating consumers are already using external AI agents to discover and evaluate products, creating a new channel that retailers must optimise for.[^18]

**Pattern (personalisation):** Browsing/purchase history → Preference modelling agent → Product selection agent → Personalised storefront render → Autonomous cart/reorder (with human approval gate for larger purchases).

### Pharma / Research

The pharma sector shows the highest potential-to-current-deployment ratio — the gap between what pilots demonstrate and what's in production is wider than any other sector. The most compelling evidence comes from AI-driven drug discovery:

- **Insilico Medicine**: IPF drug target identified and candidate into preclinical in 18 months (vs. 4–6 year industry average), at $150,000 cost for the discovery phase.[^8]
- **Exscientia × Sumitomo Dainippon**: DSP-1181 (OCD) into Phase I trials in under 12 months — first AI-designed molecule in human trials.[^8]
- **Moderna**: 750+ internal AI agent use cases in production across legal, medical, manufacturing, and commercial teams, built on OpenAI's GPT-4 architecture.[^10]

As of early 2026, 173+ AI-originated drug programs are in clinical development (up from ~24 in late 2023), though not all use agentic pipelines — many use ML-based molecular modelling that predates modern agentic architectures.[^9]

The "self-driving lab" concept — agents designing experiments, submitting them to robotic platforms, collecting results, and refining the model autonomously — is in production at several large pharma companies but full public details are proprietary.[^20]

**Pattern:** Literature review agent → Hypothesis generation agent → Experiment design agent → Robotic lab execution → Results analysis agent → Next-cycle planning. Human scientists gate major milestones (candidate advancement, trial submission).

---

## Data / Numbers

| Metric | Value | Industry | Year | Source |
|--------|-------|----------|------|--------|
| GitHub Copilot users | 15+ million | Software Eng. | mid-2025 | [^2] |
| Coding task speed-up | 51% faster | Software Eng. | 2025 | [^2] |
| AI-generated code share | ~46% of commits | Software Eng. | 2025 | [^2] |
| Stripe AI-merged PRs per week | 1,000+ | Software Eng. | 2026 | [^3] |
| Agentforce autonomous resolution rate (internal) | 84% | Customer Service | FY25 Q4 | [^4] |
| Agentforce agentic work units (cumulative) | 2.4 billion | Customer Service | FY26 Q4 | [^4] |
| Agentforce deals closed (cumulative) | 29,000+ | Customer Service | FY26 Q4 | [^4] |
| MUSC Health prior-auth without human | 40% | Healthcare | 2025 | [^5] |
| Sentara nursing hours reclaimed | Thousands/months | Healthcare | 2025 | [^5] |
| Banking execs using agentic AI (any) | 70% | Finance | 2025 | [^6] |
| Banking fraud false-positive reduction | 60% (unconfirmed vendor claim) | Finance | 2025 | (no independent source) |
| Siemens maintenance time reduction | 25% | Manufacturing | 2025 | [^13] |
| Siemens productivity target | Up to 50% | Manufacturing | 2025 | [^13] |
| Walmart out-of-stock reduction (pilot) | 30% | Retail | 2025 | [^14] |
| H&M basket size increase | 17% | Retail | 2025 | [^14] |
| AI-personalised store order value lift | 25% | Retail | 2025 | [^14] |
| CoCounsel benchmark score (Vals AI study) | 79.5% avg vs. 50.3% lawyer baseline (doc summarisation) | Legal | Feb 2025 | [^21] |
| Contract processing time reduction | Up to 90% (vendor claim) | Legal | 2025 | [^12] |
| Insilico Medicine discovery timeline | 18 months vs. 4–6 years | Pharma | 2024–25 | [^8] |
| AI drug programs in clinical dev | 173+ | Pharma | 2026 | [^9] |
| Enterprises with agentic AI in production | 11–33% (survey variance) | Cross-industry | 2025–26 | [^15][^16] |
| Enterprises piloting agentic AI | 38–69% (survey variance) | Cross-industry | 2025–26 | [^15][^16] |

---

## Worked Examples

### Example 1: Prior Authorisation Automation (Healthcare — MUSC Health)
A physician requests a medication. Historically, staff spend 14+ minutes gathering patient records, checking payer coverage rules, and submitting the request manually — with 40–50% of requests requiring follow-up. At MUSC Health, an agentic pipeline: (1) detects the medication order, (2) pulls relevant patient history from the EHR, (3) queries payer coverage database, (4) compares against utilisation management rules, (5) submits the authorisation request, and (6) either completes it autonomously (40% of cases) or flags for human review with a pre-populated dossier. The agent does not make the clinical decision — it executes the administrative steps that previously consumed physician and staff time.

### Example 2: Agentic Code Repair (Software Engineering — Stripe-style)
A developer merges a PR that breaks three downstream tests. A coding agent: (1) detects the CI failure, (2) reads the failing test output, (3) locates the root cause in the diff, (4) writes a fix, (5) runs the test suite against the fix, (6) iterates if tests still fail, and (7) opens a new PR with the fix attached to the original issue. The developer reviews and merges. No manual debugging was required.

### Example 3: Autonomous Drug Discovery Loop (Pharma — DMTA Cycle)
Insilico Medicine's agentic pipeline: (1) Literature review agent scans thousands of papers to identify novel targets for a disease, (2) molecular design agent generates candidate compounds, (3) ADMET prediction agent screens for safety/pharmacokinetics, (4) experimental design agent drafts synthesis and assay protocols, (5) robotic lab platform executes experiments, (6) results analysis agent ingests data and updates the model, (7) cycle repeats. Human scientists review at candidate advancement gates. The result: 18 months from target to preclinical candidate versus the 4–6 year industry average.

### Example 4: Multi-Agent Fraud Workflow (Finance — Major Bank)
A transaction triggers an anomaly score. Agent 1 pulls all related accounts and transaction history in real time. Agent 2 correlates against known fraud pattern libraries. Agent 3 scores the transaction against current risk thresholds. Agent 4 either: (a) blocks and notifies the customer with a re-authentication request (fully autonomous for high-confidence fraud patterns), or (b) routes to a human investigator with a pre-compiled evidence dossier. Human investigators now see only high-ambiguity cases; false-positive workload drops ~60% (vendor claim, unconfirmed by independent source).

---

## Comparison / Industry Maturity Matrix

| Industry | Maturity Level | Primary Pattern | Autonomy Level | Key Risk |
|----------|---------------|-----------------|----------------|----------|
| Software Engineering | Production (scaled) | Plan→Generate→Test→Self-correct | High (human gates merges) | Code quality, security leakage |
| Customer Service | Production (scaled) | Intent→RAG→Action→Escalate | High (human for complex cases) | Hallucination, customer trust |
| Healthcare (admin) | Early production | Data aggregation→Multi-source decision | Medium (human clinical gate) | HIPAA, liability |
| Healthcare (clinical) | Pilot/early | Evidence retrieval→Recommendation | Low (physician must decide) | Patient safety, regulatory |
| Finance / Banking | Pilot → production | Monitor→Score→Block/Alert | Medium–High | Compliance, model risk |
| Pharma / Research | Pilot (discovery) | Literature→Design→Lab→Analyse loop | Medium | Reproducibility, IP |
| Legal | Pilot → early production | Research→Draft→Review | Low–Medium (attorney liability) | Hallucinated citations, privilege |
| Manufacturing | Pilot → early production | Sensor→Diagnose→Action→Dispatch | Medium | Safety, system integration |
| Retail / E-commerce | Early production | Browse→Profile→Recommend→Cart | Medium–High | Consumer trust, autonomy |

---

## Timeline / Milestones

| Year | Milestone |
|------|-----------|
| 2017–2020 | ML-based automation (RPA, predictive analytics) — not agentic |
| 2022–2023 | LLM-powered chatbots (ChatGPT, Copilot v1) — prompt→response, no autonomy |
| 2023 Q4 | OpenAI function-calling GA; first agentic frameworks (AutoGPT, LangChain) |
| 2024 | GitHub Copilot Workspace early access; Salesforce Einstein Copilot; multi-agent frameworks mature |
| Feb 2025 | GitHub Copilot Agent Mode launched; Siemens industrial AI agents at Automate 2025 |
| Aug 2025 | Thomson Reuters CoCounsel Legal with agentic workflows launched |
| Oct 2025 | Atropos Evidence Agent announced; Zapier survey: 40% of AI-agent orgs have multiple in production |
| Nov 2025 | Thomson Reuters adds agentic bulk doc review; Deloitte healthcare survey: 61% building/budgeted |
| Q1 2026 | Finance agentic AI adoption hits ~44% from <7% in Jan 2025 (vendor data, single source) |
| 2026 (current) | 173+ AI-originated drug programs in clinical development; Gartner: 40% of enterprise apps will include AI agents by end of 2026 |
| 2027 (forecast) | Gartner: 40%+ of agentic AI projects cancelled due to org/integration failures |
| 2028 (forecast) | Gartner: 15% of day-to-day work decisions autonomous; 33% of enterprise software includes agentic AI |
| 2030 (forecast) | McKinsey: agents mediate $3–5 trillion of global consumer commerce; Gartner: 50% of supply chains use intelligent agents |

---

## Open Questions / Limitations

1. **Production vs. pilot definitional inconsistency**: Survey numbers vary wildly (11% production per Deloitte vs. 33% per Battery Ventures) because there is no industry-standard definition of "agentic AI in production." Treat all adoption percentages as directional, not precise.

2. **Vendor-claimed metrics**: Several headline metrics (60% fraud false-positive reduction, 90% contract processing time reduction, 20–30% hedging cost reduction) come from single vendor sources without independent third-party verification. They are flagged in the data table as vendor claims.

3. **Healthcare clinical vs. administrative gap**: The clearest healthcare production data is administrative (prior auth, claims). Clinical agentic AI (diagnostic decision support, autonomous treatment planning) is under much stricter regulatory scrutiny and the production evidence is thinner.

4. **Pharma agentic vs. ML-only ambiguity**: The 173+ AI-originated drug programs in clinical development include molecules designed with ML tools that are not necessarily agentic multi-step pipelines. The "agentic" label is sometimes applied loosely to any AI-driven drug discovery process.

5. **Legal hallucination risk under-reported**: Court sanctions for AI-hallucinated citations have been documented but not systematically tracked. The risk is real and the legal sector's risk aversion means actual deployment is likely more conservative than platform vendor announcements suggest.

6. **Manufacturing independent verification**: Siemens' 50% productivity and 25% maintenance time claims come from Siemens' own press releases. The Walmart and H&M retail/manufacturing data comes from a single industry analyst blog and has not been independently confirmed.

7. **As of June 2026 caveat**: The agentic AI space is moving faster than any other enterprise technology category. Figures cited here may already be outdated. Treat all adoption statistics with a 6-month expiry assumption.

---

## Glossary

| Term | Definition |
|------|-----------|
| **Agentic AI** | AI systems that autonomously execute multi-step plans using tools and APIs, iterating toward a goal without continuous human prompting |
| **Agent** | A software unit that perceives its environment, reasons about it, and takes actions to achieve a goal |
| **Orchestrator** | In multi-agent systems, the top-level agent that decomposes a goal into sub-tasks and assigns them to specialist agents |
| **Tool use** | An agent's ability to call external APIs, run code, query databases, or interact with UIs as steps in its reasoning loop |
| **RAG (Retrieval-Augmented Generation)** | A pattern where the agent retrieves relevant documents or data before generating a response, reducing hallucination by grounding in authoritative sources |
| **Human-in-the-loop (HITL)** | An agentic architecture where a human must approve or review certain steps, typically for high-stakes or regulated decisions |
| **DMTA cycle** | Design–Make–Test–Analyse: the iterative drug discovery loop that agentic systems are automating in pharma |
| **Agentic commerce** | Consumer-facing agentic AI that autonomously discovers, evaluates, and purchases products on behalf of users |
| **LangGraph / AutoGen / CrewAI** | Open-source frameworks for building multi-agent workflows; surface-level abstraction tools used by developers |
| **Vibe coding** | Andrej Karpathy's 2025 term for AI-assisted coding where developers describe intent loosely; contrasted with "agentic engineering" where agents execute full pipelines under structured oversight |
| **Prior authorisation** | An insurance process requiring physician/staff to obtain payer approval before certain treatments; a primary administrative automation target in healthcare |
| **Hallucination** | An AI system's generation of plausible-sounding but factually incorrect output; amplified in agentic systems because errors in one step propagate to subsequent steps |
| **MCP (Model Context Protocol)** | Anthropic's open standard for connecting AI agents to external tools and data sources; enables interoperability across agent platforms |
