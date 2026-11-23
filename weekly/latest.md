---
title: "AI Weekly Reads - 2026-11-07"
aliases:
  - "AI Weekly Reads - 2026-11-07"
  - "AI Weekly Reads 2026-11-07"
created: "2026-11-07"
type: "weekly-book"
status: "ready"
language: "en"
---

# AI Weekly Reads

Week of 2026-11-07

[Download the latest EPUB for Kindle](latest.epub)

## Contents

1. [Latent Space / Podcast] 2026-11-07 - Deep Dive: Anthropic S-1 Myths and Mythos — Jamin Ball, Altimeter
2. [Latent Space / Podcast] 2026-11-06 - Controlling Biology - Fabian Theis, Helmholtz Munich
3. [No Priors / Podcast] 2026-11-05 - Tokenization, Agentic Trading, Harmonic: Robinhood's Mission to Expand Ownership with CEO Vlad Tenev
4. [Unsupervised Learning / Podcast] 2026-11-05 - Ep 97: Jev Creator on Decision Models, Benchmark Fatigue & Why the Labs Missed It
5. [Training Data / Podcast] 2026-11-05 - A Model For Everyone: How Ronak From Trajectory Is Building Products For Continual Learning
6. [Latent Space / Podcast] 2026-11-04 - ⚡ Behind Latent Space: A Rare Look Inside the Pod | AIEi Shanghai
7. [AI & I by Every / Podcast] 2026-11-04 - The Inside Story of the 50 Who Built Modern AI With Kevin Roose
8. [Latent Space / Podcast] 2026-11-03 - ⚡️ The 2026 Software Factory Standard — Zach Lloyd, Warp.dev
9. [Unsupervised Learning / Podcast] 2026-11-02 - Ep 96: Nebius CTO on Racing the Hyperscalers Before AWS Wakes Up
10. [Latent Space / Podcast] 2026-11-02 - Building Legal Agents When You Can't See the Data - Jacob Lauritzen, CTO of Legora
11. [Lenny's Podcast / Podcast] 2026-11-01 - How a 19-year-old intern built the growth engine behind this $2B AI company | Hector Serrano
12. [Latent Space / Podcast] 2026-10-31 - ⚡ Building ChatGPT for Finance — Joseph Kim, OpenAI's Head of Financial Services
13. [Latent Space / Podcast] 2026-10-31 - Using Agents for Long-Horizon Financial Work — Aman Singh, Arca

## Reading Notes

# Deep Dive: Anthropic S-1 Myths and Mythos — Jamin Ball, Altimeter

- **Published:** 2026-11-07
- **Podcast:** [Latent Space](https://www.youtube.com/watch?v=P735f1xlpL0)
- **Speaker:** Jamin Ball, Partner at Altimeter Capital and author of *Clouded Judgment* newsletter

## One-Sentence Takeaway
Anthropic’s S-1 reveals a 7x efficiency gain in inference, 85% gross margins, and $134B cash on hand, proving frontier AI labs can be both capital-intensive and accidentally profitable.

## Short Summary
Anthropic’s IPO filing offers unprecedented visibility into the economics of a frontier AI lab: rapid revenue growth (14x year-over-year), extreme capital efficiency (7x inference cost improvement), and strong margins (85% gross, 20% free cash flow) despite massive compute commitments ($856B total). The business model hinges on staying at the frontier—80% of revenue now comes from models ≤6 months old—while managing the tension between reinvesting in compute and maintaining profitability.

The debate centers on whether such efficiency gains are repeatable, whether demand for frontier models will sustain growth, and whether the cost of staying ahead (training, alignment, and infrastructure) will outpace revenue. The S-1 also highlights the strategic role of going public: accessing debt markets for data center financing, providing liquidity to employees, and democratizing access to AI upside.

## Main Ideas
- **Efficiency as a moat**: Anthropic’s serving compute spend rose 2.3x over a year while revenue grew 14x, implying a 7x improvement in inference efficiency—a key driver of profitability despite high capital intensity.
- **Frontier models dominate revenue**: 80% of Anthropic’s revenue in Q3 came from models ≤6 months old, underscoring the economic value of staying at the frontier and the rapid depreciation of older models.
- **Capital structure and IPO rationale**: Going public enables cheaper debt financing for data centers (currently >10% interest rates for private deals), credit ratings, and broader investor access, while private markets struggle to syndicate multi-billion-dollar GPU debt.
- **Compute demand outpaces supply**: Labs are compute-constrained, with Anthropic committing to $100B+ annual spend on compute (including training, alignment, and inference), yet demand for frontier models continues to outstrip supply.
- **Profitability is a choice**: Anthropic’s 20% free cash flow margins suggest it could prioritize profitability, but reinvestment in compute (currently only 27% allocated to revenue-generating inference) is likely to reduce margins temporarily to sustain growth.

## Questions And Answers
- **Why IPO now?**
  Public markets offer cheaper debt for data centers, credit ratings, and liquidity for employees/investors, while private debt markets are effectively closed for large GPU financing deals.

- **How is Anthropic so efficient?**
  According to the guest, a 7x improvement in inference efficiency over the past year (from better model architectures, serving optimizations, and internal tooling) allowed revenue to outpace compute spend growth.

- **Can efficiency gains continue?**
  Unclear. Some gains may be one-time (e.g., early-stage optimizations), but Jevons Paradox suggests lower costs could unlock new use cases, sustaining demand and revenue growth even as prices drop.

- **Will frontier models remain economically dominant?**
  Yes, per the guest: while open-weight models may capture token volume share, frontier models will likely retain the majority of *dollar* share due to their superior performance on high-value tasks.

## Notable Details
- Anthropic reports $141B raised to date with $134B cash on hand, implying ~$7B lifetime burn to reach $16.8B quarterly revenue (Q3).
- Compute allocation: Only 27% of Anthropic’s compute spend goes to revenue-generating inference; the rest is R&D, training, or alignment.
- Model cost trends: Each new model family (e.g., Claude 5.1, Opus 5.5) reduces the cost to complete tasks by 25–40% compared to prior versions.
- Enterprise penetration: 50% of the Fortune 500 use Anthropic, but spend is only 0.1% of their expenses—suggesting significant headroom for growth (e.g., Stripe spends 1% on tokens today, targeting 15–20%).
- Compute commitments: Anthropic’s $856B in total commitments (including multi-year deals) annualizes to ~$100B/year, which the guest argues is coverable by revenue growth and reallocating existing compute to inference.
- Stock-based compensation: Even after adjusting free cash flow for equity grants, Anthropic remains ~8% free cash flow positive—a rarity for pre-IPO software companies.

## Actionable Takeaways
- Watch for **compute margin trends**: If Anthropic can maintain >50% compute margins (revenue minus all compute costs) while scaling, it signals durable efficiency.
- Monitor **model release cadence**: Frontier revenue share (80% from ≤6-month-old models) suggests delays in new releases could impact growth.
- Assess **debt market dynamics**: Public listings may become a prerequisite for AI labs to secure affordable data center financing as private debt markets tighten.
- Track **enterprise spend ratios**: The shift from 0.1% to 1–20% of expenses on tokens (as seen at Stripe) could foreshadow broader adoption curves.
- Evaluate **alignment compute costs**: Rising spend on safety/verification (potentially 5–20% of compute in the future) may pressure margins but is non-negotiable for frontier labs.

## People, Companies, Tools, And Links Mentioned
- [Anthropic](https://www.anthropic.com)
- [Altimeter Capital](https://www.altimeter.com)
- [Clouded Judgment newsletter](https://www.cloudedjudgement.substack.com)
- OpenAI
- Stripe
- SpaceX
- Google (Gemini, Carbon)
- Meta
- Redpoint Ventures
- Theory Ventures
- Bill Gurley
- John Collison
- Mark Chen (OpenAI)
- PHP vulnerability patch
- AWS (EC2, S3)
- NVIDIA
- TSMC
- ASML

## Reading Priority

Medium – The S-1 provides the first comprehensive look at the unit economics of a frontier AI lab, revealing counterintuitive profitability and efficiency gains that reshape assumptions about the industry’s sustainability.

***

# Controlling Biology - Fabian Theis, Helmholtz Munich

- **Published:** 2026-11-06
- **Podcast:** [Latent Space](https://lspace.beehiiv.com/podcast/s/latent_space_the_ai_engineer_podcast/controlling_biology_-_fabian_theis_helmholtz_munich_1)

## One-Sentence Takeaway
Virtual cell models are evolving from static mapping to predictive world models that can guide experiments, with scaling data and improved perturbation prediction unlocking new frontiers in systems biology and drug discovery.

***

## Short Summary
Fabian Theis argues that virtual cell models—once limited to mapping and prediction—are now capable of steering experiments via inverse generative models like Lab Compass, enabling closed-loop optimization in biology. The shift is driven by explosive growth in perturbation data (e.g., CRISPR, drug screens, organoids) and advances in foundation models for single-cell and spatial omics, though linear baselines remain surprisingly competitive for simpler tasks.

The conversation highlights tensions between inductive bias and data scale, the need for robust metrics in benchmarking, and the commercialization challenges for virtual cell platforms, which often pivot to drug development due to clearer monetization paths. Theis also emphasizes the importance of integrating computational and wet-lab expertise, both in training (via the "Y model" of co-advising) and in cultural collaboration to enable lab-in-the-loop systems.

***

## Main Ideas
- **From mapping to steering**: Virtual cell models are progressing from static representations (e.g., cell atlases) to predictive "world models" that can propose experiments to reach desired states, enabled by inverse generative models like Lab Compass.
- **Data scale unlocks complexity**: The explosion of perturbation data (e.g., 10M+ transcriptomes, organoid screens) and multi-modal assays (spatial omics, proteomics) is enabling richer models, though linear baselines still perform well for simple tasks like cell-type classification.
- **Inductive bias vs. data**: Hybrid models with light priors currently outperform purely data-driven or heavily biased approaches in biology, but scaling laws suggest data-rich regimes will favor flexible, less constrained models (e.g., AlphaFold’s evolution).
- **Benchmarking pitfalls**: Poor metrics and baselines (e.g., linear models) can mislead progress in virtual cell challenges; robust evaluations (e.g., ARC’s Virtual Cell Challenge) reveal that nonlinear methods like flow matching excel for complex tasks like perturbation prediction.
- **Commercialization hurdles**: Virtual cell platforms struggle to monetize without pivoting to drug development, but coupling modeling with unique data generation (e.g., organoid perturbation atlases) creates defensible value for pharma partnerships.

***

## Questions And Answers
**Q: What is a perturbation in biology, and why does it matter for virtual cells?**
A: A perturbation is any input that alters a cell’s state—e.g., CRISPR knockouts, drugs, signaling molecules, or environmental conditions. Modeling perturbations is central to virtual cells because it enables predicting how cells respond to interventions, a prerequisite for designing experiments or therapies.

**Q: How do organoids advance virtual cell modeling?**
A: Organoids (miniature, multicellular systems like "mini-brains" or beating heart clusters) capture emergent behaviors absent in single-cell lines, but modeling them requires new representations (e.g., graphs, spatial distributions) and richer data. They bridge the gap between in vitro simplicity and in vivo complexity.

**Q: Why do linear models often outperform complex ones in biology?**
A: For tasks like cell-type classification or simple perturbation prediction, linear models (or linear shifts in latent space) are robust to noise and overfitting, especially with limited data. Complexity only pays off for harder tasks (e.g., predicting neighboring cell states in spatial omics).

**Q: What’s the "Y model" for training students?**
A: A co-advising framework where each student has two mentors: one methodological (e.g., ML) and one domain-specific (e.g., wet-lab biology). This forces cross-disciplinary integration and produces researchers who can translate biological problems into computational solutions.

***
***
## Notable Details
- **Lab Compass**: An inverse generative model that proposes experiments to reach target cell states, tested in iterative lab-in-the-loop cycles for hematopoiesis (blood cell formation).
- **Scaling laws in biology**: Theis’s lab demonstrated scaling behavior in foundation models for single-cell data (e.g., 350M cells, 100M parameters) with tasks like cross-species latent space alignment and neighbor-cell prediction.
- **ARC Virtual Cell Challenge**: A benchmark where flow matching-based models (e.g., Self-Flow) outperformed linear baselines for perturbation prediction, but only after addressing metric exploitation.
- **Data generation at scale**: ParseBio’s "GigaLab" produced 10M transcriptomes in a single experiment; modern screens now test 100+ cell lines with thousands of drugs or CRISPR perturbations.
- **European startup ecosystem**: Germany excels at early-stage startups but lags in scaling due to conservative VC culture; Munich is a growing hub for deep-tech bio startups, though many pivot to drug development for clearer monetization.
- **Helmholtz Munich**: A research organization with ~500–600 people in the Computational Health Center, focused on multi-scale health AI (DNA to patient cohorts) and translational collaborations with clinics.

***
## Actionable Takeaways
- **Prioritize closed-loop systems**: Invest in tools like Lab Compass that turn predictive models into experiment designers, but ensure tight collaboration with wet-lab teams to validate and iterate.
- **Benchmark rigorously**: Always compare against linear baselines and simple heuristics (e.g., mean prediction) in perturbation tasks; avoid metric hacking by using diverse, domain-relevant evaluations.
- **Leverage unique data**: For commercialization, pair virtual cell models with proprietary or hard-to-replicate data (e.g., organoid perturbations, spatial omics) to create moats for pharma partnerships.
- **Adopt the Y model**: Structure teams or training programs to force integration between computational and domain experts, accelerating the translation of biological problems into ML solutions.
- **Watch for scaling inflections**: As biological data grows (e.g., 300M+ cells), expect flexible, data-driven models to outperform heavily biased ones—plan infrastructure and talent accordingly.

***
## People, Companies, Tools, And Links Mentioned
- **People**: Fabian Theis, RJ Haneke (CTO of Miraomics), Brandon Anderson (Atomic AI), Bo Wang, John Platt, Lila (likely [Lila Icarus](https://www.lila.ai/))
- **Companies/Institutions**: Helmholtz Munich, Technical University of Munich, University of Cambridge, ParseBio, BioHub, DOE, NIH, Meta, Google, NVIDIA, AstraZeneca, ARC Institute, MIT, NeurIPS, Open Problems, Genentech
- **Tools/Platforms**: Scanpy, AnnData, SCVerse, SEGen, scGen, CellTypist, SC-TAP, Self-Flow, Flow Matching, AlphaFold, FinGene, European Health Data Space, Cancer Organoid Perturbation Atlas
- **Links**: [Latent Space Podcast - Controlling Biology - Fabian Theis](https://lspace.beehiiv.com/podcast/s/latent_space_the_ai_engineer_podcast/controlling_biology_-_fabian_theis_helmholtz_munich_1)

***
## Reading Priority

Medium – A deep dive into the state of virtual cell modeling, with concrete examples of scaling, benchmarking, and commercialization challenges, though some predictions (e.g., RL-driven labs) remain speculative.

***

# Tokenization, Agentic Trading, Harmonic: Robinhood's Mission to Expand Ownership with CEO Vlad Tenev

- **Published:** 2026-11-05
- **Podcast:** [No Priors](https://traffic.megaphone.fm/PDP1158596730.mp3)
- **Speaker:** Vlad Tenev, CEO and co-founder of Robinhood, and co-founder of Harmonic

## One-Sentence Takeaway
Robinhood is expanding ownership—of public and private assets, trading strategies, and even mathematical discovery—by democratizing access to financial and AI tools, arguing that broad-based ownership stabilizes society and accelerates innovation.

## Short Summary
Vlad Tenev frames Robinhood’s mission as enabling ownership across asset classes, from tokenized stocks and private companies to AI-driven trading agents, to counter wealth concentration and foster societal stability. He highlights early traction in agentic trading (150,000+ accounts, 30M daily tool calls) and tokenization via Robinhood Chain, which extends U.S. market access globally. Tenev also advocates for decentralized mathematical discovery through Harmonic, his AI math startup, and pushes for regulatory changes to let retail investors access private markets earlier.

The conversation explores how agentic trading could scale retail participation, the infrastructure readiness for high-frequency trading (HFT) loads, and policy shifts like the SEC’s knowledge-based accreditation exam to broaden private investment access.

## Main Ideas
- **Ownership as stability**: Broad asset ownership aligns individual and societal incentives, reducing fragility; Robinhood’s products (e.g., tokenization, Trump accounts) aim to extend this globally and to earlier stages (private companies, birth).
- **Agentic trading adoption**: Robinhood’s agentic trading (150,000+ accounts, 30M daily tool calls) demonstrates product-market fit, with a sandboxed MCP harness and app store (e.g., satellite data integrations) to democratize quant strategies.
- **Tokenization and Robinhood Chain**: Fully DeFi-enabled stock tokens and a high-growth blockchain (Robinhood Chain) let developers compose financial primitives (e.g., stock-meme NFTs) and give global users low-cost U.S. market access, even in regions with weak financial infrastructure.
- **Decentralized AI for math**: Harmonic’s Aristotle model (gold medal, International Math Olympiad) shows AI can solve unsolved problems, but Tenev argues centralized AI labs risk backlash; decentralized tools in users’ hands will drive acceptance and discovery.
- **Private market access**: Robinhood Ventures (publicly traded funds) and tokenization aim to let retail investors access private companies earlier, countering wealth concentration in VC/institutionals; accredited investor rules need updating (e.g., knowledge-based exams).

## Questions And Answers
- **Q: Will people let agents trade for them?**
  A: Yes—Robinhood reports over 150,000 agentic trading accounts and 30M daily tool calls, indicating strong early adoption. The product sandboxes strategies in separate accounts with optional trade approvals.

- **Q: How can financial infrastructure handle mass agentic trading?**
  A: Existing HFT-optimized exchanges and market makers (e.g., Citadel, Jane Street) can likely scale, but Robinhood is monitoring load as agentic trading grows from a small percentage of activity.

- **Q: How does tokenization extend ownership?**
  A: Tokenized stocks (backed by custodied assets) trade on-chain like software, enabling fractional, global, 24/7 access. Robinhood Chain’s developer activity (e.g., stock-meme pairs) suggests composable financial primitives are emerging.

- **Q: Why push for retail access to private markets?**
  A: Private companies now stay private longer, concentrating gains. Robinhood Ventures (publicly traded funds) and tokenization aim to let retail invest earlier, with policy changes (e.g., SEC’s knowledge-based accreditation) reducing friction.

## Notable Details
- Robinhood Chain reports rapid growth in developer activity and is positioned as a leading chain for real-world assets and AI agents.
- Agentic trading accounts are segregated from main balances, with optional trade approvals; the harness includes skills (e.g., portfolio rebalancing) and app store integrations (e.g., satellite data).
- Trump accounts: $1,000 S&P 500 ETF seed for newborns (2025–2028), with additional donations (e.g., Dell Foundation’s $6B for low-income zip codes, SpaceX shares from Gwynne Shotwell).
- Harmonic’s Aristotle model won a gold medal at the International Math Olympiad and was used to solve Erdős problems; Tenev advocates for decentralized math discovery to avoid centralized AI backlash.
- Robinhood Ventures Fund 1 (late-stage privates, e.g., OpenAI, 11Labs) and Fund 2 (seed/Series A via YC partnership) are publicly traded, offering retail exposure to private markets.
- Tenev cites 2000% annualized inflation in 1990s Bulgaria as a formative experience shaping his views on financial systems and ownership.

## Actionable Takeaways
- Watch Robinhood Chain’s developer ecosystem for novel compositions of tokenized assets (e.g., options, derivatives) and agentic trading tools.
- Monitor adoption of agentic trading (e.g., tool call growth, strategy complexity) as a signal for retail quant participation.
- Track policy shifts (e.g., SEC’s knowledge-based accreditation exam) that could broaden retail access to private markets.
- Consider the implications of decentralized AI math tools (e.g., Harmonic) for open scientific discovery and public acceptance of AI-driven results.
- Explore KPI contracts and prediction markets as precision hedging tools for monetizing domain-specific knowledge.

## People, Companies, Tools, And Links Mentioned
- [Robinhood](https://robinhood.com)
- [Harmonic](https://harmonic.ai)
- [No Priors podcast](https://no-priors.com)
- Trump accounts
- Robinhood Chain
- Robinhood Ventures (Fund 1, Fund 2)
- Y Combinator (YC)
- OpenAI
- 11Labs
- Crusoe
- SpaceX
- Dell Foundation
- Michael Dell
- Susan Dell
- Gwynne Shotwell
- Brad Gerstner
- SEC
- FINRA
- International Math Olympiad
- Aristotle (Harmonic’s model)
- Erdős problems
- Citadel
- Jane Street
- Jump Trading
- Terence Tao

## Reading Priority

Medium – A concrete, wide-ranging discussion on democratizing ownership and AI tools, with early traction metrics and policy insights, though some initiatives (e.g., Trump accounts) are still nascent.

***

# Ep 97: Jev Creator on Decision Models, Benchmark Fatigue & Why the Labs Missed It

- **Published:** 2026-11-05
- **Podcast:** [Unsupervised Learning](https://unsupervised-learning.simplecast.com/episodes/ep-97-jev-creator-on-decision-models-benchmark-fatigue-why-the-labs-missed-it-lw9nHzNX)

## One-Sentence Takeaway
Reliability, not raw intelligence or novel model shapes, is the bottleneck for AI automation, and most LLM calls should serve machines—not humans—with structured, decision-focused outputs.

## Short Summary
Diogo Almeida argues that AI has long been "smart enough" to automate routine work but fails due to misaligned outputs (text for humans vs. structured data for machines) and a lack of focus on reliability. He built Jev as a "System 1" model to return machine-native decisions, not chat, and critiques the industry’s overemphasis on benchmarks, KV cache constraints in coding agents, and the tyranny of human-pleasing outputs. He predicts coding agents deliver 20–40% speedups but warns that jaggedness and side effects limit broader automation.

The conversation also covers the need for developer pushback on model providers, the underrated role of financial engineering in labs, and the risk of overpromising on novel model shapes without utility.

## Main Ideas
- **Machine-native outputs**: Most LLM calls in production should target machines, not humans, yet today’s models optimize for human-pleasing text; Jev focuses on structured, reliable decisions for software.
- **Reliability over shapes**: Novel model shapes (e.g., decision models) are cheap to prototype, but reliability and real-world utility are the hard, undervalued problems; benchmarks often mislead by ignoring jaggedness.
- **KV cache tyranny**: Coding agents are constrained by the KV cache’s append-only, stateful nature, which limits routing, sub-agents, and dynamic context management; alternative architectures could unlock new patterns (e.g., shared context, semantic compaction).
- **Coding agent productivity**: According to the guest, coding agents deliver roughly 20–40% speedups, but gains vary by use case, skill level, and ability to isolate side effects (e.g., via Git).
- **Benchmark fatigue**: Developers are rapidly losing trust in benchmarks due to overpromising; Jev’s launch accelerated this fatigue by exposing the gap between benchmark performance and real-world reliability.

## Questions And Answers
**Q: Why did Jev launch despite industry pushback?**
A: The team prioritized shipping a product they were proud of to co-evolve use cases with developers, rather than waiting for a "perfect" moment or optimizing for attention.

**Q: What’s the biggest limitation of current coding agents?**
A: The KV cache forces stateful, append-only interactions that hinder routing, sub-agents, and dynamic context management, limiting architectural flexibility.

**Q: How should developers engage with model providers?**
A: Push harder on jaggedness and reliability; demand provider-agnostic, SQL-like reliability and collaborate on uncovering capabilities rather than passively accepting model updates.

**Q: What’s underrated about AI labs?**
A: Financial engineering (e.g., compute deals) is their greatest strength, often overshadowing model or product innovations.

## Notable Details
- Jev’s name references **Jevons Paradox**: the idea that cheaper, better AI will increase demand and usage, expanding the total market.
- **Dependent typing for AI**: Diogo proposes using Jev-like models to verify natural-language constraints in code (e.g., "this function returns an int > 0"), enabling higher-level composability.
- **Multimodality trade-offs**: Adding modalities (e.g., images) degrades reliability; text tasks should be automated before harder multimodal tasks.
- **Productivity caveats**: Coding agent gains (20–40%) come with long-term risks like skill degradation and technical debt; side effects are the primary downside of powerful tools.
- **Benchmark skepticism**: Jev’s launch led to rapid "benchmark fatigue," as users realized benchmarks often fail to capture real-world utility.

## Actionable Takeaways
- Audit LLM use cases: Identify where text outputs are meant for machines and replace them with structured, decision-focused calls.
- Pressure providers on jaggedness: Demand transparency about model weaknesses and provider-agnostic reliability, not just benchmark scores.
- Experiment with non-KV architectures: Explore coding agent designs that decouple from the KV cache (e.g., shared context, semantic compaction) for advanced patterns.
- Prioritize reliability over novelty: Focus on real-world utility when evaluating new model shapes or tools, not just hype or benchmarks.
- Isolate side effects: For coding agents, use Git, human-in-the-loop checks, and reversible workflows to mitigate risks.

## People, Companies, Tools, And Links Mentioned
- [Jev](https://jev.ai)
- [TypeSafe AI](https://typesafe.ai)
- OpenAI
- Anthropic
- InstructGPT paper
- Langchain
- RLVR
- GPQA benchmark
- KV cache
- Jevons Paradox
- [Unsupervised Learning podcast](https://unsupervised-learning.simplecast.com)

## Reading Priority

Medium – A candid, technical critique of AI’s reliability gaps and architectural constraints, with actionable insights for developers and product builders.

***

# A Model For Everyone: How Ronak From Trajectory Is Building Products For Continual Learning

- **Published:** 2026-11-05
- **Podcast:** [Training Data](https://pscrb.fm/rss/p/traffic.megaphone.fm/CPUAI8366427179.mp3)
- **Speaker:** Ronak Malde, Co-founder, Trajectory

## One-Sentence Takeaway
Continual learning—where models update from real-world interactions rather than offline batches—is the next AI paradigm, and Trajectory is democratizing the tools to make it practical for companies to train, evaluate, and deploy customized models in a closed loop.

## Short Summary
Today’s AI agents operate in "pseudo continual learning": they’re intelligent but updated in static, offline batches, like consulting a paper map mid-trip. True continual learning, argues Ronak Malde (Trajectory co-founder), mirrors human learning—online, adaptive, and driven by real-world feedback. Trajectory’s platform aims to close this loop by letting companies train models on their own data with minimal friction, leveraging research like group-size-one GRPO (learning from single rollouts) and a meta-grader that boosts data efficiency by 100x.

The conversation highlights a shift from research-lab-only capabilities to productized workflows, where companies like Harvey and Rogo use Trajectory to train domain-specific models (e.g., Harvey’s legal model, 6x cheaper than frontier, with 4x+ gains on its own benchmark). The long-term vision: product builders become "gardeners," setting constraints for self-improving systems that grow autonomously.

## Main Ideas
- **Pseudo vs. true continual learning**: Current agents are like static maps—useful but rigid—while true continual learning (e.g., Google Maps) updates dynamically from real-world interactions. The gap is the inability to translate real-world feedback into model improvements at scale.
- **Democratizing model training**: Training custom models once required massive research teams, months of work, and hundreds of millions in compute (e.g., Windsurf’s SWE-1). Trajectory’s platform compresses this into a one-click workflow for trace-based training, evaluation, and deployment.
- **Research bets for practicality**: Trajectory’s group-size-one GRPO variant eliminates the need for simulated environments by learning from single real-world rollouts (vs. 16 replays per task). A meta-grader reduces labeling effort by 100x, inferring rewards from a small labeled subset to a larger dataset.
- **Continual learning vs. recursive self-improvement (RSI)**: Continual learning keeps humans in the loop, aligning improvements with user objectives, while RSI risks misalignment by optimizing models in isolation. The former prioritizes real-world task performance over autonomous self-improvement.
- **Product builders as gardeners**: As systems self-improve, the role of product teams shifts to setting "trellises"—constraints and objectives—that guide autonomous growth, blending model and harness optimization.

## Questions And Answers
- **What’s the core difference between continual learning and RSI?**
  Continual learning updates models from real-world human interactions and tasks, ensuring alignment with user goals. RSI focuses on models improving themselves in isolation, risking misalignment with human intent.

- **How does Trajectory’s platform simplify training?**
  It unifies training, evaluation, and deployment into a one-click interface, letting companies upload agent traces, define "what good looks like," and deploy updated models without managing infrastructure or research overhead.

- **What’s the significance of group-size-one GRPO?**
  Traditional GRPO requires replaying the same task 16+ times in a simulated environment. Trajectory’s variant learns from single real-world rollouts, removing the need for environment simulation and reducing infrastructure complexity.

- **Why is Harvey’s use case notable?**
  Harvey trained a legal model on Trajectory’s platform that was 6x cheaper than frontier models and improved an open-source baseline by 4x (from 4% to 18%) on Harvey’s own legal benchmark, demonstrating domain-specific gains from customized training.

## Notable Details
- Harvey’s model: 6x cheaper than frontier, 4% → 18% accuracy on Harvey’s legal benchmark (Harvey-reported).
- Meta-grader: Reduces labeling effort by 100x by inferring rewards from a small labeled subset (100 traces) to a larger dataset (10,000 traces) (Trajectory-reported).
- Group-size-one GRPO: Learns from single real-world rollouts instead of requiring 16 replays per task in a simulated environment (Trajectory research).
- Trajectory’s platform: One-click train/eval/deploy workflow for companies with existing agent harnesses (e.g., Harvey, Rogo, NVIDIA).
- Rogo’s focus: "Intelligence density"—concise, efficient agents that autonomously perform tasks with minimal verbosity.
- Historical analogy: Current AI adoption (1% of enterprise) mirrors pre-industrial specialization; Trajectory aims to expand this to 99% by enabling domain-specific customization.

## Actionable Takeaways
- **For AI-native companies**: Audit your agent traces and harnesses—if you’re logging interactions and feedback, you’re already partway to continual learning. Tools like Langchain or Braintrust can help structure traces for replayability.
- **For product teams**: Start designing for "trellises"—explicit constraints and objectives that guide autonomous model/harness improvements, shifting from direct control to gardening.
- **For enterprises**: Explore hybrid models—use frontier models for 10% of high-complexity tasks and customized, cheaper models (trained on domain data) for the remaining 90% to improve margins.
- **Watch for**: Advances in curiosity-driven learning (e.g., modeling transition functions in RL) and alignment mechanisms that keep humans in the loop for continual learning.

## People, Companies, Tools, And Links Mentioned
- [Trajectory](https://trajectory.ai)
- Harvey
- Rogo
- NVIDIA
- Windsurf
- SWE-1 (Windsurf’s model)
- Cursor Composer
- DeepMind
- Gemini (Google)
- Apple Vision Pro
- Langchain
- Braintrust
- Raindrop
- Modal
- Thinking Machines
- Rich Sutton
- David Silver
- Adam Smith, *Wealth of Nations*
- GRPO (Group Relative Policy Optimization)
- Pat Grady, Sequoia Capital
- Lauren Reeder, Sequoia Capital

## Reading Priority

Medium – A clear, concrete vision for continual learning as the next AI paradigm, with actionable product insights and early customer validations, though some claims are vendor-reported.

***

# ⚡ Behind Latent Space: A Rare Look Inside the Pod | AIEi Shanghai

- **Published:** 2026-11-04
- **Podcast:** [Latent Space](https://www.youtube.com/watch?v=QmDLDy3ZSNE)

## One-Sentence Takeaway
The rise of AI engineering as a discipline—and the global, grassroots communities forming around it—reflects a shift from credential-driven gatekeeping to practical, learn-in-public skill-building that empowers engineers to harness AI in real-world applications.

## Short Summary
The conversation centers on the origin and growth of the AI Engineer (AIE) movement, its global expansion (including the first AIE conference in Shanghai), and the broader cultural and technical shifts enabling it. The speaker argues that AI engineering—distinct from prestige-heavy ML research—focuses on practical harness-building, customization, and integration of AI into software workflows, often by self-taught practitioners. The discussion also critiques mid-tier SaaS vulnerability to AI-driven cloning, highlights the importance of developer-focused communities over "talking head" conferences, and explores the role of taste, GTM, and showmanship in technical product adoption.

The speaker’s personal journey—from finance to tech, learning in public, and founding Latent Space and AIE—illustrates how open knowledge-sharing and community-building can professionalize emerging roles faster than traditional credentialing.

## Main Ideas
- **AI Engineering as a discipline**: A distinct role focused on building "harnesses" (integrations, workflows, and tools) around AI models, requiring strong software engineering skills rather than advanced ML research credentials. This role emerged from the need to bridge the gap between non-technical users and the capabilities of AI systems.
- **Learn-in-public as a career strategy**: Public learning and sharing (e.g., blogging, open-sourcing) accelerates skill acquisition and reputation-building, especially in fast-moving fields like AI. This approach contrasts with zero-sum fields (e.g., finance), where knowledge hoarding is the norm.
- **Community-driven professionalization**: Conferences like AIE and grassroots communities (e.g., China’s Way2AI) help define and legitimize new roles by providing platforms for engineers to share war stories, tools, and best practices—focusing on practical, actionable insights over high-level speculation.
- **Mid-tier SaaS vulnerability**: AI-driven automation (e.g., coding agents) enables businesses to clone or customize proprietary software rapidly, threatening mid-tier SaaS providers that lack network effects, specialized data, or vertical dominance. Businesses can now build bespoke tools internally at lower cost and higher flexibility.
- **Global AI ecosystems**: China’s AI community is highly active in open-source models, robotics, and startups, but faces unique challenges (e.g., US export controls, cultural differences in credentialism). Localized AIE conferences (e.g., Shanghai) help bridge East-West knowledge gaps despite geopolitical barriers.

## Questions And Answers
- **Q: How has the role of AI engineer evolved since its inception?**
  A: The core role (building harnesses, integrating AI into workflows) remains stable, but sub-disciplines have emerged (e.g., coding agents, evals, multimodal, memory systems). The title "AI engineer" now sits alongside roles like AI architect (company-wide strategy) and AI designer (UX-focused).

- **Q: Why do Chinese founders struggle with global expansion?**
  A: Many excel at technical execution but lack go-to-market (GTM) expertise, particularly in understanding Western markets, messaging, and customer needs. Early GTM involvement (e.g., defining target segments, crafting narratives) is critical but often overlooked.

- **Q: What makes Diogo (Jeff/TypeSafe) stand out in AI?**
  A: His non-traditional background (no Stanford PhD), credibility from OpenAI, and focus on "System 1" models (small, fast, embedded in code paths) challenge the "bigger models are better" orthodoxy. His showmanship (e.g., Doom demo) and clear communication amplify his technical contributions.

- **Q: How can SMBs leverage AI to replace SaaS tools?**
  A: Businesses can now clone or customize proprietary software using open-source alternatives and coding agents, reducing costs and increasing flexibility. For example, a $40K SaaS tool was replicated in a week for $10K, with customizations tailored to internal workflows.

## Notable Details
- AIE World Fair (flagship conference) attracted **7,000+ in-person attendees** and **1.5M online viewers**, with 30 tracks covering AI engineering sub-disciplines. All talks and workshops are published openly, and transcripts are available as a dataset for LLM training.
- The **Kill My SaaS** competition demonstrated that mid-tier SaaS tools (e.g., Calendly, DocuSign) can be cloned and customized rapidly using coding agents, with **69 submissions** for a single tool and ~5 deemed production-ready.
- China’s **Way2AI community** (1M+ users) emerged alongside Stable Diffusion, focusing on collaborative learning and open-source contributions (e.g., ComfyUI).
- The speaker has **replaced multiple SaaS tools** (e.g., Calendly, Google Drive, GitHub, Slack, Dropbox) with self-hosted, open-source alternatives integrated into custom workflows.
- **TypeSafe’s System 1 models** prioritize reliability and integration into code paths over raw scale, enabling smarter software at every step rather than relying on a single "smart" chatbot interface.

## Actionable Takeaways
- **For engineers**: Adopt a learn-in-public mindset to build reputation and skills in AI engineering. Focus on practical harness-building (e.g., RAG, agents, evals) rather than waiting for formal credentials.
- **For SMBs**: Audit SaaS spending and experiment with cloning/customizing tools using open-source alternatives and coding agents. Prioritize tools that directly impact productivity (e.g., internal workflows).
- **For startups**: Involve GTM early in product development to ensure market fit. For technical founders, partner with GTM experts to bridge gaps in messaging and customer understanding.
- **For conference organizers**: Emulate AIE’s model of engineer-to-engineer knowledge-sharing, with a focus on actionable, technical content and community-building.
- **For SaaS providers**: Pivot toward vertical specialization (e.g., agent builders, data vendors) or network effects to defend against AI-driven commoditization.

## People, Companies, Tools, And Links Mentioned
- **People**: Diogo (TypeSafe/Jeff), Meng Xiao (Latent Space translator), Han Hua, Lei Du, Meng Ying, Comfy Anonymous, Joe and Alex (AI Tinkerers), Iman Mostak (Stability AI), Sean (interviewer).
- **Companies/Projects**: [Latent Space](https://latent.space), [AI Engineer (AIE)](https://www.aiengineer.io), [Cognition](https://www.cognition.ai), Fireworks, Modal, Superbase, Mistral, Way2AI, Unitree, OpenClaw, Maness, 99designs, DocuSign, Calendly, TypeSafe, Jeff.
- **Tools/Concepts**: Stable Diffusion, ComfyUI, System 1 models, coding agents (Codex, Cloud, Devin), MCP (Model Context Protocol), RAG, evals, harness engineering.
- **Links**: [AIE Shanghai](https://www.youtube.com/watch?v=QmDLDy3ZSNE), [ai.engineer.data](https://ai.engineer.data).

## Reading Priority

Medium – A candid, experience-driven look at the rise of AI engineering, the fragility of mid-tier SaaS, and the power of grassroots communities in shaping new technical disciplines, with actionable insights for engineers and business owners.

***

# The Inside Story of the 50 Who Built Modern AI With Kevin Roose

- **Published:** 2026-11-04
- **Podcast:** [AI & I by Every](https://episode.flightcast.com/01M6KJSKA8EAFY499K1BVMN3KK.mp3)
- **Speaker:** Kevin Roose

## One-Sentence Takeaway
Modern AI’s rapid development reflects deliberate choices by a small group of researchers and leaders, whose decisions—often driven by competition and urgency—now demand societal oversight to mitigate existential risks.

## Short Summary
Kevin Roose’s *The AGI Chronicles* traces the behind-the-scenes decisions that shaped modern AI, based on interviews with 150 insiders. He argues that while AI poses real risks, proactive measures like mandatory safety testing and industry coordination can help navigate its challenges without waiting for a crisis to force regulation.

The book also explores the cultural and psychological dynamics within AI labs, including the influence of early memos like Dario Amodei’s "Big Blob of Compute Hypothesis," which redirected research toward scaling general-purpose models.

## Main Ideas
- The AI race accelerated due to a shift from narrow, task-specific models to scaling general-purpose systems, as articulated in Dario Amodei’s 2017 memo, which argued for assembling "big blobs of compute" to tackle broad problems like next-word prediction.
- Roose advocates for mandatory safety testing of AI models before public release, drawing a parallel to pharmaceutical regulations, and suggests industry-wide coordination to slow frontier development and allow safety research to catch up.
- The book captures the tension between competitive urgency and risk mitigation, with key figures like Dario Amodei, Demis Hassabis, and Sam Altman now acknowledging the need to decelerate progress to address safety gaps.
- Roose used AI extensively in his research and editing process, including a "council of Claudes" to fact-check drafts and tools like NotebookLM to organize sprawling research, but insists the writing itself remained human-driven.

## Questions And Answers
**Q: How did Roose convince 150 secretive AI insiders to share untold stories?**
A: He offered anonymity (background sourcing), demonstrated deep familiarity with their work, and leveraged the small, interconnected nature of the AI community, where participation snowballed as others saw peers contributing.

**Q: What was the "Big Blob of Compute Hypothesis"?**
A: Dario Amodei’s 2017 internal memo at OpenAI argued that scaling unstructured computational capacity toward general tasks (e.g., next-word prediction) would yield intelligence more effectively than narrow, custom-built systems.

**Q: How does Roose use AI in his workflow?**
A: He employs agents for fact-checking, research organization (e.g., NotebookLM), and administrative tasks, but reserves creative and editorial judgment—like coaching and motivation—for human collaboration.

## Notable Details
- Roose’s mother’s book on atomic bomb survivors (*hibakusha*) subconsciously influenced his urgency to document firsthand accounts of AI’s development before records disappeared.
- The phrase *"feel the AGI"* originated with Ilya Sutskever at OpenAI, who would urge colleagues to recognize the transformative potential of the technology they were building.
- Roose’s 2023 interaction with Bing Sydney (Microsoft’s chatbot) marked his personal inflection point in recognizing AI’s social and technological power.
- *The Making of the Atomic Bomb* by Richard Rhodes and Arthur C. Clarke’s *Profiles of the Future* were formative for AI leaders like Dario Amodei and Ilya Sutskever, shaping their views on innovation and risk.

## Actionable Takeaways
- Distinguish between "weightlifting" (tasks where struggle is the point, like parenting or creative thinking) and "forklifting" (repetitive or administrative tasks) when deciding where to apply AI.
- For high-stakes fields like AI, push for preemptive industry standards (e.g., safety testing) rather than waiting for a crisis to trigger regulation.
- Use AI tools to augment research and editing, but preserve human judgment for narrative structure, motivation, and ethical considerations.
- Study historical parallels (e.g., the Manhattan Project) to understand the cultural and strategic dynamics of rapid technological development.

## People, Companies, Tools, And Links Mentioned
- [Kevin Roose](https://x.com/kevinroose)
- [*The AGI Chronicles*](https://theagichronicles.com/)
- [*Machine Gods* podcast](https://www.npr.org/podcasts/g-s1-143588/machine-gods)
- ["The Big Blob of Compute Hypothesis" excerpt](https://kevinroose.substack.com/p/the-essay-that-started-the-ai-race)
- *Profiles of the Future* by Arthur C. Clarke
- *The Making of the Atomic Bomb* by Richard Rhodes
- [NotebookLM](https://notebook.google/)
- Dario Amodei (Anthropic)
- Demis Hassabis (DeepMind)
- Sam Altman (OpenAI)
- Ilya Sutskever (former OpenAI)
- Casey Newton (co-host, *Machine Gods*)
- Walter Isaacson

## Reading Priority

Medium – A well-sourced, narrative-driven account of AI’s development with practical insights on safety, industry dynamics, and the role of journalism in demystifying technology.

***

# ⚡️ The 2026 Software Factory Standard — Zach Lloyd, Warp.dev

- **Published:** 2026-11-03
- **Podcast:** [Latent Space](https://www.youtube.com/watch?v=LL0YmIyBKSU)
- **Speaker:** Zach Lloyd, Founder/CEO, Warp.dev

## One-Sentence Takeaway
A software factory is a declarative, measurable, and self-improving agentic system for building software at scale, turning ad-hoc coding agent use into an engineered, closed-loop process.

## Short Summary
Zach Lloyd argues that a software factory should be a concrete, code-defined system with clear workflows, roles, and observability—not a vague collection of automations. By centralizing agent traces, artifacts, and interactions, teams can measure throughput, cost, and quality, then iteratively tune their setup (models, harnesses, skills) for efficiency. Warp’s approach emphasizes declarative factory definitions, benchmarking against real tasks, and self-improving loops where agents propose and test factory upgrades.

The conversation also clarifies that factories make sense for teams of ~5–10+ engineers, not small groups better served by off-the-shelf coding agent subscriptions. Criticisms include the complexity of bespoke infrastructure and the economic reality that API-based agent development struggles to compete with subsidized consumer plans.

## Main Ideas
- A software factory is a **code-defined, measurable system** operating on a product surface (e.g., a repo), with explicit workflows (triage, spec, implementation), skills, and tool integrations (MCPs), enabling closed-loop optimization.
- **Centralized observability** of agent traces, artifacts, and interactions unlocks metrics (cost/PR, throughput, automation rate) and **online evals** (LLM-as-judge) to identify failure modes (e.g., redundant tests) and guide improvements.
- **Benchmarking** replays real tasks against different models/harnesses (e.g., GPT-56 Sol vs. GLM-53 Flash) to optimize cost-correctness tradeoffs, enabling **model routing strategies** tailored to a team’s workflows.
- **Self-improving factories** use agents to analyze failure patterns (e.g., triage needing sub-agents) and propose code changes to the factory definition, with the potential to replay historical runs to validate improvements.
- **Declarative factories as code** enable versioning, branching, and agent-driven upgrades, forming the foundation for a new discipline: **factory engineering** (distinct from product engineering).

## Questions And Answers
**Q: What’s the minimal viable scale for a software factory?**
A: Teams of ~5–10+ engineers see value; smaller teams are better off with consumer coding agent subscriptions (e.g., Cursor, Codex) due to cost and complexity.

**Q: How do you handle model/harness selection?**
A: Benchmark real tasks against a matrix of models (e.g., OpenAI, Anthropic, Google) and harnesses (Warp, Cloud Code, Pi) to optimize for cost, correctness, and workflow fit, then route dynamically.

**Q: What’s the biggest pushback against factories?**
A: Companies with highly bespoke infrastructure (e.g., Uber, Ramp) or those relying on subsidized consumer plans may find factories overkill or uneconomical.

## Notable Details
- Warp reduced its **cost per PR from ~$80 to ~$15–20** by tuning model usage (e.g., avoiding Opus for triage), agent orchestration, and redundant work, while increasing **PR throughput by 40%** without higher revert rates.
- **Factory stack layers**: declarative code (foundation), data collection (agent traces/artifacts), access points (Slack, Linear, GitHub), compute (pluggable sandboxes like Namespace, Daytona), inference (open provider support), and orchestrator (workflow execution).
- **Subsidized consumer plans** (e.g., $200/month for 8,000 API calls) can be 5–50x cheaper than pay-as-you-go APIs, but are unscalable and may violate terms of service.
- **Self-improvement example**: Warp’s agents identified 54 triage failures where spawning sub-agents would help, then generated PRs to update the factory definition.

## Actionable Takeaways
- **Start small**: Define one factory per product surface with a YAML workflow, then expand observability and evals.
- **Benchmark real tasks**: Replay historical agent runs against new models/harnesses to find cost-correctness sweet spots.
- **Centralize traces**: Aggregate agent conversations and artifacts to diagnose failures and tune systems (not just individual setups).
- **Separate factory engineering from product engineering**: Invest in a platform team to own factory optimization, distinct from feature development.
- **Watch for economic shifts**: Monitor the viability of API-based agent development vs. subsidized consumer tools as team size grows.

## People, Companies, Tools, And Links Mentioned
- [Warp.dev](https://warp.dev)
- Zach Lloyd on Twitter
- Namespace (agent sandbox)
- Daytona, Modal, E2B (sandbox providers)
- Cursor, Cloud Code, Codex, Pi (coding agents/harnesses)
- AIE Code (event)
- Uber, Ramp (examples of bespoke infrastructure)
- SuiBench, TerminalBench (benchmark suites)

## Reading Priority

Medium – A concrete, actionable framework for scaling coding agents beyond ad-hoc use, with strong emphasis on measurement and iteration.

***

# Ep 96: Nebius CTO on Racing the Hyperscalers Before AWS Wakes Up

- **Published:** 2026-11-02
- **Podcast:** [Unsupervised Learning](https://unsupervised-learning.simplecast.com/episodes/ep-96-nebius-cto-on-racing-the-hyperscalers-before-aws-wakes-up-AZ_eCjjr)
- **Speaker:** Danila Shtan, CTO, Nebius

## One-Sentence Takeaway
Independent AI clouds like Nebius can outmaneuver hyperscalers by specializing in software-first, high-performance AI workloads while hyperscalers are constrained by legacy infrastructure and internal demand for scarce GPUs.

## Short Summary
Nebius positions itself as a software-first AI cloud, optimizing for both large-scale clusters and self-service users, with a bet that demand for AI compute will explode 10-100x in the next three years. Hyperscalers have been slow to dominate AI cloud due to chip scarcity, internal consumption priorities, and the need to retrofit infrastructure built for non-AI workloads.

The conversation highlights gaps in inference optimization, the prevalence of modified (non-vanilla) models among customers, and the operational challenges of integrating new NVIDIA hardware. Nebius also emphasizes the growing importance of storage throughput, compliance for enterprise customers, and the long-term viability of niche AI infrastructure providers.

## Main Ideas
- **Hyperscaler constraints**: AWS, Google, and Microsoft struggle to prioritize AI cloud due to limited GPU allocations, internal demand for compute, and the cost of retrofitting infrastructure designed for traditional workloads. Chip scarcity has prevented them from capturing the market as aggressively as expected.
- **Software-first differentiation**: Nebius focuses on building a holistic, software-defined cloud platform that can serve both massive clusters and small-scale users, rather than relying on bare-metal or third-party patchworks.
- **Inference optimization gaps**: Running open-source models efficiently remains unsolved; 95% of Nebius customers use modified or fine-tuned models, and there is significant untapped potential in kernel optimizations, model compression, and speculative decoding.
- **Storage as a bottleneck**: AI workloads now demand extreme storage throughput (e.g., 700 GB/s from a single shared file system), a requirement that was underappreciated just two years ago.
- **Prefill/decode disaggregation**: While widely discussed, it remains more talk than practice due to operational complexity and the presence of lower-hanging optimizations (e.g., model pruning, traffic pattern tuning).

## Questions And Answers
**Why haven’t hyperscalers dominated AI cloud yet?**
Hyperscalers face chip scarcity, internal competition for GPU allocations, and the need to justify massive infrastructure investments for a market that, while growing, is still a small fraction of their overall revenue.

**What differentiates Nebius from other AI clouds?**
Nebius prioritizes a software-first approach, enabling it to serve both large-scale and retail customers on the same platform, with deep optimizations for AI workloads (e.g., storage throughput, model inference).

**What are the biggest bottlenecks in AI infrastructure today?**
The primary bottleneck is execution: managing supply chain constraints (GPUs, CPUs, NVMe, transformers, etc.), sourcing components, and flexibly reallocating resources across facilities. Project management and operational agility are critical.

**How do customer needs vary in AI cloud?**
Startups and new labs prioritize GPU performance, storage, and availability, often signing billion-dollar contracts with minimal concern for location or compliance. Enterprises, however, demand compliance, security audits, and predictable outcomes, even at smaller contract sizes.

## Notable Details
- Nebius reports that **95% of its customers run modified or fine-tuned models**, not vanilla open-source versions, due to domain-specific needs.
- Some customers require **700 GB/s throughput from a single shared file system** connected to thousands of servers or 8,000 GPUs.
- Nebius acquired a company in mid-2025 to bolster its model optimization capabilities, including compression and speculative decoding.
- The company operates with **no internal limits on AI token usage**, but enforces accountability: outputs generated by agents are treated as the responsibility of the human user.
- NVIDIA’s rapid iteration on hardware (e.g., GB200 racks vs. server-based architectures) forces cloud providers to constantly adapt their software and infrastructure.
- Nebius expects AI demand to grow **10-100x in the next three years**, driven by broader enterprise adoption and specialized agents.

## Actionable Takeaways
- Watch for **inference optimization breakthroughs** (e.g., model pruning, kernel tuning) as a key differentiator for AI clouds, given that vanilla models are rarely used in production.
- Assume **storage throughput will remain a critical constraint**—design systems for extreme bandwidth (hundreds of GB/s) to shared file systems.
- Monitor **hyperscaler investments in AI-specific infrastructure**; as chip supply stabilizes, they may aggressively enter the market with retrofitted or new buildouts.
- For enterprise AI adoption, **compliance and predictability** will outweigh raw performance for many customers.
- Consider **disaggregated prefill/decode** as a future optimization, but focus first on lower-hanging fruits like model compression and traffic-specific tuning.

## People, Companies, Tools, And Links Mentioned
- [Nebius](https://nebius.com)
- [NVIDIA](https://www.nvidia.com)
- [AWS](https://aws.amazon.com)
- [Google Cloud](https://cloud.google.com)
- [Microsoft Azure](https://azure.microsoft.com)
- [Yandex](https://yandex.com)
- [Anthropic](https://www.anthropic.com)
- [OpenAI](https://openai.com)
- [Base10](https://base10.ai)
- [Tavoli](https://tavoli.ai)
- [DigitalOcean](https://www.digitalocean.com)
- [Hetzner](https://www.hetzner.com)
- [Linode](https://www.linode.com)
- [Snowflake](https://www.snowflake.com)
- [MongoDB](https://www.mongodb.com)
- [ClickHouse](https://clickhouse.com)
- [Redpoint Ventures](https://redpoint.com)

## Reading Priority

Medium – A detailed, insider perspective on the operational and strategic challenges of building an AI cloud, with concrete technical and market insights from a leading competitor to hyperscalers.

***

# Building Legal Agents When You Can't See the Data - Jacob Lauritzen, CTO of Legora

- **Published:** 2026-11-02
- **Podcast:** [Latent Space](https://lspace.beehiiv.com/podcast/s/latent_space_the_ai_engineer_podcast/building_legal_agents_when_you_can_t_see_the_data_-_jacob_lauritzen_cto_of_legora)
- **Speaker:** Jacob Lauritzen, CTO of Legora

## One-Sentence Takeaway
Building high-impact legal AI agents requires solving privacy, evaluation, and workflow orchestration without access to the underlying data.

## Short Summary
Legora’s agents automate legal tasks (e.g., due diligence, contract review) while preserving client confidentiality—Legora cannot see the data it processes. The company focuses on domain-specific workflows (e.g., tabular review for bulk document analysis) and model routing, using a mix of frontier and open models optimized for cost, latency, and task-specific performance.

Evaluation is critical but constrained: Legora’s evals team (lawyers + engineers) tracks model performance across legal subdomains, revealing that new model releases often regress on specific tasks even as they improve overall. The product evolves toward orchestration (e.g., intake, lists) and agent swarms, with forward-deployed engineers and "legal engineers" (ex-big law lawyers with CS backgrounds) bridging gaps between core product and client needs.

## Main Ideas
- **Privacy as a constraint**: Legora’s agents operate on confidential client data it cannot access, forcing reliance on synthetic evals, strict data isolation (e.g., Azure-only hosting), and client-side controls.
- **Model routing over selection**: Instead of exposing model pickers to users, Legora subdivides tasks (e.g., transcription vs. analysis) and routes to the best model (e.g., Gemini for speaker attribution, Microsoft for transcription) based on cost, latency, and governance.
- **Evals reveal regression**: New model releases often improve some legal tasks while regressing on others (e.g., citation accuracy jumped from 70% to 99% in one release, but other tasks degraded), necessitating continuous, domain-specific benchmarking.
- **Workflow primitives**: Core building blocks like *Tabular View* (spreadsheet-style bulk document review), *Lists* (Notion-like databases), and *Intake* (Slack-integrated task orchestration) enable customization without code, while forward-deployed engineers handle deeper integrations.
- **Legal engineering as a role**: Ex-big law lawyers with CS backgrounds ("legal engineers") configure workflows, run evals, and act as force multipliers, bridging product and client needs without writing code.

## Questions And Answers
**Q: How do you evaluate models when you can’t see the data?**
A: Legora’s evals team (lawyers + engineers) creates synthetic tasks (e.g., due diligence simulations) and tracks performance across legal subdomains (e.g., M&A, litigation) using a heatmap to spot regressions.

**Q: What’s the hardest part of building legal agents?**
A: Orchestrating workflows (e.g., due diligence) without visibility into the data, while ensuring citations, red-flag detection, and collaboration tools (e.g., Tabular View) meet legal standards.

**Q: How do you handle model selection for users?**
A: Legora routes tasks to the best model (e.g., Gemini for transcription, frontier models for analysis) based on cost, latency, and governance, but offers a model picker for users who insist on control—despite the inefficiency.

**Q: What’s the future of legal work with agents?**
A: Lawyers will focus on high-value judgment (e.g., risk assessment, client strategy), while agents handle menial tasks (e.g., document review). The partnership model may shift as firms codify expertise into systems (e.g., knowledge graphs) to create durable capital.

## Notable Details
- **Tabular View**: Spreadsheet-style bulk review of up to 1M cells/documents, with citations and collaborative flagging; built on AG Grid.
- **Evals team**: 3 engineers + 3 lawyers + a pool of "legal engineers" (ex-big law with CS degrees) to run domain-specific benchmarks.
- **Model quirks**: Early Gemini models excel at transcription/speaker attribution; Microsoft’s newer transcription model outperforms older Gemini for legal jargon (e.g., avoiding "condom" for court roles).
- **Infrastructure**: Azure-only hosting due to law firm trust in Microsoft (365 integration); on-prem demands have faded as cloud security improved.
- **Acquisitions**: Used Legora’s own tools (e.g., Tabular View) for due diligence in acquisitions like Kira (Sweden) and Wexler (UK litigation fact intelligence).
- **Pricing pressure**: Law firms adopt flat-fee models for commoditized work (e.g., NDAs), while high-value work (e.g., M&A, litigation) remains hourly or relationship-based.

## Actionable Takeaways
- **For legal tech builders**: Prioritize workflow primitives (e.g., spreadsheets, lists) over raw model capabilities; privacy constraints demand synthetic evals and client-side controls.
- **For enterprise AI adopters**: Invest in "legal engineers" (domain experts + technical skills) to configure tools and run evals without code.
- **For model providers**: Legal tasks reveal niche strengths (e.g., transcription, citation) where specialized models can outperform generalists.
- **Watch for**: Agent swarms coordinating via primitives like *Lists*; shifts in law firm business models as agents codify expertise into reusable systems.

## People, Companies, Tools, And Links Mentioned
- [Legora](https://www.legora.ai)
- [Kira](https://kirasystems.com) (acquired by Legora)
- [Wexler](https://wexler.ai) (acquired by Legora)
- [AG Grid](https://www.ag-grid.com/)
- [Azure](https://azure.microsoft.com)
- [Anthropic](https://www.anthropic.com)
- [Google Gemini](https://deepmind.google/technologies/gemini/)
- [Microsoft Transcription Model](https://azure.microsoft.com/en-us/products/ai-services/speech/)
- [Y Combinator](https://www.ycombinator.com)
- [Cognition Labs](https://cognition.ai)
- [Palantir](https://www.palantir.com)

## Reading Priority

Medium – A concrete look at building domain-specific agents under strict privacy constraints, with actionable insights on evals, workflows, and the evolving legal tech landscape.

***

# How a 19-year-old intern built the growth engine behind this $2B AI company | Hector Serrano

- **Published:** 2026-11-01
- **Podcast:** [Lenny's Podcast](https://www.lennysnewsletter.com/p/how-a-19-year-old-intern-built-the)

## One-Sentence Takeaway
Paid user-generated content (UGC) programs, structured with performance-based compensation and a tight-knit creator community, can drive explosive growth for SaaS companies with strong product-market fit.

***

## Short Summary
Wispr Flow’s growth engine relies on a paid UGC program where 50 creators produce 500–600 ads monthly, earning uncapped commissions tied to ad spend. The model combines performance incentives (e.g., 10–20% of ad spend) with "smart retainers" to ensure creators stay motivated during early ramp-up. Success hinges on treating creators as partners, avoiding rigid briefs, and fostering a culture of experimentation—even "ugly" ads can outperform polished ones.

The approach works for SaaS despite attribution challenges, and it’s adaptable to niche or technical audiences by matching creators to specific ICPs (e.g., lawyers, engineers). Young marketers with hands-on content experience—regardless of traditional credentials—are uniquely suited to build these programs, as they intuitively understand platform trends and creator psychology.

***

## Main Ideas
- **Product-market fit is the foundation**: Paid growth channels amplify organic traction but cannot compensate for a weak product. Wispr Flow’s 30x revenue growth followed only after achieving PMF.
- **Paid UGC outperforms organic UGC for SaaS**: Organic UGC (CPM-based) chased vanity metrics with low conversions; paid UGC (performance-based) aligns creator incentives with revenue and scales sustainably.
- **Performance-based compensation unlocks creator retention**: Creators earn 10–20% of ad spend (or GMV for e-commerce), with "smart retainers" (e.g., $1,500 for 25 videos) bridging early gaps. Top creators earn $13,000+/month, far exceeding traditional influencer rates.
- **Avoid creative constraints**: Rigid briefs stifle creativity; Wispr Flow’s best ads (e.g., a keyboard typing in the rain) emerged from unscripted experimentation. Creators often understand the product better than the marketing team.
- **Culture and community drive quality**: Weekly meetings, giveaways, and in-person retreats foster loyalty. Creators refer peers (with $100 referral bonuses), and the program caps at 50 to maintain exclusivity.
- **Young marketers have a natural advantage**: Gen Z creators intuitively grasp platform nuances (e.g., TikTok, Instagram) and can spot trends faster than older hires. Hiring should prioritize hands-on content experience (e.g., growing a 10K+ following) over traditional credentials.

***
***
## Questions And Answers

**Q: When should startups invest in paid growth?**
A: Early—even pre-PMF. Paid ads provide fast feedback on messaging, conversion, and cold traffic viability, accelerating learning. Organic content is harder to measure and scale without deep platform expertise.

**Q: How do you structure creator compensation?**
A: For SaaS, pay a percentage of ad spend (e.g., 10–20%) due to attribution complexity. For e-commerce, use a percentage of GMV. Supplement with "smart retainers" (e.g., $1,500 for 25 videos) to ensure early earnings.

**Q: How do you find the first creators?**
A: Manually DM 150–250 targeted creators on Instagram (search niche keywords like "UGC creators," "tech," or "lawyer"). Avoid mass outreach; prioritize creators whose content aligns with your ICP. Early creators often come from your brand’s existing followers or DMs.

**Q: Why does UGC work for technical or enterprise SaaS?**
A: Match creators to the audience. For dev tools, use older, technical creators; for sleep products, avoid 18-year-olds. "Ugly" screen-recorded ads can outperform polished content for serious buyers.

***
***
## Notable Details
- Wispr Flow’s paid UGC program runs **500–600 ads/month** with **50 creators**, paying out **$300,000+ total** (as displayed on Tribe’s platform).
- Top creators earn **$13,000+/month** from commissions alone, with no earnings cap.
- **Ad fatigue mitigation**: Meta’s algorithm penalizes ads >60% similar (e.g., same script, visuals). Wispr Flow avoids this by encouraging constant experimentation—no two ads in their library look alike.
- **Outreach conversion**: 150–250 targeted DMs typically yield **5–6 high-quality creators**.
- **Payout frequency**: Weekly payouts (every 7 days) maximize creator motivation and dopamine-driven engagement.
- **Team structure**: Only **2 roles** are essential to start: a creative lead (e.g., Hector) to manage creators and a media buyer to optimize ad spend.

***
***
## Actionable Takeaways
- **Start small**: Launch with 5–10 creators, each targeting a distinct ICP or messaging angle. Scale only after proving the model.
- **Prioritize platform fit**: Use **Tribe** for SaaS to manage performance-based payouts; it’s the closest equivalent to TikTok Shop for Meta ads.
- **Hire for scrappiness**: Look for marketers with **10K+ followers on Instagram/YouTube** and a track record of consistent content creation. Ignore traditional credentials (GPA, school) in favor of demonstrated hustle.
- **Treat creators like partners**: Onboard with 1:1 calls, share product roadmaps, and host community events. This reduces churn and improves ad quality.
- **Experiment relentlessly**: Run high volumes of diverse ads (even "ugly" ones) to discover unexpected winners. Avoid over-optimizing for aesthetics.

***
***
## People, Companies, Tools, And Links Mentioned
- **People**:
  - Hector Serrano
  - Tanae (Tobin Tang?)
  - Daniel McCallum
  - Tobin Tang
  - Matt Swulinski
  - Lukas Pakter
  - Jimmy Farley
  - Eric Zaworski
  - Naval Ravikant
  - Elizabeth Stone (Netflix CPTO)
- **Companies/Tools**:
  - [Wispr Flow](https://wisprflow.ai)
  - [Tribe](https://jointrybe.com)
  - [WorkOS](https://workos.com)
  - [DX](https://getdx.com/lenny)
  - [Polymarket](https://polymarket.us)
  - [SquidHaus](https://gohaus.com)
  - [Physician’s Choice](https://physicianschoice.com)
  - [Victor](https://viktor.com)
  - [Miso](https://miso.com)
- **Links**:
  - [Hector’s X/Twitter](https://x.com/hectorserrranoo)
  - [Hector’s LinkedIn](https://linkedin.com/in/hector-serrano-martin)
  - [Hector’s YouTube](https://www.youtube.com/@hectorchats)
  - [Lenny’s Newsletter](https://www.lennysnewsletter.com)
  - [Hector’s paid-UGC playbook on X](https://x.com/hectorserrranoo/status/2108260769603486100)
  - [“The best marketers are allergic to AI” on X](https://x.com/hectorserrranoo/status/2110432634451169699)
  - [“Startups should recruit more like sports teams” on X](https://x.com/hectorserrranoo/status/2113676414973259782)

***
***
## Reading Priority

Medium – A tactical, step-by-step playbook for scaling paid UGC in SaaS, with concrete examples and counterintuitive insights (e.g., "ugly ads" outperforming polished ones).

***

# ⚡ Building ChatGPT for Finance — Joseph Kim, OpenAI's Head of Financial Services

- **Published:** 2026-10-31
- **Podcast:** [Latent Space](https://www.youtube.com/watch?v=v-d1WTqIULs)
- **Speaker:** Joseph Kim, Head of Financial Services at OpenAI

## One-Sentence Takeaway
Enterprise-grade AI in finance succeeds by bundling high-quality data, domain-specific workflows, and human-in-the-loop safety—while the next frontier is training models on fuzzy, high-judgment tasks like investment thesis generation.

## Short Summary

OpenAI’s ChatGPT for Financial Services targets enterprise knowledge work by integrating curated financial data (e.g., earnings transcripts) and firm-specific templates, addressing gaps left by unreliable third-party connectors. The product leverages ChatGPT’s plugin architecture, with 95% of its value achievable by startups or enterprises—only the final 20% of domain-specific polish required OpenAI’s direct involvement.

The bigger challenge ahead is scaling model capabilities from junior analyst tasks (e.g., slide formatting) to higher-judgment work (e.g., investment ideas), which demands better evals, human preference data, and research focus. Safety relies on existing hierarchical review systems in finance, treating models like junior staff whose work is audited by humans.

## Main Ideas
- Enterprise AI in finance must account for industry realities (e.g., data quality, workflows) rather than rely solely on first-principles reasoning. OpenAI found third-party MCP connectors for financial data had error rates over 40%, necessitating in-house data bundling despite redundant licensing costs.
- The "last 20%" of domain-specific polish (e.g., UI, integrations) is critical—ChatGPT alone would fail as a financial product without it, but this layer is buildable by startups using OpenAI’s plugin primitives.
- Model capabilities are progressing from verifiable tasks (e.g., Excel checks) to fuzzy, high-judgment domains (e.g., investment theses), requiring new evals, human preference training (e.g., pairwise slide comparisons), and sustained research focus.
- Safety in finance leverages existing human hierarchies: models are treated as junior analysts, with work reviewed by associates, VPs, and MDs. Future systems will mimic human permissions (e.g., read/write access) to align with institutional controls.
- Financial benchmarks are broken or saturated—OpenAI’s internal evals for GPT-6 revealed flaws like incorrect answer keys, prompting a push to build profession-specific evals (e.g., "automate a junior analyst’s work").

## Questions And Answers
**Q: What’s the technical approach to adapting a model for a new domain (e.g., legal or sales)?**
A: 95% of the work uses existing plugin architecture; only 5% requires model-level changes. Focus on the "last 20%" of domain-specific polish (e.g., integrations, UI) to bridge the gap between a generic model and a viable product.

**Q: How do you train models for "taste" (e.g., slide design, investment judgment)?**
A: Use pairwise human preferences (e.g., "Which slide looks better?") to train reward models, mirroring early RLHF methods. Coding’s mix of verifiable rewards (e.g., "does it compile?") and human taste (e.g., "is this clean?") is a blueprint for finance.

**Q: How should analysts adopt AI tools given the fear of career-ending mistakes?**
A: Models are improving fastest at factual reliability (reducing hallucinations), but still lag on human judgment (e.g., aesthetics). Use AI for tedious tasks (e.g., Excel, slides) while relying on existing review hierarchies to catch errors.

## Notable Details
- OpenAI’s financial reasoning data is upstreamed into the main model runs (e.g., GPT-6), making it available to all builders, not just first-party products.
- Codex adoption in finance jumped from ~0% to 90% after the February 2026 desktop app release, highlighting the importance of co-developing model capabilities and product surfaces.
- OpenAI is prioritizing hiring subject-matter experts (e.g., ex-investment bankers) to improve financial model training, akin to how coding expertise accelerated code-generation models.
- GPT-6’s financial evals showed stagnant scores due to saturated or flawed benchmarks, prompting OpenAI to develop new, profession-specific evals tied to real-world automation potential.
- Predictions for 2027: Models will improve at "human taste" (e.g., slide design) and begin tackling associate/MD-level tasks (e.g., investment theses), though objectives are fuzzier and harder to evaluate.

## Actionable Takeaways
- For enterprise AI in regulated domains, audit third-party data connectors rigorously—error rates may be unacceptably high, justifying in-house solutions.
- Build on top of existing plugin architectures to capture the "last 20%" of domain-specific value; the barrier to entry is lower than assumed.
- Design safety frameworks that mirror human workflows (e.g., hierarchical reviews, permission systems) to ease adoption in risk-averse industries.
- Invest in profession-specific evals that correlate with real-world automation potential, as generic benchmarks are often saturated or misleading.
- Watch for OpenAI’s prosumer rollout of ChatGPT for Financial Services to test capabilities before enterprise adoption.

## People, Companies, Tools, And Links Mentioned
- OpenAI
- Morgan Stanley (design partner)
- Evercore (design partner)
- S&P Global
- DeLoop
- Codex
- GPT-6
- GPT-6 Astra
- ChatGPT for Financial Services
- [Keynote at AIE Finance (YouTube)](https://www.youtube.com/watch?v=v-d1WTqIULs)
- Cognition (Frontier Code)
- SWE-bench
- GDP eval
- RLHF (Reinforcement Learning from Human Feedback)

## Reading Priority

Medium – A concrete look at how OpenAI is bridging the gap between general-purpose models and enterprise finance, with actionable insights on data, safety, and evals.

***

# Using Agents for Long-Horizon Financial Work — Aman Singh, Arca

- **Published:** 2026-10-31
- **Podcast:** [Latent Space](https://latent.space/p/arca)
- **Speaker:** Aman Singh, Arca

## One-Sentence Takeaway
Arca demonstrates how AI-native wealth management can proactively automate back-office analysis while keeping humans in the loop for critical decisions, improving service quality and compliance.

## Short Summary
Arca is an AI-native wealth management firm that uses agents to automate complex, long-horizon financial tasks (e.g., tax planning, portfolio rebalancing) while reserving execution and client communication for human advisors. The system relies on a custom, model-agnostic harness, tiered model selection, and persistent memory to track multi-day workflows, with strict guardrails for safety, auditability, and compliance.

The approach prioritizes proactive service—agents prompt humans more than humans prompt agents—enabled by internal knowledge bases, deterministic safety checks, and LLM-based verification for data integrity and regulatory adherence.

## Main Ideas
- **Proactive agentic workflows**: Agents handle long-running tasks (e.g., 10-day portfolio adjustments) by maintaining persistent memory of client state, goals, and deadlines, surfacing human intervention points only when necessary.
- **Tiered model selection**: Tasks are routed to model tiers (e.g., Opus, Sonnet, GPT-heavy) based on complexity, with internal benchmarks guiding provider choices (e.g., Anthropic, OpenAI) over external evaluations.
- **Safety and compliance by design**: Deterministic guardrails, LLM-based verification for data writes, and edge checks for prompt injection/PII ensure auditability and regulatory adherence, with all actions logged for both agents and humans.
- **Human-in-the-loop execution**: Agents perform analysis (e.g., tax optimization, fee detection) but defer money movement, trades, and client communication to advisors, preserving service quality and trust.

## Questions And Answers
**How do agents resume long-horizon tasks after delays?**
Agents rely on a centralized memory system tracking client state, pending actions, and deadlines, combined with "dreaming" processes that reflect on updates (e.g., new emails, calls) to recontextualize work.

**What prevents agents from executing trades autonomously?**
Strict guardrails reserve money movement, liquidation, and client communication for humans; agents propose plans (e.g., tax-optimized liquidation) but require advisor approval for execution.

**How does Arca improve agent accuracy for financial tasks?**
Decision models (e.g., from JV) validate recommendations against verified knowledge bases (e.g., current tax brackets) and flag errors like outdated data or non-compliant language in artifacts.

**How is feedback looped back into the system?**
Staff edits/cancellations trigger mandatory explanations, which are paired with agent traces. A nightly meta-agent suggests harness improvements (e.g., tool fixes, knowledge gaps), reviewed by engineers before deployment.

## Notable Details
- Arca’s harness is model-agnostic, using sandboxes for safe code execution (e.g., financial plan generation) with strict data access controls and post-processing verification.
- Internal benchmarks overruled external claims for models like Luna due to latency/cost issues, emphasizing vendor-agnostic flexibility.
- Agents detected hidden fees and non-fiduciary status in a prospect’s existing advisory relationship, showcasing proactive analysis capabilities.
- Compliance benefits from AI’s tireless checks (e.g., scanning PDFs for non-compliant return promises) exceed human-only processes.

## Actionable Takeaways
- For AI-native firms, own the harness and operational knowledge to standardize workflows and retain control over intelligence.
- Use tiered models and internal benchmarks to optimize cost/performance tradeoffs for heterogeneous tasks.
- Implement deterministic safety layers (e.g., PII checks) and LLM-based verifiers at capability edges (e.g., data egress, client artifacts).
- Design feedback loops to tie agent traces to human corrections, enabling traceable, iterative improvements.
- Prioritize auditability by default—log all actions (agent/human) with timestamps, actors, and change contexts for compliance.

## People, Companies, Tools, And Links Mentioned
- Arca
- Aman Singh
- Anthropic (Claude, Luna)
- OpenAI
- Frontier Labs
- JV (decision models)
- [Latent Space: Using Agents for Long-Horizon Financial Work — Aman Singh, Arca](https://latent.space/p/arca)

## Reading Priority

Medium – A concrete case study of enterprise AI agents in regulated financial services, with technical depth on harness design, safety, and human-AI collaboration.

***
