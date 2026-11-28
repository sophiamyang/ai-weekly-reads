---
title: "AI Weekly Reads - 2026-11-28"
aliases:
  - "AI Weekly Reads - 2026-11-28"
  - "AI Weekly Reads 2026-11-28"
created: "2026-11-28"
type: "weekly-book"
status: "ready"
language: "en"
---

# AI Weekly Reads

Week of 2026-11-28

[Download the latest EPUB for Kindle](latest.epub)

## Contents

1. [Latent Space / Podcast] 2026-11-27 - Inside the AI Training Data Market — Gabe Greenberg, G2i
2. [Latent Space / Podcast] 2026-11-26 - How Clay Builds GTM Agents — Jeff Barg, Head of AI
3. [Latent Space / Podcast] 2026-11-25 - The Revolution vs The Renaissance — Thariq Shihipar, OpenAI
4. [Training Data / Podcast] 2026-11-24 - OpenAI’s Noam Brown: Why Game Theory Didn’t Lead to General Intelligence (Live at No Limit Finals)
5. [Unsupervised Learning / Podcast] 2026-11-24 - Ep 98: China Expert on Jensen’s Return
6. [Lenny's Podcast / Podcast] 2026-11-22 - First principles: What it takes to be a great product manager in the AI era | Sherif Mansour

## Reading Notes

# Inside the AI Training Data Market — Gabe Greenberg, G2i

- **Published:** 2026-11-27
- **Podcast:** [Latent Space](https://lspace.beehiiv.com/podcast/s/latent_space_the_ai_engineer_podcast/inside_the_ai_training_data_market_gabe_greenberg_g2i)
- **Speaker:** Gabe Greenberg – CEO, G2i

## One-Sentence Takeaway

G2i's human-data pipeline for frontier labs has scaled from $15M to a projected $100M in revenue in one year by shifting from gig-work annotators to staff-level engineers and exclusive, high-quality datasets.

## Short Summary

Frontier labs now treat data as a first-class lever in post-training, spending 4–6% (and sometimes up to 50%) of compute budgets on human data to avoid waste. G2i has captured this demand by building a proprietary network of staff engineers who can design RL environments and curate niche datasets (coding, STEM, 3D, robotics) that are “just hard enough” to be trainable but not so hard they become evals. The market is concentrated—five or six labs account for most revenue—and procurement is fast, pilot-style, and partner-oriented rather than enterprise RFP. Exclusivity clauses are negotiable: labs will pay a premium for exclusivity or accept off-the-shelf data at a discount, depending on their immediate benchmark needs.

## Main Ideas

- Frontier labs are shifting human-data spend from 2–3% to 4–6% (and sometimes 50%) of total compute budgets because better data reduces wasted flops during post-training.
- G2i moved from 6,000 gig workers in 2023–24 to staff-level engineers today, emphasizing agentic coding ability, taste, and the ability to design RL environments rather than simple annotation.
- The market is concentrated: five or six labs drive most revenue; procurement is pilot-based, fast (minutes to allocate millions), and lacks formal RFPs.
- Exclusivity is negotiable: labs pay more for exclusive datasets or accept off-the-shelf data at a discount depending on benchmark urgency.
- G2i’s internal multi-agent orchestration platform (ORC.ai) is used to run its own “software factory,” and is now being productized for enterprise, security, and government use cases.

## Questions And Answers

**Q: What changed in human data between 2023–24 and today?**
A: In 2023–24, labs hired mid-level engineers in gig-work fashion; today they hire staff-level engineers for complex data set building, taste work, and RL environment design.

**Q: How do labs decide between exclusive and off-the-shelf data?**
A: If a lab needs a quick benchmark lift, they’ll buy off-the-shelf at a discount; if they want a competitive moat, they’ll pay a premium for exclusivity.

## Notable Details

- G2i revenue: $15M in 2023 → projected $100M in 2024; profitable, no VC backing; could triple next year.
- Labs can allocate multi-million-dollar budgets in minutes; researchers can spend $10M in 60 seconds.
- RL environment anti-patterns include confusing production code quality with RL verifier requirements; G2i screens for agentic engineers who can design features in 30 minutes.
- Data pricing is based on average handling time (AHT): a two-week task with 10% iteration is one unit, not a flat “per task.”
- Security risks include leaked instructions, supply-chain issues, and competitors in the same pool; incidents have exposed training material but rarely cost vendors their status because alternatives are scarce.
- G2i’s ORC.ai multi-agent orchestration platform is built in Rust, hostable anywhere, and used internally for coding, security, and government workflows.

## Actionable Takeaways

- If you’re a startup with ≥10 employees and a few terabytes of clean, cohesive data, consider monetizing it via curated data marketplaces.
- Invest in staff-level engineers who can design RL environments and curate “trainable” datasets rather than simple annotation tasks.
- For enterprise pilots, expect fast, pilot-style procurement with minimal RFP overhead; focus on partner-style collaboration and gap analysis.
- Watch for labs shifting more compute spend to post-training data (4–6% and up); this is a leading indicator of demand for high-quality human data.
- Evaluate multi-agent orchestration platforms (e.g., ORC.ai) if you need opinionated governance, inter-agent comms, and SDK-driven extensibility.

## People, Companies, Tools, And Links Mentioned

- Gabe Greenberg – CEO, G2i
- G2i – [g2i.ai](https://g2i.ai)
- ORC.ai – G2i’s multi-agent orchestration platform
- SuiBench / SuiBench Pro – industry benchmarks referenced for coding tasks
- Anthropic – cited as an example of labs rebuilding tooling (e.g., GitHub alternatives)
- YC startups – mentioned as potential data sellers

## Reading Priority

Medium – A concrete insider view of the frontier-lab data market, pricing, and procurement dynamics with vendor-presented scale and mechanisms.

***

# How Clay Builds GTM Agents — Jeff Barg, Head of AI

- **Published:** 2026-11-26
- **Podcast:** [Latent Space](https://lspace.beehiiv.com/podcast/s/latent_space_the_ai_engineer_podcast/how_clay_builds_gtm_agents_jeff_barg_head_of_ai)
- **Speaker:** Jeff Barg, Head of AI

## How Clay Builds GTM Agents — Jeff Barg, Head of AI

**URL:** [Latent Space Podcast](https://lspace.beehiiv.com/podcast/s/latent_space_the_ai_engineer_podcast/how_clay_builds_gtm_agents_jeff_barg_head_of_ai)
**Source type:** podcast
**Published:** 2026-11-26

***

## One-Sentence Takeaway

Clay’s AI agents are designed to be as effective as external coding harnesses like Claude Code, ensuring users get similar results whether they use Clay’s native agent or an external tool, while focusing on go-to-market engineering as a creative, data-driven discipline.

***

## Short Summary

Clay positions itself as a “creative tool for growth,” helping revenue teams build systems to find and qualify customers at scale. The company’s AI agents—Claygent for task-level work and Sculptor for orchestrating multi-step workflows—are built to be flexible enough for power users like go-to-market engineers while remaining accessible to less technical users. Jeff Barg, Head of AI at Clay, emphasizes that the goal is not to make Clay’s agent *markedly better* than external harnesses, but to ensure it integrates seamlessly into the platform and delivers consistent value.

The conversation highlights the evolution of Clay’s agent stack, from early web-crawling agents to a modern coding-agent architecture that leverages CLI-based workflows. Barg also discusses the company’s approach to model routing, post-training, and infrastructure, emphasizing cost efficiency, scalability, and user trust. A key insight is that go-to-market engineering is increasingly a software engineering discipline, blending data mining, entity resolution, and automation into scalable revenue systems.

***

## Main Ideas

- Clay’s AI agents (Claygent and Sculptor) are designed to be as effective as external coding harnesses like Claude Code, with usage split nearly 50/50 between Clay’s native agent and external tools.
- The company explicitly avoids making its agent *markedly better* than alternatives, prioritizing platform integration and user choice over competitive differentiation.
- Go-to-market engineering is framed as a creative, software-driven discipline that combines data engineering, prompt engineering, and traditional software development to build scalable revenue systems.
- Clay rebuilt its agent architecture to use a CLI-based coding agent in a cloud sandbox, improving expressivity and enabling access to all Clay platform primitives.
- Model routing and post-training are emerging priorities, with a focus on cost reduction and performance optimization, though frontier model training remains challenging and premature for most teams.

***

## Questions And Answers

**Q: What percentage of Clay users use the native agent versus external harnesses like Claude Code?**
A: Usage is split close to 50/50 between Clay’s agent and external harnesses.

**Q: Why does Clay not make its agent markedly better than external tools?**
A: Clay wants users to get similar results whether they use Clay’s agent or point an external tool like Claude Code at Clay. The goal is platform integration and user choice, not competitive differentiation.

**Q: What was the hardest part about building Clay’s Signals product?**
A: The diversity of customer needs and the scale of use cases—some users tracked every customer interaction, career progressions, news mentions, and more—created unexpected complexity in designing a system that could handle such varied and large-scale workflows.

**Q: What’s the biggest learning from Avenue that was applied to Clay?**
A: Focus on a single customer persona. At Avenue, the team struggled to define a core customer, but at Clay, everything is built for the go-to-market engineer, enabling deeper product-market fit.

***

## Notable Details

- Clay maintains a company dataset of 40 million companies and can run ICP (ideal customer profile) queries across all of them for around $1,500 in inference costs.
- Clay’s agent product (Claygent) was launched in November 2023, enabling structured data extraction from web searches directly into spreadsheet cells.
- Sculptor, launched in September 2024, acts as an orchestrator for Claygent agents, building multi-step workflows like outbound campaigns.
- Clay rebuilt its agent stack to use a CLI-based coding agent in a cloud sandbox, improving expressivity and enabling access to all Clay platform primitives.
- The company is exploring post-training and model routing to reduce costs and improve performance, targeting inference spend in the $10–$100 million range for material savings.
- Clay’s internal data stack includes ClickHouse for product use and Snowflake for analytics, with most in-product data pipelines hand-rolled on Postgres.
- BullMQ is used for agent durability, though the team acknowledges potential scalability limits as usage grows.

***
## Actionable Takeaways

- If building AI agents for enterprise workflows, prioritize platform integration and user choice over competitive differentiation—users often prefer familiar tools.
- Invest in robust observability (e.g., LangSmith) and throttling mechanisms early to handle spiky inference workloads and provider outages.
- Focus on a single core customer persona to drive product depth and clarity, even if early traction comes from broader use cases.
- Consider post-training and model routing only after inference spend reaches material levels ($10–$100M), and avoid premature frontier model training.
- Build a canonical data context layer (e.g., audiences) to unify CRM, Gong, and other data sources, enabling richer agent workflows.
- Monitor the balance between native agent adoption and external harness usage—it signals whether your platform is sticky enough for power users.

***
## People, Companies, Tools, And Links Mentioned

- **Clay** – [clay.com](https://www.clay.com/)
- **Avenue** – Acquired by Clay; previously focused on marketplace operations observability.
- **Cursor / Cloud Code** – External coding harnesses used by Clay’s go-to-market team.
- **LangSmith** – Used for agent observability and debugging.
- **BullMQ** – Job queue used for agent durability.
- **ClickHouse** – Used for in-product data storage and querying.
- **Snowflake** – Used for analytics.
- **Postgres** – Underlying database for most in-product data pipelines.
- **Grokbot** – Mentioned as a preferred external agent harness by some users.
- **Jev** – A classifier model discussed as a potential fit for Clay’s use cases.
- **GLM 5.3 Flash / Opus** – Reference models for cost-performance comparisons.
- **Temporal** – Mentioned in context of workflow orchestration (not used by Clay).

***
## Reading Priority

High – Clay’s approach to agent design, model routing, and infrastructure offers practical insights for AI teams building enterprise agents, especially in go-to-market contexts. The emphasis on user choice and platform integration is a thoughtful counterpoint to competitive agent-first strategies.

***

# The Revolution vs The Renaissance — Thariq Shihipar, OpenAI

- **Published:** 2026-11-25
- **Podcast:** [Latent Space](https://lspace.beehiiv.com/podcast/s/latent_space_the_ai_engineer_podcast/the_revolution_vs_the_renaissance_thariq_shihipar_openai)
- **Speaker:** Thariq Shihipar, OpenAI

## One-Sentence Takeaway

AI can simultaneously industrialize software production (revolution) and elevate craftsmanship and personal expression (renaissance), and the best outcomes come from intentionally designing the human feedback loop back into the process.

## Short Summary

Thariq Shihipar argues that AI-driven software development is entering a dual phase: a revolution that makes software cheaper and more reliable at scale, and a renaissance that allows for personal craftsmanship and marginal quality improvements. He emphasizes that the most valuable software emerges when humans actively participate in the loop—not as bottlenecks to be removed, but as taste-makers and evaluators. His own work—building a game with a custom “/human” scripting layer—illustrates how structured human-in-the-loop development can yield software that is both functional and personally resonant. He also critiques the rush to fully autonomous “dark factories” and advocates for decision models, personal software, and multi-agent communication as promising frontiers.

## Main Ideas

- AI is both an **industrial revolution** (scalable, reliable, standardized output) and a **renaissance** (personal, expressive, high-taste output), and both can coexist in the same project.
- Fully autonomous agents (“dark factories”) risk producing “slop” because they lack human feedback and dogfooding during development.
- Thariq uses a custom scripting language called “/human” to create human-readable, spec-like code that he can play with, adjust, and understand—bridging AI generation and human taste.
- **Decision models** (fast, low-latency, single-forward-pass models) are undervalued today but offer a powerful middle ground between hardcoded logic and full inference loops, especially for support bots and dynamic systems.
- Personal software is becoming feasible: small, niche tools that integrate deeply with native platforms (e.g., macOS docks, iPhone Shortcuts, widgets) can be prototyped quickly and iterated based on real usage.
- Multi-agent communication—letting different AI assistants (e.g., Dot, Duet, Grokbot) share context—could reduce redundancy and improve user experience, but today’s ecosystem encourages redundant clones rather than coherent integration.
- The future of AI research may turn into **knowledge work**: models handle the technical heavy lifting (wet labs, compute, correctness), while humans focus on strategy, resource allocation, and stakeholder buy-in.
- AI-native enterprises won’t emerge from pure efficiency gains alone; true value comes from frontier applications (robotics, biology, energy) where AI accelerates discovery and unlocks new revenue streams.

## Questions And Answers

**Q: You mentioned being wrong about “Bash is all you need” and “React is all you need.” What changed your mind?**

A: As models become more general, they can work in whatever format you want—including drawing in Figma or generating code in multiple paradigms—so the idea that everything must be forced into one narrow format (like Bash or React) is outdated.

**Q: How do you balance the Industrial Revolution and Renaissance in a single project?**

A: Use AI to generate the underlying primitives (e.g., a game engine in WebAssembly), then layer a human-readable scripting language on top for iteration and taste-making. Automate balance testing, but keep a human in the loop to avoid boring, perfectly balanced outcomes.

**Q: What excites you most about decision models today?**

A: They enable fast, low-latency responses with known behavior after one forward pass—ideal for support bots, routing, and systems where you want predictable, interpretable decisions without heavy inference loops.

## Notable Details

- Thariq builds a game using a custom scripting language called “/human,” where files are human-readable specs with strict formatting (no single-letter vars, dense comments, limited line length) to make the code understandable and tweakable.
- He found that default game mechanics (e.g., shift-to-boost) are easy for models to generate, but marginal improvements in feel and nuance require human iteration.
- In a card/board game simulation, AI-generated balance tweaks failed to create meaningful diversity; Thariq argues for adding variance (e.g., randomized tech trees, roguelike elements) to make imbalances interesting and fun.
- He uses Anthropic’s Claude and OpenAI’s Codex daily and reports not being token- or compute-bottlenecked on a $200/month plan.
- Thariq is exploring **weight-space programming**, **memory models**, and “do what I meant, not what I said” models as promising variants of decision models.
- He built a macOS dock alternative that combined focus states and activities, but ultimately didn’t use it—highlighting the difficulty of predicting personal needs without prototyping and dogfooding.
- He repurposes old NLP tasks (NER, extractive summarization) under new names as “decision models,” arguing that many classic models were effectively decision engines in disguise.

## Actionable Takeaways

- Build a “/human” layer in your projects: a folder or module where code is written for humans first, with strict formatting and rich comments, to enable iteration and taste-making.
- Use **decision models** for tasks that require fast, predictable, single-pass decisions (e.g., routing, support bots, state machines), especially when user input is unpredictable.
- Prototype **personal software** aggressively—use native hooks (Shortcuts, widgets, iMessage, Apple Health) to create tools that fit your exact workflow, even if they’re niche.
- Design for **human-in-the-loop** in agent systems: don’t remove the human; make it easy to test, dogfood, and refine outputs in real time.
- Avoid “dark factory” traps: autonomy without evaluation leads to slop. Keep a tight feedback loop between generation and use.
- Experiment with **multi-agent communication**: connect your AI assistants (e.g., Dot, Duet, Grokbot) via a shared context file to reduce redundancy and improve coherence.
- Watch for **frontier applications** (robotics, biology, energy) where AI accelerates discovery—not just enterprise efficiency.

## People, Companies, Tools, And Links Mentioned

- **Thariq Shihipar** – AI Engineer and Researcher, OpenAI
- **Claude** – Anthropic’s language model
- **Codex** – OpenAI’s code generation model
- **/human** – Thariq’s custom scripting layer for human-readable, spec-like code
- **WebAssembly** – Target runtime for the game engine in his project
- **Decision models** – Fast, low-latency models optimized for single-forward-pass decisions
- **Frontier Lab** – Thariq’s card/board game project
- **Shortcuts (Apple)** – Automation tool for iPhone and macOS
- **Jira by Atlassian** – Mentioned as a tool for managing agent swarms and shared context
- **Lucius (Luna)** – OpenAI’s decision model
- **Sol** – OpenAI’s system-one model
- **Opus 5.5** – OpenAI model cited for improved efficiency and intelligence
- **RSI (Recursive Self-Improvement)** – The idea that models improve their own training, inference, or research processes
- **WoW (World of Warcraft)** – Mentioned as a “prosthetic for achievement” for organizing teams and solving complex coordination problems

## Reading Priority

Medium – Thariq Shihipar offers a thoughtful, practitioner-oriented perspective on balancing automation with craftsmanship in AI-driven development, grounded in concrete examples and clear tradeoffs.

***

# OpenAI’s Noam Brown: Why Game Theory Didn’t Lead to General Intelligence (Live at No Limit Finals)

- **Published:** 2026-11-24
- **Podcast:** [Training Data](https://pscrb.fm/rss/p/traffic.megaphone.fm/CPUAI4645919503.mp3)

## One-Sentence Takeaway

Game theory alone is insufficient for general intelligence because humans are irrational; the path to advanced AI lies in training models to imitate human behavior and reason step-by-step, not in scaling up pre-training.

## Short Summary

Noam Brown’s research trajectory—from building superhuman poker AIs to Diplomacy bots—revealed a critical flaw in relying on game theory: it assumes perfect rationality, which humans do not exhibit. This insight led to a “crisis of faith” and a pivot toward training models on human data to capture real-world irrationality. At OpenAI, Brown contributed to the development of reasoning models like o1, which combine chain-of-thought reasoning with reinforcement learning to scale test-time compute. He argues that AI progress today resembles a “centaur period,” where humans and AI collaborate, with models excelling in narrow domains but still requiring human guidance for long-term planning and problem decomposition. Brown also contends that recursive self-improvement (RSI) is accelerating AI development, making it a pivotal time for students to join labs rather than wait for formal education to conclude.

## Main Ideas

- Game theory assumes rational players, but humans are predictably irrational; modeling human behavior through imitation learning is more effective for AI than pure game-theoretic approaches.
- The breakthrough in AI reasoning came from combining chain-of-thought prompting with reinforcement learning, enabling models to “think before acting” and scale test-time compute.
- OpenAI’s o1 and later models demonstrate that reasoning can be trained, not just scaled, addressing limitations of larger pre-trained models that struggle with tasks like chess or poker.
- AI today is in a “centaur period,” where human-AI collaboration is essential; humans must guide models by breaking problems into solvable sub-tasks and leveraging the models’ strengths.
- Recursive self-improvement (RSI) is accelerating AI progress, with models already aiding in tasks like data quality and tool development, though bottlenecks like compute and long-tail weaknesses remain.

## Questions And Answers

**Q: Why can’t models build a great poker bot on their own?**
A: Models lack long-term planning and organizational skills; they may over-optimize irrelevant details (e.g., CFR numerics) and fail to recognize when they’re heading down the wrong path. Humans compensate by decomposing problems and guiding the model toward solvable sub-tasks.

**Q: Is chain-of-thought the right way to scale test-time compute?**
A: Chain-of-thought is a sufficient but imperfect solution; it verbalizes reasoning in English, which may not capture all forms of thought (e.g., visual thinking). However, it has proven effective for scaling reasoning in language models.

**Q: Should promising students drop out to join AI labs now?**
A: Brown argues yes, citing rapid progress and the value of hands-on experience in labs. He notes that several successful hires joined after dropping out or skipping senior year.

**Q: Will an AI win the World Series of Poker in the next five years?**
A: Unlikely if the AI plays a game-theoretic optimal (GTO) strategy due to high variance, but a 20% chance exists if the AI excels at reading opponents’ tells and exploiting weaknesses.

## Notable Details

- Brown’s poker bots won the MIT PokerBots competition in 2014 and 2015, earning $10,000 in prize money, which he donated to avoid exploiting non-experts.
- Diplomacy was chosen as a harder challenge than poker or Go because it involves natural language negotiation, cooperation, and alliances, requiring models to capture human irrationality.
- In the Ultimatum Game, game theory suggests offering a penny, but humans reject unfair offers, highlighting the need for models to learn from human data rather than assume rationality.
- OpenAI’s reasoning models (e.g., o1) improve with longer “thinking” time before responding, scaling test-time compute to enhance performance across domains.
- Brown uses “building a poker bot” as a personal evaluation metric for new models; early models were 10–20x worse than humans, but recent models (e.g., Astra) can create competent river solvers autonomously.
- RSI is not new—human technological progress has always been recursive—but AI’s generality and speed make it unprecedented, with models already aiding in data quality and tool development.

## Actionable Takeaways

- If you’re building agents, pair them with humans to handle their “jagged” capabilities; break problems into sub-tasks where the model excels and let humans handle the rest.
- For research or coding tasks, use models to generate ideas or prototypes, then iterate with human oversight to correct long-term planning flaws.
- Evaluate new models by asking them to build a poker bot or solve a complex game; this reveals their strengths (e.g., river solving) and weaknesses (e.g., full-game planning).
- Stay close to the lab environment if you’re a student; hands-on experience with RSI and rapid iteration may outpace formal education in AI research.
- Watch for models that combine reasoning with tool use (e.g., compilers, search) as a proxy for future RSI breakthroughs.

## People, Companies, Tools, And Links Mentioned

- **Noam Brown** – [OpenAI profile](https://openai.com/index/author/noam-brown/)
- **Alfred Lin** – Partner at Sequoia Capital
- **MIT PokerBots competition**
- **OpenAI o1**
- **GPT-6 Astra**
- **Counter-Strike** (video game)
- **Ultimatum Game**
- **CFR (Counterfactual Regret Minimization)**
- **JEPA (Joint Embedding Predictive Architecture)**
- **World Series of Poker (WSOP)**

## Reading Priority

Medium – Noam Brown’s insights on reasoning, game theory, and the “centaur period” offer a grounded perspective on AI’s current trajectory and limitations.

***

# Ep 98: China Expert on Jensen’s Return

- **Published:** 2026-11-24
- **Podcast:** [Unsupervised Learning](https://unsupervised-learning.simplecast.com/episodes/ep-98-china-expert-on-jensens-return-hq9diKMj)

## One-Sentence Takeaway

Jensen Huang’s return as NVIDIA CEO stabilizes the AI ecosystem and U.S. AI leadership, but the deeper issue—willful blindness to chip smuggling into China—remains unresolved and politically explosive.

## Short Summary

Jordan Schneider argues that NVIDIA’s chip smuggling to China, tolerated under Jensen Huang’s leadership, was the real scandal—not the alleged affair with a Chinese national. The political backlash, including a new U.S. Commerce rule cutting off Chinese remote access via Malaysian data centers, forced Huang’s temporary ouster and rapid reinstatement. While Huang’s return strengthens NVIDIA and U.S. AI infrastructure, the long-term risk is bipartisan outrage over AI’s dual-use risks and public backlash, which money alone cannot solve.

The conversation also highlights structural vulnerabilities: China’s dominance in rare earths for robotics, the fragility of humanoid robotics demos, and the likelihood that China will soon impose export controls on strategic AI data and models. Schneider warns AI founders to expect tightening global controls and geopolitical friction regardless of U.S. administration.

## Main Ideas

- NVIDIA’s alleged willful blindness to chip smuggling into China—including military-linked use—was the core scandal, not the personal affair allegations.
- The U.S. Commerce Department’s new rule blocking Chinese remote access via Malaysian data centers gained momentum due to the spy scandal and smuggling reports.
- Jensen Huang’s return stabilizes NVIDIA and the AI ecosystem, but the political and regulatory environment remains volatile and bipartisan.
- Humanoid robotics are still largely non-functional in real-world demos, and China’s control over rare earths for magnets creates a strategic dependency.
- China is likely to impose export controls on AI models and robotics data, mirroring U.S. export control strategies.
- Public backlash against AI is growing, driven by cyber incidents and labor concerns, and could lead to restrictive legislation within 2–3 years.

## Questions And Answers

**Q: Why did Jensen Huang get ousted and then reinstated so quickly?**
A: The board likely believed Trump intervened to secure a settlement (e.g., a $25M fine) and prevent further market disruption, as NVIDIA’s stock drop and political pressure made the situation untenable.

**Q: Will the U.S. Commerce rule on remote access be reversed?**
A: It’s possible if Trump pressures the Commerce Department, but Congress could codify the rule to prevent reversal. The rule’s fate depends on political momentum and bipartisan outrage.

**Q: Is AI a “normal technology” that can be safely exported, or a dual-use threat?**
A: The speaker argues AI is now a dual-use technology with clear national security implications, especially after models like Mythos demonstrated offensive cyber capabilities.

## Notable Details

- NVIDIA is reportedly facing a $25M fine as part of a settlement related to illegal chip sales to China.
- The U.S. Commerce rule blocks Chinese access to advanced chips via Malaysian data centers and requires approval for fabbing advanced chips in TSMC.
- A Supermicro executive used hair dryers to remove labels from server racks to smuggle NVIDIA chips into China.
- Chinese military procurement orders show demand for NVIDIA chips despite export bans.
- Only 2% of Americans want AI to progress faster, indicating significant public skepticism.
- Rare earth magnets used in robotics are 99% sourced from China, with no easy substitutes.
- DeepMind’s robot could “barely pick up a muffin” at a recent conference, highlighting the state of humanoid robotics.

## Actionable Takeaways

- Expect continued and possibly escalating U.S. export controls on AI chips, data, and models regardless of administration.
- Factor in high probability of Chinese export controls on strategic AI data and robotics components over the next 12–24 months.
- Plan for regulatory risk in AI infrastructure and enterprise deployments, especially those involving Chinese entities or data centers.
- Monitor public sentiment and state-level legislation as AI becomes a campaign issue in 2026–2028.
- Consider supply chain diversification for critical components (e.g., rare earth magnets) to reduce dependency on China.

## People, Companies, Tools, And Links Mentioned

- **Jensen Huang** – CEO of NVIDIA
- **Jordan Schneider** – Host of *ChinaTalk*
- **Jacob Effron** – Host of *Unsupervised Learning*
- **NVIDIA** – AI chip manufacturer
- **Supermicro** – Server manufacturer implicated in smuggling
- **Megaspeed** – Company linked to military chip procurement in China
- **Mythos** – AI model cited as evidence of AI’s dual-use nature
- **U.S. Commerce Department** – Issued the remote access rule
- **Pangram** – Tool used to analyze the Commerce rule
- **ChinaTalk** – Newsletter and podcast on China and technology
- [ChinaTalk](https://www.chinatalk.media)
- [Unsupervised Learning Podcast](https://unsupervised-learning.simplecast.com)

## Reading Priority

Medium – Jordan Schneider’s analysis of U.S.-China AI competition, NVIDIA’s regulatory and geopolitical risks, and the dual-use nature of AI models. - Low - Host banter, podcast housekeeping, and repetitive anecdotes about Jensen Huang’s ouster/reinstatement.

***

# First principles: What it takes to be a great product manager in the AI era | Sherif Mansour

- **Published:** 2026-11-22
- **Podcast:** [Lenny's Podcast](https://www.lennysnewsletter.com/p/first-principles-what-it-takes-to)
- **Speaker:** Sherif Mansour, Head of AI and Product Craft at Atlassian

## One-Sentence Takeaway
In the AI era, the most valuable product managers focus on building a "shared brain" for their teams—filling context gaps and steering direction rather than increasing throughput or becoming builders themselves.

## Short Summary
The core role of a product manager (PM) is to create alignment and context—customer, product/market, and business—so teams can make better decisions independently. AI amplifies both strengths and weaknesses, making direction (not speed) the primary bottleneck. PM roles are growing fastest in the AI era because organizations need more people to steer strategy, not just execute.

Atlassian’s experiments with AI builder teams (where PMs and designers became builders) initially boosted speed but ultimately revealed that direction, not throughput, was the real challenge. The best PMs are those who can identify and close context gaps, whether through shared experiences (e.g., involving engineers in customer interviews) or frameworks like the "artist/scientist/GM" triangle to match PMs to the right work.

## Main Ideas
- **PMs own decision-making velocity, not decisions themselves.** Their primary job is to fill context gaps (customer, product/market, business) so teams can align and act autonomously. This scales better than centralized decision-making, especially in larger organizations.
- **AI amplifies strengths and weaknesses.** Tools like AI lower the barrier to prototyping and building, but they don’t replace specialization. Teams still need domain expertise to identify "AI slop" (low-quality outputs) and refine solutions.
- **Direction, not throughput, is the bottleneck.** Atlassian’s experiment with AI builder teams showed that while speed increased initially, the real need was for PMs to provide strategic direction and coherence.
- **Diverse PM archetypes thrive in different contexts.** The "artist/scientist/GM" triangle helps match PMs to roles: artists lead with vision and experience, scientists with hypotheses and data, and GMs with business metrics. Few excel at all three.
- **"Bolting AI on" can be a valid strategy.** For established products, adding AI to existing workflows (e.g., Atlassian’s RovoAgents in Jira) is often more practical than rebuilding from scratch. This approach helps discover high-value use cases before productizing them.

## Questions And Answers
**Q: Why are PM roles growing fastest in the AI era?**
A: AI reduces the cost of building, making throughput less of a constraint. Organizations now need more PMs to provide direction, align teams, and ensure the right problems are being solved.

**Q: Should PMs learn to code or build with AI?**
A: PMs should focus on accelerating their team’s decision-making velocity. If coding or prototyping helps fill a context gap (e.g., clarifying vision), it can be useful, but it’s rarely the bottleneck. Specialization still matters.

**Q: How can teams spot AI slop?**
A: Seniors with domain expertise are best at identifying low-quality AI outputs, while juniors (or "AI natives") are more likely to experiment with new tools and workflows. Diverse teams balance innovation with quality.

**Q: When is starting with a solution (not a problem) the right approach?**
A: Two cases: (1) **Product discovery**—observing how customers manually solve problems (e.g., grouping sticky notes in Confluence) can reveal opportunities to productize workflows. (2) **Strategy**—starting with existing assets (e.g., Amazon’s inventory scale) to identify unique advantages.

## Notable Details
- Atlassian’s AI builder experiment: Teams initially moved faster without PMs/designers, but within a month, roles reverted because direction (not speed) was the issue.
- **38% of juniors** (internal and customer data) are more likely to adopt new tools than seniors, though seniors achieve higher quality and productivity with familiar tools.
- **RovoAgents**: Atlassian’s AI agents run ~10 million times/month in Jira/Confluence workflows, with some use cases later productized (e.g., sticky note grouping in whiteboards).
- **Artist PM signals**: Early indicators include visual thinking (e.g., drawing on whiteboards), focusing on experience over metrics, and starting with solutions to work backward into problems.
- **Hiring trend**: Atlassian is hiring more juniors to bring "AI-native" ways of working, complementing seniors who excel at identifying quality issues.

## Actionable Takeaways
- **Audit context gaps** in your team: Are engineers missing customer empathy? Are designers unaware of business constraints? Design activities (e.g., joint customer interviews) to close them.
- **Use the artist/scientist/GM framework** to hire or recalibrate PMs. Match archetypes to the work (e.g., artists for experience-led projects, scientists for growth).
- **Start with existing workflows** when adding AI: Identify human or rigid workflows in your product and "bolt on" AI to assist steps before rebuilding.
- **Pair juniors with seniors** to balance experimentation and quality. Juniors bring fresh, tool-agnostic perspectives; seniors provide domain expertise.
- **Celebrate weaknesses publicly** to normalize specialization. Build teams where strengths complement each other (e.g., an artist PM paired with a GM-focused counterpart).

## People, Companies, Tools, And Links Mentioned
- [Atlassian](https://www.atlassian.com)
- [Jira](https://www.atlassian.com/software/jira)
- [Confluence](https://www.atlassian.com/software/confluence)
- [WorkOS](https://workos.com)
- [DX](https://getdx.com/lenny)
- [Balsamiq](https://balsamiq.com)
- [Sherif Mansour on Medium](https://sherifmansour.medium.com)
- [How to: Use the Product Management Craft Triangle](https://sherifmansour.medium.com/how-to-use-the-product-management-craft-triangle-a6048b1c9bc9)
- [Direct the ship, don't row it](https://sherifmansour.medium.com/direct-the-ship-dont-row-it-28785929626f)
- [On hiring "juniors" in the world of AI](https://sherifmansour.medium.com/on-hiring-juniors-in-the-world-of-ai-b1d05843f167)

## Reading Priority

Medium – A counterintuitive but practical take on PM roles in the AI era, with actionable frameworks and Atlassian’s internal experiments as evidence.

***
