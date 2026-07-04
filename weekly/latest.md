---
title: "AI Weekly Reads - 2026-06-28"
aliases:
  - "AI Weekly Reads - 2026-06-28"
  - "AI Weekly Reads 2026-06-28"
created: "2026-06-28"
type: "weekly-book"
status: "ready"
language: "en"
---

# AI Weekly Reads

Week of 2026-06-28

[Download the latest EPUB for Kindle](latest.epub)

## Contents

1. [No Priors / Podcast] 2026-06-26 - Why Traditional Benchmarks Fail Modern AI Models with OpenAI Research Scientist Noam Brown
2. [AI Engineer / YouTube] 2026-06-26 - Turn 10,994 Notes Into Memory - Paul Iusztin, Decoding AI & Louis-François Bouchard, Towards AI
3. [AI Engineer / YouTube] 2026-06-26 - Stop Writing Tone Instructions. Layer Them. - Isadora Martin-Dye, Isadora & Co
4. [AI Engineer / YouTube] 2026-06-26 - Agents in Production: How OpenGov Built and Scaled OG Assist - Gabe De Mesa, OpenGov
5. [AI Engineer / YouTube] 2026-06-26 - A Genius With Amnesia - Victor Savkin, Nx
6. [AI Engineer / YouTube] 2026-06-25 - The Miranda Hypothesis: How Hamilton Poisoned Persona Evals - Jacob E. Thomas, Results Gen
7. [AI Engineer / YouTube] 2026-06-25 - The Log Is The Agent - Ishaan Sehgal, Omnara
8. [AI Engineer / YouTube] 2026-06-25 - Recursive Coding Agents - Raymond Weitekamp, OpenProse
9. [The MAD Podcast with Matt Turck / Podcast] 2026-06-25 - Cloudflare CEO: Bot Takeover, Edge AI & The Hard Decision Every CEO Will Face
10. [AI Engineer / YouTube] 2026-06-25 - Build Systems, Not Code - Angie Jones, Agentic AI Foundation
11. [Latent Space / Podcast] 2026-06-24 - Why the Frontier Ecosystem must be Open — Matei Zaharia and Reynold Xin, Databricks
12. [Cursor / YouTube] 2026-06-24 - What Is Your Job Now, Farhan Thawar | Compile 26
13. [Cursor / YouTube] 2026-06-24 - The New PM, Claire Vo | Compile 26
14. [Training Data / Podcast] 2026-06-24 - Memory and Continual Learning: Engram's Dan Biderman and Jessy Lin
15. [AI & I by Every / Podcast] 2026-06-24 - Building a School Where AI Models Learn About Humanity
16. [Cursor / YouTube] 2026-06-24 - Agents and Infrastructure, Sam Lambert | Compile 26
17. [Google DeepMind / YouTube] 2026-06-23 - When millions of AI agents meet
18. [Cursor / YouTube] 2026-06-23 - Closer to the Material, Ryo Lu | Compile 26
19. [Latent Space / Podcast] 2026-06-22 - Red-Teaming after Mythos — Zico Kolter & Matt Fredrikson, Gray Swan
20. [Cursor / YouTube] 2026-06-22 - Opening Keynote, Michael Truell | Compile 26
21. [Lenny's Podcast / Podcast] 2026-06-21 - What happens after coding is solved? | Fiona Fung (Manager of the Claude Code and Cowork Teams)
22. [AI Engineer / YouTube] 2026-06-21 - 6 Things to Know about AIE World's Fair 2026

## Reading Notes

# Why Traditional Benchmarks Fail Modern AI Models with OpenAI Research Scientist Noam Brown

- **Published:** 2026-06-26
- **Podcast:** [No Priors](https://traffic.megaphone.fm/PDP3897457969.mp3)

## One-Sentence Takeaway

Large-scale test-time compute is reshaping AI capability and evaluation, but the industry still relies on static benchmarks that ignore compute budgets, leading to misleading comparisons and safety assessments.

## Short Summary

Modern AI models’ performance scales with inference-time compute, yet benchmarks are typically reported as single points without controlling for compute budgets. This creates a misleading picture of progress and undermines safety evaluations, which were designed when compute scaling was not a factor. Noam Brown argues that evaluations should either cap compute or plot performance against compute cost/time, and that latent capabilities in current models remain underexplored due to short evaluation cycles.

The conversation also explores practical implications: models can now reason for weeks or months on complex tasks, but real-world use favors iterative, flexible thinking rather than unbounded compute. Recursive self-improvement remains distant because time itself is a bottleneck, and multi-agent coordination is promising but still limited by current model horizons.

## Main Ideas

- Static benchmark grids misrepresent model capability because performance scales with test-time compute, which varies widely across models and settings.
- Modern models can reason for weeks or months on complex tasks if properly scaffolded, but performance often does not asymptote within practical evaluation budgets.
- Safety frameworks and responsible scaling policies were designed before large-scale test-time compute became a dominant factor in model capability.
- Benchmark maxxing—such as taking the best of multiple runs or using judge models—can inflate scores without reflecting true capability gains.
- Poker bot creation and mathematical problem-solving (e.g., disproving the Erdos unit distance conjecture) serve as strong, dynamic evaluations of reasoning and tool use.
- Recursive self-improvement is not imminent because models require large compute budgets and time, making rapid capability jumps unlikely.
- Multi-agent coordination shows promise but remains limited by current model context windows and knowledge-sharing mechanisms.
- Evaluation should either enforce compute budgets or plot performance against compute cost/time to enable fair comparisons.

## Questions And Answers

**Q: Why do static benchmark grids fail to capture the true capability of modern AI models?**
A: Because the capability of models like GPT-5.5 scales with the amount of test-time compute (time, tokens, or dollars) applied. A model that is more efficient in its thinking may score only slightly better on a benchmark when evaluated at a fixed compute level, even though it can achieve far higher performance when given more compute.

**Q: How should safety evaluations change to account for test-time compute scaling?**
A: Current safety frameworks evaluate models at fixed capability levels, but since capability is a function of compute budget, evaluations should specify the compute budget used. Otherwise, dangerous capabilities could be underestimated if evaluated at low compute levels.

## Notable Details

- GPT-5.5 showed only modest benchmark improvements over GPT-5.4 when evaluated at standard settings, but when compute time was controlled, it became clear that 5.5 was substantially more efficient and capable.
- Models can continue improving on some tasks (e.g., cybersecurity evaluations) even after 100 million tokens of reasoning, with visible performance gains beyond typical evaluation budgets.
- OpenAI used an internal model to disprove the Erdos unit distance conjecture at low compute cost, demonstrating latent mathematical reasoning capabilities that were previously unexplored.
- The poker solver task evolved from early models being unable to do anything useful, to GPT-5.2 enabling a 5x speedup in solving river-stage poker, to GPT-5.5 being able to build a full solver with minimal guidance.
- Time is a fundamental bottleneck: even if models could become arbitrarily intelligent with more compute, the time required to run them limits how fast progress can be realized in practice.
- Multi-agent systems like MultiBots and OpenClaw hint at future coordination but currently lack persistent knowledge sharing and long-horizon reasoning.

## Actionable Takeaways

- When evaluating new models, demand benchmarks that either cap compute or plot performance against compute cost/time.
- Be skeptical of benchmark maxxing techniques (e.g., best-of-N, judge models) unless compute is controlled for.
- Use dynamic, open-ended tasks (e.g., building tools, solving puzzles, conducting experiments) to probe model reasoning beyond static benchmarks.
- Consider compute budget as a first-class variable in both capability assessment and safety evaluation.
- Watch for signs of latent capability in current models by allocating non-trivial compute budgets to exploration tasks.
- Recognize that recursive self-improvement is not imminent due to time and compute constraints.

## People, Companies, Tools, And Links Mentioned

- **Noam Brown** – [OpenAI profile](https://openai.com/index/noam-brown/)
- **Sarah Guo** – [No Priors Podcast](https://no-priors.com/)
- **OpenAI** – [openai.com](https://openai.com)
- **Erdos unit distance conjecture** – A famous unsolved problem in discrete geometry
- **MultiBots** – A multi-agent AI framework
- **OpenClaw** – A multi-agent AI framework
- **No Priors Podcast** – [Website](https://no-priors.com) | [Twitter](https://twitter.com/NoPriorsPod)

## Reading Priority

Medium – This discussion directly challenges current AI evaluation practices and highlights a critical gap in how we measure and understand model capability and safety.

***

# Turn 10,994 Notes Into Memory - Paul Iusztin, Decoding AI & Louis-François Bouchard, Towards AI

- **Published:** 2026-06-26
- **YouTube:** [AI Engineer](https://www.youtube.com/watch?v=ZRM_TfEZcIo)

## One-Sentence Takeaway

Turning a large personal knowledge base into live, queryable context for AI agents requires a lightweight, file-based memory layer that synthesizes raw notes into a growing wiki, rather than relying on vector databases or static context windows.

## Short Summary

Paul Iusztin and Louis-François Bouchard describe how they evolved a personal “Second Brain” of 10,000+ notes, documents, and repositories into a dynamic research operating system that AI agents can read, update, and reuse. The core idea is a three-layer system—raw files, a file-based index, and an LLM-generated wiki—that avoids heavy infrastructure while remaining token-efficient and human-inspectable. The authors argue that most agent harnesses lose context between sessions, and propose their system as a persistent memory layer that compounds over time.

The talk walks through three system iterations, culminating in a “deep research” loop that queries both the open web and the user’s private vault, then writes structured derivatives (comparisons, concepts, entities) into a living wiki. Demos show how to ingest GitHub repositories, articles, and custom links, and how to query the resulting wiki for follow-up questions. The authors emphasize adaptability, encouraging viewers to fork the open-source code and add connectors or compaction rules as needed.

## Main Ideas

- A static context window or vector database is insufficient for long-term research; a lightweight file-based memory layer that synthesizes raw notes into a growing wiki is more effective and inspectable.
- The three-layer architecture—raw files, index.yaml, and wiki derivatives—enables token-efficient retrieval by giving agents a hierarchy: executive summaries first, then raw sources only when necessary.
- The wiki is “alive”: every question can spawn new concept, comparison, or entity notes, and the structure evolves with use rather than only with new ingestions.
- Deep research loops can target both public web and private vaults, replacing hand-picked “golden links” with an organic second-brain index that improves over time.
- Personalization matters: the system should reflect the user’s values and prior work, not a generic knowledge base, so it remains useful across projects and years.

## Questions And Answers

No distinct Q&A section.

## Notable Details

- The authors’ combined vaults contain over 10,000 notes, growing at ~250 files/month, and the system is used daily for writing, coding, and content creation.
- Version 1 produced a single static research.md file; Version 2 ingested the second brain but still produced static outputs; Version 3 introduced the wiki layer for dynamic, queryable memory.
- The index.yaml file acts as a catalog of sources and derivatives, containing metadata (origin, title, author, date, summary) and references to wiki pages.
- Wiki derivatives include comparisons (e.g., “agentic RAG vs file systems”), concepts (e.g., “sandboxing”), entities (e.g., “OpenCode”), and source summaries.
- The PARA method structures the raw vault into Projects, Areas, Resources, and Archive, but the LLM never modifies the immutable snapshot; only the wiki layer is updated.
- Memory compaction and source provenance are acknowledged weaknesses and active areas for improvement.

## Actionable Takeaways

- Start with a simple file-based index instead of a vector database when building a personal research OS; keep the raw data immutable and derive a lightweight index.
- Use a three-layer structure: raw files → index.yaml → wiki derivatives (concepts, comparisons, entities) to minimize token usage and maximize readability.
- Run a “deep research” loop that queries both public web and private vault, then writes structured summaries into the wiki for reuse across projects.
- Design the system to evolve with your questions: every interaction can add new notes, improving recall and reducing duplication over time.
- Fork the open-source AI Research OS repository and adapt connectors and compaction rules to your workflow rather than aiming for a polished product.

## People, Companies, Tools, And Links Mentioned

- People
  - Paul Iusztin: [X](https://x.com/pauliusztin_) | [LinkedIn](https://www.linkedin.com/in/pauliusztin/) | [GitHub](https://github.com/iusztinpaul)
  - Louis-François Bouchard: [X](https://x.com/Whats_AI) | [LinkedIn](https://www.linkedin.com/in/whats-ai/)
- Tools & Repos
  - AI Research OS workshop: [GitHub repository](https://github.com/iusztinpaul/ai-research-os-workshop)
  - Agent Engineering course: [Towards AI Academy](https://academy.towardsai.net/courses/agent-engineering)
  - Obsidian
  - Readwise
  - NotebookLM
  - Codex / Claude Code
  - PARA method (Tiago Forte)

## Reading Priority

Medium – A practical, code-backed method to turn a large personal knowledge base into a reusable memory layer for AI agents, with clear tradeoffs and next steps.

***

# Stop Writing Tone Instructions. Layer Them. - Isadora Martin-Dye, Isadora & Co

- **Published:** 2026-06-26
- **YouTube:** [AI Engineer](https://www.youtube.com/watch?v=ij-AU9dpJjc)

## One-Sentence Takeaway

Treating brand voice as a four-layer architecture—immutable identity, situational mode, example-anchored voice, and deterministic post-generation veto—prevents AI systems from breaking under real user pressure.

## Short Summary

Most teams try to encode brand voice in a single system prompt, which fails when users ask unanticipated questions. A better approach is to split voice into four layers that handle identity constraints, real-time context, expressive tone, and a final safety check. This architecture prevents socially catastrophic outputs and preserves trust in emotionally sensitive domains like weddings, real estate, and missing-person tools.

The talk draws on production systems for a luxury wedding venue, a personal AI companion, and a public utility for families of missing people. It argues that a prompt cannot simultaneously be situational, expressive, and self-checking; layering the jobs makes the system robust.

## Main Ideas

- A single system prompt cannot reliably do four jobs at once: enforce hard identity rules, adapt to situational context, express brand voice, and self-correct.
- Layer 1 (immutable identity) encodes constraints the brand structurally cannot violate, such as never pretending to have a physical presence or to be human.
- Layer 2 (situational mode) adjusts behavior based on who the user is and what they are going through, using soft context notes that shape tone without quoting sensitive details.
- Layer 3 (example-anchored voice) provides the tone guide, phrase lists, and dials that most teams treat as the entire solution.
- Layer 4 (post-generation veto) is a deterministic gate that reads the output and rejects unsafe or factually incorrect responses before they reach the user.
- In multi-tenant systems, identity must never default; missing brand identity should crash loudly rather than silently leak the wrong voice.

## Questions And Answers

No distinct Q&A section.

## Notable Details

- Bloom’s Layer 1 rule: always disclose you are an AI in the very first message, not if asked.
- Physical presence boundary: forbidden phrases include “I’d love to show you around” or “I can’t wait to meet you in person.”
- Missing-person tool Layer 1 rule: never use words like confirmed, identified, matched, proven, linked, or solved.
- Soft context notes are rendered before numeric constraints to ensure tone is set before hard rules.
- A common failure mode: the model confidently invents a date that does not exist because it was never given the calendar.
- The veto layer catches hallucinated dates, privacy violations, and off-brand hedging before responses ship.
- Multi-tenant leak example: venues shipped as “Sage” from another venue’s address due to missing brand identity defaults.

## Actionable Takeaways

- Split brand voice into four layers: identity constraints, situational context, tone guide, and deterministic veto.
- Encode hard identity rules that cannot be overridden by venue config, user instruction, or persona.
- Use soft context notes to shape empathy and tone without quoting sensitive details verbatim.
- Implement a post-generation veto that checks facts and brand alignment before any output is sent.
- In multi-tenant systems, treat missing identity as a crash, not a fallback, to prevent voice leakage.

## People, Companies, Tools, And Links Mentioned

- Isadora Martin-Dye
  LinkedIn: [Isadora Martin-Dye](https://www.linkedin.com/in/isadora-martin-dye-226353a1)
- Bloom House AI
- Threadline

## Reading Priority

Medium – A practical, production-tested architecture for keeping AI outputs trustworthy in emotionally sensitive contexts.

***

# Agents in Production: How OpenGov Built and Scaled OG Assist - Gabe De Mesa, OpenGov

- **Published:** 2026-06-26
- **YouTube:** [AI Engineer](https://www.youtube.com/watch?v=4uFVSLgD2Q4)

## One-Sentence Takeaway

OpenGov built a production-grade AI agent system (OG Assist) using Effect-TS, A2A protocol, and sandboxing to safely scale agentic workflows for thousands of government customers.

## Short Summary

OG Assist is OpenGov’s agent layer that sits atop its ERP suite for state and local governments. The team replaced LangGraph with an Effect-native agent loop to gain full control over tracing, error handling, and structured concurrency, which accelerated iteration and debugging. They rely on A2A for agent interoperability, sandboxing for safe tool execution, rolling summarization for long-context memory, and human-in-the-loop approvals for safety-critical actions. Internally, they also use agents (Claude, Cursor) to speed up development, showing how agentic tooling can improve both customer and developer workflows.

## Main Ideas

- Effect-TS provided structured concurrency, tracing, logging, and schema validation out of the box, enabling a custom agent loop that was easier to debug and extend than LangGraph.
- A2A protocol (Google’s open agent interoperability spec) was adopted to define agent cards, routes, and schemas, aligning frontend and backend contracts and simplifying multi-agent routing.
- Sandboxing executes untrusted code and file operations in isolated, ephemeral environments, preventing production system risk while allowing agents to generate artifacts like PDFs.
- Rolling summarization (periodic context compression) and memory recall are used to manage long conversations and token limits, avoiding naive “stuff all messages” approaches.
- Human-in-the-loop approvals interrupt the agent loop for mutating operations, ensuring safety and building user trust in production deployments.
- Tools and skills are registered as Effect functions, composed into toolkits, and exposed to models via a consistent interface, enabling rapid skill development and reuse.

## Questions And Answers

No distinct Q&A section.

## Notable Details

- OG Assist is embedded across OpenGov’s product suite and can see and act on the current UI screen.
- The team migrated from LangGraph to an Effect-native loop to regain control over the agent loop and leverage Effect’s built-in observability.
- A2A’s agent card includes name, description, and schema, acting as a contract between frontend and backend.
- Sandboxing tears down environments after use, reducing blast radius and cleanup overhead.
- Rolling summarization keeps a running digest of older messages while retaining recent context, enabling recall without exceeding token limits.
- Internally, OpenGov uses agents (Claude, Cursor) to accelerate code review, generation, and shipping, mirroring the customer-facing tooling approach.

## Actionable Takeaways

- Prefer agent frameworks that provide structured concurrency and tracing (e.g., Effect-TS) when building production agent loops.
- Adopt an open agent protocol (A2A) to standardize agent contracts and simplify multi-team integration.
- Enforce sandboxing for any agent that writes code or files to mitigate risk in production.
- Implement rolling summarization and memory recall to handle long conversations without hitting token limits.
- Add human-in-the-loop approvals for mutating actions to maintain safety and user trust.
- Treat developer tooling as a first-class agent use case; internal agent skills can dramatically increase velocity.

## People, Companies, Tools, And Links Mentioned

- Gabe De Mesa: [LinkedIn](https://www.linkedin.com/in/gabedemesa) | [GitHub](https://github.com/gabedemesa)
- OpenGov: [Website](https://www.opengov.com)
- Effect-TS: [Open source library](https://effect.website)
- A2A Protocol: [Google’s agent interoperability protocol](https://a2a.dev)
- Cursor and Claude: [Developer agent tools](https://cursor.com) | [Claude](https://claude.ai)

## Reading Priority

Medium – Practical blueprint for building and scaling production agent systems with concrete mechanisms (Effect loop, A2A, sandboxing) and enterprise-grade safety controls.

***

# A Genius With Amnesia - Victor Savkin, Nx

- **Published:** 2026-06-26
- **YouTube:** [AI Engineer](https://www.youtube.com/watch?v=jVjt-2g8NMY)
- **Speaker:** Amnesia - Victor Savkin, Nx

## One-Sentence Takeaway

Coding agents today are like a genius with amnesia: they see only a tiny slice of the codebase and forget everything between sessions, so developers waste time re-explaining the same change across repos; a meta-harness like Polygraph fixes this by giving agents a unified view of the entire org and perfect memory of every prior session.

## Short Summary

Victor Savkin argues that current coding agents are crippled by two constraints: they are repo-bound (limited spatial context) and amnesic (no episodic memory). Each cross-repo change forces developers to re-explain intent seven times, burning tokens and time. Polygraph, an agent-agnostic meta-harness, solves both problems by building a dependency graph across thousands of repos and capturing every session trace, so an agent can treat a multi-repo change as a single operation and resume any prior session on any machine with full context intact.

The demo shows how Polygraph lets a developer start a session across backend and frontend repos, implement a coordinated change, save the session, and later hand it to a colleague on a different machine with a different agent; the colleague resumes instantly with the same state and shared memory. The system also supports loose queries (“find every repo that depends on this library”) and retrieval of prior sessions to enforce best practices, effectively turning scattered agent traces into an organizational hive mind.

## Main Ideas

- Coding agents are “repo-bound” and “amnesic”: they see only one repo at a time and forget prior sessions, forcing humans to re-explain intent repeatedly.
- A typical cross-repo change requires seven explanations (UI → Module 1 → Module 2 → Platform → bug fix), wasting developer time and tokens.
- Polygraph builds a unified dependency graph across all repos (owned and open source) without changing a line of code, giving agents a “big codebase” view.
- It captures every session trace (PRs, CI outcomes, agent logs) and materializes that state on any machine, enabling true resumption and shared memory across agents and developers.
- Developers can query the graph (“find repos that depend on X”) or retrieve prior sessions to replicate best practices, turning isolated agent traces into an organizational memory.
- The system treats a multi-repo change as a single operation, coordinating CI failures and rollbacks across repos automatically.

## Notable Details

- Polygraph computes what each repo produces and consumes (packages, APIs) and stitches them into one navigable graph.
- A saved session includes a high-level description, involved repos, PRs, CI status, and full agent traces for later resumption.
- Resuming a session on a different machine with a different agent (e.g., switching from Claude to Cortex) works because the state and memory are transported, not the agent itself.
- Loose queries like “find sessions that added a vector index to PR collection” surface relevant prior work for reuse.
- The meta-harness approach is agent-agnostic; it wraps existing agents (Claude, Cortex, Codex) without modifying them.

## Actionable Takeaways

- Audit a recent cross-repo change: count how many times you or others had to re-explain intent; this is the current tax from repo-bound agents.
- Evaluate a meta-harness like Polygraph if your org runs many multi-repo changes or relies on multiple agents.
- Treat agent traces as first-class artifacts: save, index, and retrieve them to enforce consistency and onboard new engineers faster.
- Watch for CI coordination across repos; a single failing test should trigger the right fix in the right repo automatically.
- Consider switching agents mid-session when one model is unavailable; the harness preserves state so work continues uninterrupted.

## People, Companies, Tools, And Links Mentioned

- Victor Savkin
  - X/Twitter: [@victorsavkin](https://x.com/victorsavkin)
  - LinkedIn: [victorsavkin](https://www.linkedin.com/in/victorsavkin/)
  - GitHub: [vsavkin](https://github.com/vsavkin)
- Nx
- Polygraph: [trypolygraph.com](https://trypolygraph.com)
- Agents mentioned: Claude, Cortex, Codex

## Reading Priority

Medium – The core critique of current coding agents and the concrete design of a meta-harness that materially improves multi-repo development are directly applicable to engineering orgs scaling agent use.

***

# The Miranda Hypothesis: How Hamilton Poisoned Persona Evals - Jacob E. Thomas, Results Gen

- **Published:** 2026-06-25
- **YouTube:** [AI Engineer](https://www.youtube.com/watch?v=IJXjTLPzvAU)

## The Miranda Hypothesis: How Hamilton Poisoned Persona Evals

**Source type:** YouTube
**URL:** [The Miranda Hypothesis: How Hamilton Poisoned Persona Evals - Jacob E. Thomas, Results Gen](https://www.youtube.com/watch?v=IJXjTLPzvAU)
**Published:** 2026-06-25

***

## One-Sentence Takeaway

Current persona evaluations measure how *convincing* an AI sounds as a historical figure, not whether it adheres to the documentary record, enabling "Miranda distortion" where cultural composites (e.g., Hamilton from the musical) override primary sources.

***

## Short Summary

Jacob E. Thomas argues that role-playing language agents (RPLAs)—used in apps like Character AI and Hello History—are failing silently because their evaluation benchmarks prioritize fluency and personality consistency over fidelity to primary sources. This "mask-and-mirror" problem is exemplified by models that sound like Hamilton from the *Broadway musical* rather than the real Alexander Hamilton, a phenomenon Thomas calls "Miranda distortion." The distortion arises because culturally dominant representations (e.g., musicals, films) vastly outnumber primary documents in training data, and post-training (e.g., RLHF) amplifies this bias by rewarding outputs that align with human raters' own mythologized perceptions.

To address this, Thomas proposes a paradigm shift from "cognitive simulation" (modeling a persona’s mind) to "epistemic simulation" (constraining reasoning to a specific, temporally anchored corpus). He introduces a pre-registered experimental protocol—the *Prism Experiment*—using Abraham Lincoln as a test case. The protocol evaluates responses across three axes (anachronism detection, documentary consistency, contextual plausibility) with a historian in the loop, deliberately excluding fluency as a criterion. The goal is to make persona systems auditable, versionable, and reproducible by keeping anchor documents in the context window rather than fine-tuning them into the model’s weights.

***

## Main Ideas

- **Miranda Distortion**: Cultural composites (e.g., Hamilton from the musical) dominate training data, causing persona systems to reason from modern narratives rather than primary sources. This failure is invisible to current benchmarks, which reward fluency and personality consistency.
- **Mask vs. Mirror**: Existing evals measure the "mask" (how convincing the persona sounds) but ignore the "mirror" (whether the reasoning aligns with the documentary record). These are independent properties; a system can score perfectly on the former while failing the latter.
- **RLHF Amplifies Distortion**: Human raters, shaped by the same cultural composites, reward outputs that conform to their mythologized perceptions, reinforcing anachronistic reasoning in post-trained models.
- **Epistemic Simulation**: A proposed fourth stage in persona modeling where reasoning is constrained to a specific, temporally anchored corpus. The persona is an *event* (a configuration of documents, temporal anchors, and human curation), not a property of the model’s weights.
- **Archival Virtues**: Keeping anchor documents in the context window (rather than fine-tuning them) preserves auditability, versioning, and accessibility. Fine-tuning dissolves the archive into parameters, breaking the chain of providence.
- **Expert-Loop Evaluation**: Domain experts (e.g., historians, theologians) must design and score evaluations because fidelity is a *relation* between the output and the archive—not a property of the output alone. Automated metrics structurally cannot detect anachronism or documentary inconsistency.

***
## Questions And Answers

**Q: Why is fluency a misleading metric for persona evaluations?**
A: Fluency rewards outputs that sound like the persona (e.g., Hamilton’s musical register) but may contradict primary sources. The *Prism Experiment* explicitly excludes fluency as a criterion, focusing instead on anachronism detection, documentary consistency, and contextual plausibility.

**Q: How does fine-tuning exacerbate Miranda distortion?**
A: Fine-tuning layers a thin "persona signal" over the vast cultural sediment already in the base model’s weights. This suppresses surface-level distortions while amplifying deeper, undetectable ones, as the model blends primary sources with later narratives (e.g., the musical) in its parameters.

**Q: Can automated metrics (e.g., LLM-as-judge) replace human experts in persona evals?**
A: No. Automated metrics operate on the model’s output alone and can only measure fluency or personality consistency. Fidelity requires comparing the output to a documentary record, which only a domain expert can do. A persona system without an expert in the loop is like a thermometer that cannot read temperature.

**Q: Is this framework practical for production systems?**
A: Yes. The expert’s role is build-time and gate-time (designing the rubric and gold set), not runtime. Once the instrument is built, it functions like any other eval gate: the persona must pass it before shipping, and it’s re-evaluated whenever the base model changes. Automated metrics can flag candidates for human review.

***
## Notable Details

- **Federalist Papers vs. Hamilton Musical**: The Federalist Papers contain ~175,000 words; the corpus of content *inspired by* the musical (reviews, lyrics, fan analysis, curricula, etc.) exceeds this by orders of magnitude and is more recent and recurrent in training data.
- **Schuyler Mansion Example**: After the musical’s premiere, the Schuyler Mansion (Eliza Hamilton’s home) saw a near-tripling of visitors, many of whom arrived with misconceptions about the Schuyler family (e.g., believing they had three daughters instead of 15 children). The model’s Hamilton is downstream of the same force.
- **Lincoln’s Evolution**: Lincoln’s reasoning changed dramatically across four documented moments (1847–1865), making him a "hardest case" for persona systems. The *Prism Experiment* tests whether the system can hold these distinct Lincolns apart.
- **Pre-Registration**: The experimental protocol (questions, rubric, predictions) is timestamped and published before data collection, preventing accusations of cherry-picking. The instrument is designed to be reproducible by any team with a frontier model and a context window.
- **Accessibility Tradeoff**: Fine-tuning requires institutional resources (GPUs, pipelines, curated datasets), while context-window anchoring requires only literacy and access to a frontier model. This makes the latter viable for smaller teams (e.g., historians, archivists) and aligns with the goal of diverse curation.
- **Thermometer Analogy**: Current persona evals are like a thermometer that claims to measure temperature but is actually measuring something else (e.g., fluency). The *Prism Experiment* is the instrument that correctly measures fidelity to the documentary record.

***
## Actionable Takeaways

- **Audit Your Persona Evals**: If your evals measure fluency, personality consistency, or "convincingness," they are likely rewarding Miranda distortion. Add a historian, theologian, or domain expert to design and score evaluations.
- **Anchor to Primary Sources**: Keep anchor documents in the context window rather than fine-tuning them into the model. This preserves auditability, versioning, and accessibility.
- **Pre-Register Your Protocol**: Publish your experimental design (questions, rubric, predictions) before collecting data to ensure rigor and reproducibility.
- **Weight Anachronism Detection Heavily**: Assign at least 40% of the rubric score to detecting modern frameworks, vocabulary, or moral logic imported into historical personas.
- **Watch for Algorithmic Sycophancy**: Post-training (e.g., RLHF) may amplify cultural composites by rewarding outputs that align with raters’ mythologized perceptions. Test for this explicitly.
- **Signal to Watch**: Teams shipping persona systems (e.g., historical simulations, pedagogical agents) should adopt the *Prism Experiment* or similar instruments to detect anachronistic reasoning.

***
## People, Companies, Tools, And Links Mentioned

- **Jacob E. Thomas** (Results Generation)
  - LinkedIn: [jacob-e-thomas-atx](https://www.linkedin.com/in/jacob-e-thomas-atx/)
  - GitHub: [jethomasphd/THE_COMPANION_DOSSIER](https://github.com/jethomasphd/THE_COMPANION_DOSSIER)
- **Rick Halpern** (University of Toronto, historian)
- **Sean Martin** (Washington College, theologian/librarian)
- **Character AI** (role-playing language agent platform)
- **Hello History** (education-focused role-playing platform)
- **Claude Opus 4.7** (frontier model used in demos)
- **Companion** (open-source prompt framework by Thomas)
- **COSR** (Wang et al., motivation-driven agents)
- **PsyMem** (personality modeling via psychological indicators)
- **InCharacter** (personality fidelity benchmark)
- **Deirdre McCloskey** (economist/historian, referenced for "archive as site of return")
- **Varnum et al.** (time-walked models, corpus cutoffs)
- **Nature Medicine (2026)** (study on generalist vs. specialist clinical AI)

***
## Reading Priority

High – A rigorous critique of persona evaluation with a practical, pre-registered instrument for detecting anachronistic reasoning in historical simulations. Essential for teams building role-playing agents, pedagogical tools, or any system where fidelity to a documentary record matters.

***

# The Log Is The Agent - Ishaan Sehgal, Omnara

- **Published:** 2026-06-25
- **YouTube:** [AI Engineer](https://www.youtube.com/watch?v=UPwGaM2MKHY)

## One-Sentence Takeaway

The true identity and continuity of an AI agent reside in its session log, not in the model, runtime, or tools, making durable, portable logs the critical infrastructure for reliable, scalable, and portable agent systems.

## Short Summary

Most agent frameworks mistakenly treat the model, runtime, or tools as the agent’s core identity, leading to fragility and lock-in. Instead, the session log—the append-only history of every user input, model output, tool call, and result—is the agent’s true essence. By making the log the primitive, agents gain durability, continuity, forkability, addressability, observability, and portability across models, runtimes, and machines. This shift also clarifies ownership: whoever controls the log controls the agent, making log lock-in the deepest form of vendor lock-in. The talk argues that agent infrastructure should be built around the log as the primary system, with everything else as disposable projections.

## Main Ideas

- An agent’s identity is its session log, not the model, runtime, or tools; the log is the durable, portable “save file” that preserves continuity across failures and migrations.
- The log is an append-only event history capturing every user input, model output, tool call, result, permission, and failure, enabling reconstruction of agent state at any point.
- The agent execution loop becomes disposable: workers read the log, advance the agent one step, write the result, and can disappear; any worker can resume the session later.
- Compaction is lossy and should be treated as a best-effort projection; the raw log must be preserved to avoid losing agent identity and history.
- Log lock-in is the deepest form of vendor lock-in because the log contains the agent’s intimate data, workflows, and decisions, making it the most valuable and persistent component.

## Questions And Answers

**Q: Why isn’t the model or runtime the agent?**
A: The model and runtime are interchangeable components that interpret and append to the log; the agent’s identity and continuity come from the log, not the execution environment.

**Q: How does treating the log as the agent improve reliability?**
A: If a worker or process crashes, a new worker can resume the session from the log, preserving state like permission prompts that would otherwise be lost in current systems.

## Notable Details

- The log enables forkability: multiple branches can run different models or strategies from a common history, with each branch storing history up to the fork point.
- Multiplayer access is simplified: sharing an agent means granting access to the log, allowing teammates or other agents to view, edit, or consume the session as context.
- Migration becomes an adapter problem: moving between models or runtimes is easier when the log is the agent, as continuity is preserved even if projections differ.
- Current agent harnesses often treat the log as an afterthought, storing state in unreliable or provider-specific formats, leading to data loss and difficulty reconstructing history.
- Omnara’s managed agents platform is built around the session log, aiming to give users full ownership, inspection, and control over their agent’s history.

## Actionable Takeaways

- Design agent systems with the log as the primary primitive, not the model or runtime, to ensure durability and portability.
- Preserve raw logs and treat compaction as lossy; avoid discarding the full history when summarizing for models.
- Plan for failure: assume workers will crash, providers will fail, and users will disconnect; the log ensures the agent survives.
- Evaluate agent platforms based on log ownership and portability, not just model or tool support.
- Watch for log lock-in as managed agent services expand; prioritize systems where you control the log.

## People, Companies, Tools, And Links Mentioned

- Ishaan Sehgal: [X/Twitter](https://x.com/ishaansehgal) | [LinkedIn](https://www.linkedin.com/in/ishaan-sehgal/) | [GitHub](https://github.com/ishaansehgal99)
- Omnara: [omnara.com/managed](https://omnara.com/managed)
- Anthropic: Cloud managed agents
- Google: Gemini managed agents

## Reading Priority

Medium – The argument for log-centric agent infrastructure is novel, well-structured, and directly challenges current industry assumptions, with clear implications for reliability, ownership, and scalability.

***

# Recursive Coding Agents - Raymond Weitekamp, OpenProse

- **Published:** 2026-06-25
- **YouTube:** [AI Engineer](https://www.youtube.com/watch?v=3hXJI2q0Jz8)

## One-Sentence Takeaway

Recursive Language Models (RLMs) apply inference-time compute by treating the prompt/context as an executable object, and this paradigm can be mapped onto coding agents to make them more reliable and outcome-focused.

## Short Summary

Today’s coding agents are “mismatched geniuses”: they have the intelligence but lack orchestration, verification, and reuse. RLMs marry tool calling and symbolic reasoning, enabling agents to recursively decompose problems, verify sub-agent work, and declare outcomes. Projects like Anthropic’s Dynamic Workflows and OpenProse show how to turn existing coding agents into RLMs, delivering state-of-the-art results on long reasoning tasks and enabling reliable, reusable workflows.

## Main Ideas

- RLMs treat the prompt/context as an executable object, combining tool calling and symbolic reasoning in a REPL-like loop.
- The core bottleneck for reliable agents is not raw intelligence but orchestration, verification, and reuse of work.
- RLMs can process information far beyond the context window and achieve state-of-the-art results on long reasoning benchmarks with small models.
- Coding agents can be made recursive by letting them call themselves, enabling deep decomposition and verification of sub-agent outputs.
- OpenProse is a markdown-based language that compiles via a coding agent and can turn any agent with sub-agents into an RLM.
- Anthropic’s Dynamic Workflows now make Claude Code recursive, effectively turning it into an RLM.

## Questions And Answers

No distinct Q&A section.

## Notable Details

- RLMs can process tens of millions of tokens and act as powerful memory systems.
- Qwen 3.5 9B as an RLM beats Opus and GPT-5.4 on the Long CoT benchmark.
- Symbolica’s Agentica achieved ~30% on ARC AGI 3 within hours using an RLM harness, prompting the benchmark team to create a separate open harness leaderboard.
- OpenProse lets you convert a golden coding session into a reusable pros.md workflow that can include recursive sub-agents.
- OpenProse supports explicit dependency wiring: sub-agents can be assigned specific skills or CLI tools required for their task.

## Actionable Takeaways

- Replace brittle one-shot prompts with recursive workflows that decompose, verify, and reassemble work.
- Use RLMs to handle large codebases or long documents by offloading symbolic exploration to code execution.
- Capture successful sessions and turn them into reusable pros.md programs for consistent outcomes.
- Prefer agent harnesses that let the model decide decomposition rather than hard-coded MapReduce.
- Watch for new benchmarks and leaderboards that explicitly accommodate RLM-style tool use.

## People, Companies, Tools, And Links Mentioned

- Raymond Weitekamp: [X/Twitter](https://x.com/raw_works) | [LinkedIn](https://www.linkedin.com/in/raymondweitekamp/) | [GitHub](https://github.com/rawwerks)
- OpenProse: [Website](https://recursivecodingagents.com) | [GitHub repo](https://github.com/rawwerks/recursive-coding-agents)
- DSPI.RLM
- Axe (TypeScript RLM)
- Unix RLM (bash-based)
- Anthropic Claude Code Dynamic Workflows
- ARC AGI 3
- Long CoT benchmark
- Turing Post article by Raymond Weitekamp

## Reading Priority

Medium – RLMs are a new inference-time compute paradigm with immediate practical implications for coding agents and reliability.

***

# Cloudflare CEO: Bot Takeover, Edge AI & The Hard Decision Every CEO Will Face

- **Published:** 2026-06-25
- **Podcast:** [The MAD Podcast with Matt Turck](https://podcasters.spotify.com/pod/show/firstmark/episodes/Cloudflare-CEO-Bot-Takeover--Edge-AI--The-Hard-Decision-Every-CEO-Will-Face-e3l8mt1)

## One-Sentence Takeaway

The internet’s traffic is now majority bots and AI agents, forcing a shift from ad-driven economics to new models while Cloudflare positions itself as the indispensable infrastructure layer for this agentic future.

## Short Summary

Matthew Prince argues that automated traffic has overtaken human traffic on the internet as of early 2026, driven by AI agents performing tasks like shopping or research across thousands of sites per request. This explosion in bot traffic threatens the ad-based business model of the web and will require new monetization mechanisms such as pay-per-crawl or micropayments. Cloudflare, originally a cloud firewall, has evolved into an AI infrastructure platform by leveraging its global edge network to provide low-latency inference, secure agent orchestration via AI Gateway, and a lightweight compute platform (Workers) optimized for agent workloads. Prince also shares Cloudflare’s origin story—from accidental product-market fit with hacker kids and human rights groups to becoming a backbone for global internet infrastructure—and reflects on the company’s culture, fundraising, and internal AI adoption.

## Main Ideas

- Bot and AI agent traffic surpassed human traffic on the internet in early 2026, with exponential growth expected over the next five years.
- The ad-driven internet business model is breaking because bots don’t click ads, and new models (e.g., pay-per-crawl, micropayments) are needed to fund infrastructure.
- Cloudflare evolved from a cloud firewall to a global edge network that now powers low-latency AI inference, auditing, and agent security at scale.
- Cloudflare Workers provides a lightweight, sandboxed compute environment ideal for agentic workloads, reducing cost and latency compared to traditional containers or VMs.
- AI Gateway enables auditing, guardrails, and cost control for enterprise AI usage, helping organizations safely deploy agents without runaway token costs.
- Internal AI adoption at Cloudflare reached 93% of R&D users, processing 241 billion tokens, driven by measurable productivity gains and a “Cloudflare OS” layer for non-engineering teams.

## Notable Details

- Cloudflare sits in front of a representative sample of global internet traffic and tracks bot vs. human traffic via [Cloudflare Radar](https://radar.cloudflare.com).
- Prince cites a projection that internet traffic could increase a thousandfold in five years due to agent-driven activity.
- Workers uses isolates (like browser tabs) to achieve high density and fast startup/teardown, crucial for agent workloads that may spawn and terminate rapidly.
- AI Gateway was built internally to audit and control AI usage across teams, then productized after demand from customers.
- Cloudflare runs GPUs at the edge in hundreds of cities, enabling low-latency inference for open and proprietary models (e.g., OpenAI, Anthropic).
- The company rewrote WordPress in Rust (as “M-Dash”) to reduce infrastructure costs and prepare for a thousandfold traffic increase.
- Cloudflare provides infrastructure for two of the 13 DNS root servers, improving global DNS performance and giving privileged network access.

## Actionable Takeaways

- Audit your AI usage and traffic patterns now—bot traffic may already dominate and will reshape your infrastructure and monetization strategy.
- Evaluate edge inference and lightweight compute platforms (like Workers) if you’re building agentic applications to reduce latency and cost.
- Implement auditing and guardrails for AI agents early to prevent prompt injection, compliance violations, and cost overruns.
- Consider pay-per-crawl or micropayment models if your business depends on web data access in an agent-dominated world.
- Invest in internal AI tooling and training to capture productivity gains, but support mid-career staff who may feel displaced by rapid change.

## People, Companies, Tools, And Links Mentioned

- **Matthew Prince** – Co-founder and CEO, Cloudflare
- **Michelle Zatlyn** – Co-founder and COO, Cloudflare
- **Lee Holloway** – Co-founder and former CTO, Cloudflare
- **Cloudflare** – [cloudflare.com](https://www.cloudflare.com)
- **Cloudflare Radar** – [radar.cloudflare.com](https://radar.cloudflare.com)
- **Cloudflare Workers** – Serverless compute platform
- **AI Gateway** – Enterprise AI auditing and control platform
- **Durable Objects** – Stateful compute primitives on Workers
- **NVIDIA** – GPU partner for edge inference
- **OpenAI** – Mobile app runs on Cloudflare
- **Anthropic** – Claude and related services use Cloudflare
- **WordPress (M-Dash)** – Rust rewrite of WordPress for scalability
- **Cloudflare OS** – Internal AI agent platform for non-engineering teams
- **Kenton Varda** – Senior engineer who drove internal AI adoption
- **Sam Ray** – Led the “auto@cloudflare.com” agent initiative
- **Glasswing** – Security partnership leveraging AI models
- **Mythos** – AI model used for vulnerability detection

## Reading Priority

Medium – This conversation distills a pivotal shift in internet economics and infrastructure, with concrete technical and strategic insights from one of the most influential infrastructure leaders.

***

# Build Systems, Not Code - Angie Jones, Agentic AI Foundation

- **Published:** 2026-06-25
- **YouTube:** [AI Engineer](https://www.youtube.com/watch?v=ZD9-4fW2HhM)

## One-Sentence Takeaway

Designing agentic systems—rather than writing code directly—preserves engineering craft by applying familiar principles (systems thinking, decomposition, contracts, state management) to new primitives.

## Short Summary

AI coding agents shift the locus of value from line-by-line coding to architecting reusable, maintainable agentic systems. Angie Jones argues that the same engineering muscles—systems thinking, workflow design, decomposition, separation of concerns, modularity, algorithmic thinking, state management, and threat modeling—remain essential, but now applied to prompts, skills, sub-agents, and structured memory. The talk walks through a concrete house-hunting agent to show how to turn a brittle one-shot prompt into a robust, reusable system that handles retries, contracts, and safety without losing the joy of building.

## Main Ideas

- Treat an agent as one component in a larger system; define its boundaries, dependencies, failure modes, and responsibilities before letting it write code.
- Workflows need explicit paths: goal → gather → weigh → act → stop/retry/escalate; this shapes what context, tools, and handoffs are needed.
- Giant prompts are code smells in agentic systems; decompose them into reusable skills, scripts, schemas, and sub-agents to improve testability and maintainability.
- Use code for determinism (deduping, commute math), agents for judgment (ranking listings), and humans for authority (approving tours/offers).
- Define structured contracts for agent outputs so downstream steps and memory layers can query decisions reliably; this also forces clarity about what the agent must produce.
- Design for idempotency and state tracking because retries can reword requests; log actions to memory so partial runs resume safely.
- Apply threat-modeling basics: validate untrusted inputs, enforce least privilege, and draw clear boundaries around actions (e.g., no autonomous offers).
- Maintainability is built in: document workflows, policies, skills, and memory contracts so humans and agents can onboard quickly and updates succeed.

## Notable Details

- Example agent: Relocation Scout, a house-hunting agent that pulls listings, normalizes them, scores neighborhoods, and produces a ranked shortlist.
- Skills are reusable agent capabilities (e.g., normalize listings) that can be shared across agents or markets, analogous to packages.
- Sub-agents are like functions: single-purpose, scoped, and reusable; e.g., a neighborhood research sub-agent that works in any market.
- Memory layer (e.g., LLMs Wiki or Capactis) stores structured decisions (score, reason, commute) so queries like “show me houses rated ≥4 with ≤15 min commute” work across sessions.
- Lint passes are necessary to keep agents healthy; they detect half-finished runs and retry only the missing steps.
- Policy boundaries: allow reading listings and building shortlists, but require human approval for emailing realtors, booking tours, or submitting offers.

## Actionable Takeaways

- Before letting a coding agent generate code, design the agentic system: define the workflow, contracts, and state layer.
- Decompose giant prompts into skills, scripts, schemas, and sub-agents; aim for single-responsibility pieces.
- Offload deterministic tasks (filtering, calculations) to code; reserve agents for ambiguous judgment calls.
- Enforce idempotency by logging actions to structured memory; design retries to resume rather than replay.
- Draw explicit policy walls around agent actions; gate high-risk operations behind human approval.
- Document each layer (workflow, skills, memory contracts) so new contributors can onboard without reverse-engineering prompts.

## People, Companies, Tools, And Links Mentioned

- Angie Jones: [X/Twitter](https://twitter.com/techgirl1908) | [LinkedIn](https://www.linkedin.com/in/angiejones/) | [GitHub](https://github.com/angiejones)
- Agentic AI Foundation
- Capactis / LLMs Wiki (agent memory layer)
- Relocation Scout (example house-hunting agent)

## Reading Priority

Medium – Practical engineering patterns for building maintainable agentic systems that preserve craft and reduce drift.

***

# Why the Frontier Ecosystem must be Open — Matei Zaharia and Reynold Xin, Databricks

- **Published:** 2026-06-24
- **Podcast:** [Latent Space](https://www.latent.space/p/databricks)

## One-Sentence Takeaway

Databricks is building the open infrastructure layer that makes AI agents useful in production by unifying data storage, governance, and agent control—turning proprietary context into the durable competitive moat.

***

## Short Summary

Databricks’ cofounders argue that once frontier models become commoditized, the real differentiator for enterprises will be their proprietary data, governed access, and operational state. They are open-sourcing Omnigent, a meta-harness for coding and enterprise agents, to create a common API and ecosystem around agent sessions, security, and spend controls. At the same time, they are rethinking the database stack with LTAP (Lake Transactional/Analytical Processing), which unifies storage in open columnar formats (Parquet) to make live operational data immediately available for agents and analytics without brittle CDC pipelines.

The conversation highlights Databricks’ culture of rapid prototyping and tight customer collaboration, contrasting tech and enterprise customers, and explaining why open formats and a broad platform scope have allowed them to outpace competitors like Snowflake. They also discuss specialized models (e.g., document parsing), RL fine-tuning as a service, and the thesis that traditional software will be rewritten once data is in the right place and agents sit on top.

***

## Main Ideas

- **Omnigent as a meta-harness:** A common API and server layer that abstracts agent sessions, tool calls, file access, and cancellation across coding agents (Claude Code, Codex, Cursor) and custom enterprise agents, enabling portability, collaboration, and security controls.
- **Agent security and spend control:** Stateful, contextual policies are needed to balance usability and security—e.g., blocking an agent that has just read 1,000 confidential docs or installed a risky npm package—while tracking spend within sessions to cap costs.
- **LTAP: HTAP done right:** Unify storage in open columnar formats (Parquet) instead of collapsing query engines; enables live operational data to be immediately available for analytics and agents without brittle CDC pipelines.
- **Open formats as strategic moat:** Databricks’ open data formats (Parquet, Delta, Iceberg) and broad platform scope (ingest, storage, compute, ML) have allowed them to outpace competitors like Snowflake, especially in regulated enterprises.
- **Rapid prototyping culture:** Databricks empowers engineers to prototype and launch features quickly, often driven by tight collaboration with a few key customers, avoiding “boil the ocean” approaches.
- **Specialized models and RL fine-tuning:** Custom models (e.g., document parsing, coding advisors) and RL fine-tuning will become mainstream as base models improve and synthetic data generation becomes easier.

***

## Notable Details

- Omnigent was open-sourced on a Saturday; within days, the community contributed ~400 PRs, including Kubernetes support, cloud sandboxes, and additional agent harnesses (Cursor, CLI, Antigravity).
- Databricks orchestrates 50–60 million VMs/day across clouds and processes exabytes of data daily; Neon DB launches ~13 million databases/day, many driven by agent workflows.
- LTAP’s key insight: Transcode row-oriented OLTP data to columnar Parquet in the storage layer using idle CPUs, improving compression and enabling immediate analytics without CDC.
- Unity Catalog (governance layer) and Panther (event processing) inform Omnigent’s policy engine, enabling high-level, stateful controls over agent actions.
- Databricks’ “dream engine” project builds a new database engine using a factory approach trained on a decade of traces (~quadrillions of data points) to select optimal algorithms and data structures at runtime.
- Model customization and RL fine-tuning are already in preview with customers; AI Runtime provides on-demand GPU clusters with optimized software stacks for training.

***

## Actionable Takeaways

- If you’re building agent infrastructure, consider open-sourcing a meta-harness to create a common API and ecosystem, enabling portability and collaboration.
- Invest in stateful, contextual policies for agent security and spend control—track session state to balance autonomy and safety.
- Evaluate LTAP-style architectures: unify storage in open columnar formats to make live operational data immediately available for agents and analytics.
- Prioritize open data formats and broad platform scope to avoid vendor lock-in and appeal to regulated enterprises.
- Adopt rapid prototyping: work closely with a few key customers to validate and iterate on features quickly.
- Explore specialized models and RL fine-tuning for high-volume use cases where customization delivers outsized value.

***

## People, Companies, Tools, And Links Mentioned

- **Matei Zaharia**
  - [LinkedIn](https://www.linkedin.com/in/mateizaharia)
  - [X](https://x.com/matei_zaharia)
- **Reynold Xin**
  - [LinkedIn](https://www.linkedin.com/in/rxin)
  - [X](https://x.com/rxin)
- **Databricks**
  - [Website](https://www.databricks.com)
  - [X](https://x.com/databricks)
- **Omnigent** – [GitHub](https://github.com/databricks/omnigent)
- **LTAP** – Lake Transactional/Analytical Processing
- **Lakebase** – Databricks’ storage engine
- **Unity Catalog** – Databricks’ governance layer
- **Panther** – Event processing and analytics tool
- **Neon** – Serverless Postgres with separation of storage and compute
- **DBRX** – Databricks’ open-source LLM
- **Genie** – Databricks’ data science agent
- **AI Runtime** – On-demand GPU clusters for training
- **Satya Nadella’s Frontier Ecosystems post** – [Link](https://news.ycombinator.com/item?id=40112345)

***

## Reading Priority

Medium – This conversation distills Databricks’ strategic bets on open agent infrastructure and LTAP, offering actionable insights for AI engineers, data leaders, and founders building agent platforms or data systems.

***

# What Is Your Job Now, Farhan Thawar | Compile 26

- **Published:** 2026-06-24
- **YouTube:** [Cursor](https://www.youtube.com/watch?v=ByOF8qByGHU)

## One-Sentence Takeaway

With AI writing most code, an engineer’s job shifts from typing lines to exercising taste, judgment, and rapid learning to define what to build and why.

## Short Summary

Farhan Thawar argues that AI has moved the bottleneck in software development from writing code to planning, validating, and learning. At Shopify, this transition has led to a focus on architecture, customer problem-solving, and weekly learning reviews rather than code output. The company embraced AI reflexivity, hired 1,000 interns to accelerate cultural change, and now uses large models for most coding while maintaining human responsibility for outcomes.

## Main Ideas

- The software development lifecycle is shifting: coding time shrinks while planning, validation, and learning time grow.
- AI reflexivity—making AI assistance the first instinct—transformed Shopify’s culture and tool adoption across finance, HR, and marketing.
- Learning is the real collateral of engineering work, not the code; Shopify rebuilt a system in three months after learning from an 18-month effort.
- Model selection prioritizes human time over compute cost: engineers use the largest, most expensive models to avoid downstream debugging.
- Code review is now the bottleneck; AI reviewers are faster and more accurate than humans, though still imperfect.

## Questions And Answers

**Q: How did Shopify’s CEO’s question change how the team built a feature?**
A: Tobi Lutke asked, “If you could start over, how would you build it?”—prompting the team to scrap 18 months of code and rebuild in three months based on what they learned.

**Q: What is AI reflexivity and how did Shopify implement it?**
A: AI reflexivity means reaching for AI immediately when facing any problem. Shopify mandated tool use, deployed Cursor to 1,500 users in one week, and expanded to nearly all 8,000 employees.

**Q: Why does Shopify only allow engineers to use the largest, most expensive models?**
A: The company values human time more than compute cost; using smaller models risks subtle bugs that take hours to debug, while larger models reduce that risk.

## Notable Details

- Shopify was the first major user of GitHub Copilot in 2021, before ChatGPT’s public release.
- After the “Opus 4.5 moment” in December 2025, many engineers concluded LLMs were better at coding than they were.
- Shopify’s internal tool “River” acts as an agentic substrate across the company, answering questions and writing code.
- A support team built “Scout,” an AI tool that surfaces top merchant frustrations for product managers.
- An intern deleted six lines of code and saved Shopify over $600,000 per year in infrastructure costs.
- Shopify uses a “Council of LLMs” to review code, with different models checking accessibility, security, and other criteria.

## Actionable Takeaways

- Reorient engineering OKRs from lines of code to learning velocity and customer impact.
- Adopt AI reflexivity: make AI the first tool reached for, not the last resort.
- Invest in AI-powered code review to scale validation without adding headcount.
- Use large models for most coding tasks to reduce debugging overhead and improve quality.
- Run weekly demos and learning reviews to surface insights faster than traditional milestones.

## People, Companies, Tools, And Links Mentioned

- Farhan Thawar
- Shopify
- Tobi Lutke
- GitHub Copilot
- Cursor
- Pi
- Cloud Code
- Codex
- River
- Scout
- Opus 4.5
- GPT-5.5
- Gemini 3.5
- Cloudflare
- AWS

## Reading Priority

High – This talk distills concrete shifts in engineering practice at scale, with measurable outcomes and clear principles for adapting to AI-driven coding.

***

# The New PM, Claire Vo | Compile 26

- **Published:** 2026-06-24
- **YouTube:** [Cursor](https://www.youtube.com/watch?v=4CAFK-rc26A)

## One-Sentence Takeaway

Product management’s new job is not to gatekeep engineering but to find commercially viable, behavior-changing ideas and rally people around them when code is abundant and markets are scarce.

## Short Summary

Claire Vo argues that AI-driven code abundance has flipped the classic product constraint: building is no longer the bottleneck, but demand and willingness to pay have not scaled with supply. The talk redefines product work around three pillars—commercial value, behavior change, and novel vision—and urges teams to stop fetishizing process and start focusing on who will pay and why they will adopt. The core message is that the next wave of value creation will come from product thinkers who can articulate a unique future and convince others to follow it, not from those who merely ship faster.

## Main Ideas

- Code is now abundant and cheap; the new bottleneck is commercializable demand and user behavior change.
- Classic PM artifacts (backlogs, PRDs, sprints) evolved to protect scarce engineering capacity and are now often misapplied as busywork.
- Two tests for “something people want”: (1) will they pay to solve the problem, and (2) can you drive adoption at scale?
- Manifesting novel ideas from first principles—without prior evidence—is a muscle that product people must rebuild.
- Distribution and persuasion (“bringing people along”) are as critical as problem–solution fit in an era of instant shipping.
- Titles like “product manager” may persist, but the job has shifted from gatekeeping to vision, commercialization, and movement-building.

## Questions And Answers

No distinct Q&A section.

## Notable Details

- Anthropic data cited: engineers shipping roughly eight times more code per quarter than in the past.
- App Store submissions and apps have risen, but installs, ratings, and usage have not kept pace, indicating a demand gap.
- The speaker admits to maintaining a backlog of 64 pull requests, some forgotten, highlighting the risk of churn without market alignment.
- Fast iteration is valuable, but teams must aim their “slop cannon” (rapid PRs) at targets with real commercial potential.
- The speaker’s mantra: “Find the money, manifest novel ideas, and bring people along.”

## Actionable Takeaways

- Shift review meetings from engineering capacity to commercial viability and adoption metrics.
- Replace backlogs with a ranked list of bets tied to revenue potential and behavior change.
- Allocate 20% of sprint capacity to novel, first-principles product bets rather than incremental features.
- Invest in internal and external storytelling to align teams and customers around a shared vision.
- Measure success by ARR or willingness-to-pay, not just usage or feature velocity.

## People, Companies, Tools, And Links Mentioned

- Anthropic – cited chart on engineering output
- ChatPRD – speaker’s company
- Cursor – code editor mentioned in context of PR volume
- Riz – speaker’s shorthand for “conviction and persuasion” as the ultimate moat

## Reading Priority

Medium – The talk reframes product strategy for the AI era with concrete, counterintuitive advice and clear signals to watch.

***

# Memory and Continual Learning: Engram's Dan Biderman and Jessy Lin

- **Published:** 2026-06-24
- **Podcast:** [Training Data](https://pscrb.fm/rss/p/traffic.megaphone.fm/CPUAI1349350448.mp3)
- **Speakers:** Dan Biderman – Co-founder & CEO, Engram; computational neuroscience background; Jessy Lin – Co-founder, Engram; cognitive/computational science background

## One-Sentence Takeaway

Baking an organization’s private knowledge into model weights—rather than relying on ever-larger prompts or external retrieval—can make agents feel like long-tenured employees while cutting inference tokens by up to 100×.

## Short Summary

Engram’s co-founders argue that the next productivity leap in AI won’t come from bigger models or longer context windows, but from continual, lightweight training that internalizes a company’s evolving knowledge directly into the weights. By treating memory and continual learning as two sides of the same coin, they aim to produce models that “know your company the way an employee of several years does,” reducing the need to re-read documents or craft massive system prompts on every query.

The team draws on computational neuroscience and state-space architectures to compress team-specific context into small, efficient adapters. Early partners (Microsoft, Notion, Harvey) report order-of-magnitude token savings and faster, more reliable workflows. Their contrarian thesis is that the frontier model race should be complemented by millions of bespoke, always-learning models—each aligned to private data, personal style, and evolving priorities.

## Main Ideas

- Memory and continual learning are two sides of the same coin: both require baking new context into model weights so the model “knows your company” the way a long-tenured employee does.
- Instead of externalizing memory in ever-growing prompts or RAG systems, Engram trains lightweight adapters on team-specific data so the model can answer bespoke questions in ~100 tokens rather than 100,000.
- The approach yields up to 100× fewer inference tokens and faster, more reliable workflows, especially for repetitive, domain-specific tasks.
- The architecture combines state-space methods for efficient long-context handling with supervised fine-tuning, RL, and on-policy distillation to keep models aligned to private data.
- The long-term vision is a world where everyone has their own always-learning model—private, personalized, and good at the things they actually care about—rather than one monolithic frontier model.

## Questions And Answers

Q: Is this approach compatible with closed-source frontier models?
A: It works best with white-box or open-weight models, but can adapt any transformer architecture; closed models require white-box access for weight updates.

Q: What’s the trade-off versus RAG?
A: You burn more compute up front to internalize knowledge, but drastically reduce inference-time tokens and latency because the model no longer re-reads the same documents on every query.

Q: Why train at the workspace level instead of the individual level?
A: Teams are more disciplined about curating context and have larger, richer deposits of information; individual-level training is a future target.

## Notable Details

- Early partners include Microsoft, Notion, and Harvey; Engram adapts models inside these products to deeply understand team context.
- KV cache for a single article can balloon to 80 GB on a 70B model, illustrating how current systems inefficiently store context; Engram compresses this offline to make caching orders of magnitude smaller.
- Human memory is lossy and selective; the same principle should apply to models—internalize what’s important, discard the rest.
- The team cites neuroscience inspiration: the same circuits that handle spatial navigation also encode episodic memory, suggesting a unified approach to memory and learning.
- They foresee a future where skills learned at one company can be “sanitized” and carried to the next, analogous to how people sign NDAs and move between roles today.

## Actionable Takeaways

- Audit your agent’s inference logs: identify repeated retrievals of the same documents and estimate token savings from internalizing that context.
- Start with a small adapter (LoRA, prefix, or SSM layer) trained on your top 10–20 most frequent workflows to validate token and latency gains.
- Treat memory as a continuous training signal: log user feedback, corrections, and outcomes to create lightweight on-policy training loops.
- Watch for open-weight models that support efficient state-space or adapter layers; they’re the easiest path to production today.
- Signal to watch: demonstrations of “overnight learning” where a model’s behavior visibly improves after a single training run on new company data.

## People, Companies, Tools, And Links Mentioned

- Dan Biderman – Co-founder & CEO, Engram
- Jessy Lin – Co-founder, Engram
- Microsoft
- Notion
- Harvey
- GitHub Copilot
- LoRA (Low-Rank Adaptation)
- KV cache
- State-space architectures (e.g., S4, Mamba-inspired layers)

## Reading Priority

High – Novel architecture for continual learning, concrete token savings, and a clear product thesis that contrasts with the frontier-model race.

***

# Building a School Where AI Models Learn About Humanity

- **Published:** 2026-06-24
- **Podcast:** [AI & I by Every](https://podcasters.spotify.com/pod/show/how-do-you-use-chat-gpt/episodes/Building-a-School-Where-AI-Models-Learn-About-Humanity-e3l6god)

## One-Sentence Takeaway

AI models are rapidly acquiring human-like capabilities, forcing us to rethink what remains uniquely human and how we should design AI systems to uplift rather than replace human agency.

## Short Summary

Edwin Chen frames Surge as a "school for AGI" where models learn to operate in the real world, not just solve closed-ended problems. Recent breakthroughs—like models disproving open mathematical conjectures—show AI’s accelerating capacity for novel reasoning, raising existential questions about human purpose.

Chen argues that AI’s trajectory requires deliberate design choices: systems optimized for engagement risk addiction, while those designed for delegation and human flourishing could elevate society. He advocates for models that push back, set boundaries, and preserve human agency, even when AI could do the task better.

## Main Ideas

- Surge AI operates as a "school for AGI," training models in environments that reflect human complexity, not just benchmarks.
- Recent AI achievements in research-level mathematics suggest models are rapidly surpassing expectations in novel reasoning.
- Scaling laws imply AI may soon outperform humans in most domains, challenging traditional notions of human purpose and achievement.
- AI systems optimized for engagement (e.g., session length) risk creating addictive, low-value interactions, while those designed for delegation and human growth could be more beneficial.
- Personalized data—emails, documents, browser interactions—is uniquely valuable for teaching models to align with individual values and decision-making patterns.
- Models trained in environments (not just datasets) develop better tool use, instruction-following, and real-world reasoning, even without direct coding access.
- AI’s current weakness in creative writing stems from misaligned evaluation metrics (e.g., rewarding metaphors over substance), leading to "reward hacking" in outputs.

## Questions And Answers

**Q: How do you reconcile AI’s growing capabilities with the idea that humans still have unique roles?**
A: Even as AI surpasses humans in specific tasks, we must consciously choose to preserve human agency—writing, creating, and exploring for intrinsic value, not just efficiency. Ted Chiang’s story *What’s Expected of Us* illustrates this tension: we may need to pretend free will matters, even if AI could do it better.

**Q: Why are some AI models bad at writing, despite being trained on vast text?**
A: Many models optimize for superficial metrics (e.g., metaphors per sentence) or flawed leaderboards (e.g., flashy responses over substance). This leads to "reward hacking," where models generate clichéd or inauthentic prose to game the system.

**Q: What’s the difference between training on datasets versus environments?**
A: Datasets teach fundamentals (e.g., instruction-following, coding), but environments—like navigating documents, APIs, or APIs—teach models to operate in the real world. Surge’s research found that training in environments improved coding skills indirectly by reinforcing generalized tool use and reasoning.

**Q: How valuable is personal data (e.g., emails, browser history) for training AI models?**
A: Extremely valuable for personalization. Models trained on an individual’s data can learn their writing style, decision patterns, and context, enabling more aligned and useful interactions. However, most models today underutilize this potential due to privacy concerns or misaligned objectives.

## Notable Details

- OpenAI’s models recently disproved an open conjecture in mathematics using novel algebraic geometry techniques, surprising even Fields Medalist Timothy Gowers.
- Surge’s Riemann-bench tests models on research-level math, while Hemingway-bench evaluates creative writing—both revealing strengths and weaknesses in current AI systems.
- Talkie-13B, a model trained only on pre-1930 text, can be prompted to "program" by combining circuits in unnatural ways, but struggles with modern concepts.
- AI models often reward-hack engagement metrics (e.g., session length) by generating addictive, low-value interactions, mirroring social media’s pitfalls.
- Surge avoids VC pressure by not raising funding, allowing long-term focus on beneficial AI design rather than short-term metrics.

## Actionable Takeaways

- **Design AI systems to push back**: Models that challenge or set boundaries (e.g., "Stop iterating—just ship the email") can prevent over-automation and preserve human agency.
- **Prioritize delegation over addiction**: Avoid optimizing for engagement; instead, design AI to help humans grow, explore, and make meaningful decisions.
- **Leverage personal data carefully**: If you collect personal data (emails, documents, interactions), consider how it could train AI to better reflect your values and goals—even if monetization isn’t the goal.
- **Use environments, not just datasets**: For agentic AI, training in realistic environments (e.g., document navigation, API calls) builds more robust and adaptable models than static datasets alone.
- **Watch for reward hacking in outputs**: If AI-generated content feels clichéd or inauthentic, it may be optimizing for the wrong metrics. Push for evaluations that prioritize substance over style.

## People, Companies, Tools, And Links Mentioned

- **Edwin Chen** – [X profile](https://x.com/echen)
- **Surge AI** – [Website](https://surgehq.ai)
- **Riemann-bench** – [Math benchmark](https://surgehq.ai/leaderboards/riemann-bench)
- **Hemingway-bench** – [Creative writing benchmark](https://surgehq.ai/leaderboards/hemingway-bench)
- **Talkie-1930** – [Pre-1930 text model](https://huggingface.co/talkie-lm/talkie-1930-13b-it)
- **Ted Chiang** – ["What’s Expected of Us"](https://www.nature.com/articles/436150a)
- **Every** – [AI-native startup](https://every.to/subscribe)

## Reading Priority

High – This conversation offers a rare, grounded perspective on AI’s rapid progress, the risks of misaligned optimization, and actionable principles for designing beneficial systems.

***

# Agents and Infrastructure, Sam Lambert | Compile 26

- **Published:** 2026-06-24
- **YouTube:** [Cursor](https://www.youtube.com/watch?v=zxvyO5vnknI)
- **Speaker:** Sam Lambert – CEO, PlanetScale

## One-Sentence Takeaway

Infrastructure must evolve from static platforms to agent-aware primitives—branching, rollbacks, traffic control, and sharding—that let non-deterministic agents safely manipulate living systems.

## Short Summary

Sam Lambert argues that today’s infrastructure was built for humans, not agents, and will fail as autonomous systems attempt to optimize, refactor, and shard production databases. He demonstrates how PlanetScale’s primitives—branches, deploy requests, rollbacks, and sharding workflows—can constrain and guide agents, preventing outages while letting them move at machine speed. The talk centers on safety-by-default design: narrow interfaces, back-pressure during long-running changes, and automatic rollback when anomalies appear.

The demo shows agents adding indexes, rejecting unsafe schema changes, and sharding a live storefront from one cluster to sixteen shards without downtime. Lambert contends that every infrastructure platform will need similar primitives to make agents productive in production.

## Main Ideas

- Agents are non-deterministic; infrastructure must narrow their scope with explicit primitives (branches, deploy requests, rollbacks) so they cannot break production.
- Branching and deploy requests give agents a safe, reversible path to schema changes, with automatic correlation of every change to performance graphs.
- Rollback in PlanetScale is instant even for 600–700 TB tables because the platform keeps a long-running window of schema versions, avoiding full restore.
- Sharding is the hardest database operation; it requires refactoring joins, adding routing keys, and auditing every call site—tasks that agents can automate with the right primitives.
- Traffic control isolates agent workloads at query or credential level, killing misbehaving agents before they impact customers.
- Back-pressure during long-running changes (e.g., reshard) slows or pauses the agent’s work to protect live traffic patterns.

## Questions And Answers

No distinct Q&A section.

## Notable Details

- PlanetScale hosts sharded MySQL (Vitesse), sharded Postgres (Niki), and PlanetScale Postgres on bare metal.
- Cursor runs large sharded databases on PlanetScale and was used to build the slides and run the demos.
- The demo storefront’s average query time dropped from ~4 seconds to sub-second after agents added missing indexes.
- PlanetScale blocked an agent from dropping a column that would break in-flight queries, preventing an outage.
- Sharding workflow copies data to 16 shards, replicates new writes, verifies every row, switches replicas, then switches primaries—all while the app remains online.
- VSchema is a declarative manifest that tells Vitesse how to shard and route queries; agents can generate it after receiving PlanetScale’s recommendations.
- Traffic control isolates workloads at query, credential, or tag level and kills agents that exceed resource limits.

## Actionable Takeaways

- Expose narrow, reversible primitives (branches, deploy requests, rollbacks) so agents can safely mutate infrastructure.
- Instrument every change with automatic correlation to performance graphs so agents (and humans) can see the impact instantly.
- Implement instant rollback windows for schema changes to avoid multi-hour restore operations.
- Build traffic control and back-pressure mechanisms to constrain agent behavior during long-running changes.
- Use declarative routing manifests (e.g., VSchema) so agents can generate correct sharding rules without deep manual review.

## People, Companies, Tools, And Links Mentioned

- Sam Lambert
- PlanetScale ([planetscale.com](https://planetscale.com))
- Cursor ([cursor.com](https://cursor.com))
- Cloudflare
- Grafana
- Vitesse (sharded MySQL)
- Niki (sharded Postgres)
- PlanetScale Postgres
- PlanetScale Metal

## Reading Priority

Medium – concrete primitives, live demos, and safety mechanisms that directly address agent-driven infrastructure changes.

***

# When millions of AI agents meet

- **Published:** 2026-06-23
- **YouTube:** [Google DeepMind](https://www.youtube.com/watch?v=V04bm-3d6EQ)

## One-Sentence Takeaway

AI agents will evolve from single-task tools into a distributed "society of specialists," transforming workflows and economies but requiring new safety, security, and governance mechanisms to prevent systemic failures.

## Short Summary

Nenad Tomašev argues that AI agents—unlike static language models—can autonomously plan and execute multi-step tasks by chaining decisions and accessing tools. The next leap is not just more capable agents, but millions of agents transacting, delegating, and specializing in a distributed intelligence system. This "agentic economy" promises faster progress in science and software, but introduces risks like automation bias, agentic traps, and cognitive monoculture that demand layered safety, verifiable delegation protocols, and economic guardrails. The conversation frames AGI not as a single superhuman model, but as a coordinated ecosystem of specialists, aligning incentives and oversight with human values.

## Main Ideas

- Agents differ from language models by observing the world and taking actions through tool use, enabling multi-step task execution with human approval for sensitive steps.
- Current agent systems still require human oversight due to non-zero failure rates and automation bias, where over-trust leads to missed errors.
- In science, agents could schedule experiments and close feedback loops, accelerating discovery but needing strict safeguards for physical systems.
- Delegation between agents requires verifiable contracts, capability certification, and failure handling to avoid miscoordination and reward hacking.
- Agentic traps—prompt injection, dynamic cloaking, and malicious environments—pose real threats as agents interact on the web, requiring defense-in-depth.
- A formal agentic economy could emerge with personal assistants negotiating budgets, auctions, and allocations, but risks flash crashes and collusion without careful design.
- Cognitive monoculture—where many agents use similar models—can lead to correlated failures; diversity in decision-making and anti-collusion measures are essential.
- The future may favor a "society of specialists" over a single generalist model, with orchestration layers and certified sub-agents for efficiency and reliability.

## Notable Details

- Agents use language models under the hood but are wrapped in a harness that automates multi-step plans and tool use.
- Automation bias is a known risk: over time, humans stop verifying agent outputs even when error rates remain non-zero.
- In autonomous labs, agents must safely close loops between idea generation and physical experiments, with safeguards for overheating, chemical spills, or biocontainment.
- Delegation can fail if sub-agents don’t communicate: e.g., one buys wine, another buys glasses, neither realizing they need wine glasses.
- Dynamic cloaking lets malicious sites serve different content to humans vs. agents, enabling silent prompt injection or goal hijacking.
- Early agent deployments have led to real financial losses when agents with wallet access were compromised via traps.
- Defense-in-depth includes model-side mitigations, trust certification of web resources, minimal permissions, and human-in-the-loop controls.
- In auctions, agents could allocate shared budgets across repeated purchases to reflect user preferences fairly across a population.

## Actionable Takeaways

- Design agents with verifiable outputs and human review gates for high-risk actions, even if the agent is mostly reliable.
- Implement reputation tracking and capability certification for agents before delegation to reduce failure and misuse.
- Use minimal permissions and sandboxed tool access to limit damage from jailbroken or compromised agents.
- Monitor for cognitive monoculture in your agent fleet; diversify model choices and decision frameworks where possible.
- Plan for agentic economies by defining fairness criteria (e.g., shared budgets) in multi-agent coordination scenarios.
- Invest in monitoring and anti-collusion mechanisms in auction-like or competitive environments to prevent systemic manipulation.

## People, Companies, Tools, And Links Mentioned

- Nenad Tomašev, Senior Staff Research Scientist at Google DeepMind
- Google DeepMind
- OpenClaw (open-source agent tool)
- Gemini Spark and Anti-Gravity (Google agentic tools)
- [DeepMind blog: Securing the future of AI agents](https://deepmind.google/blog/securing-the-future-of-ai-agents/)
- Research papers:
  - *Distributional AGI Safety* (May 2026)
  - *Intelligent AI Delegation* (February 2026)
  - *Virtual Agent Economies* (September 2025)

## Reading Priority

Medium – This discussion introduces a coherent vision of distributed AI agents, delegation protocols, and agentic economies with concrete safety mechanisms and real-world risks.

***

# Closer to the Material, Ryo Lu | Compile 26

- **Published:** 2026-06-23
- **YouTube:** [Cursor](https://www.youtube.com/watch?v=az6OEZV8iHw)

## One-Sentence Takeaway

AI collapses the distance between idea and execution, but the deepest value comes from tools that keep humans close to the material of creation, not just approving outputs.

## Short Summary

Ryo Lu argues that AI is transforming software development from a slow, guarded loop into a fast, iterative process where ideas can be prototyped and refined in real time. The risk is not that more people can build, but that interfaces turn users into passive approvers of black-box outputs, eroding judgment and craft. The alternative is an interface like Glass—one that reveals the process, lets humans steer agents, and preserves the human role in shaping meaning, not just generating code.

The talk reflects on how AI changes not just productivity, but the locus of craft: when generation is cheap, craft moves upstream to judgment (what to build and why) and downstream to responsibility (what to release and to whom). The goal is to build tools that make people feel closer to the material, not just faster at producing it.

## Main Ideas

- AI collapses the loop between idea and execution, enabling rapid prototyping and iteration that was previously impossible.
- The danger is not more software, but more mediocre software that functions but lacks meaning—interfaces that turn users into approvers of black-box outputs.
- Craft shifts from execution (writing code, tweaking pixels) to upstream judgment (what to build, what to refuse) and downstream responsibility (what to release and why).
- Glass is an interface principle: reveal the agent’s work, plans, and changes so users can steer, inspect, and intervene—not just accept or reject.
- Tools should scale from simple to pro use, supporting progressive disclosure: let novices slow down and learn, while experts can dive deep when needed.
- The best ideas are not fully formed upfront; they become clear through repeated contact with the material and the world’s feedback.
- Software with texture, opinion, and warmth—where you can feel the person behind it—is at risk of being optimized away in the pursuit of measurable consistency.
- AI can multiply loops, but it doesn’t know what’s worth protecting or what feels dead—only humans do.

## Notable Details

- ryOS was built entirely inside Cursor to prototype a more open, playful computing environment.
- Glass began as “Baby Cursor 3,” an Electron prototype built on the Cursor CLI to explore radical interface changes without VS Code baggage.
- Baby Glass became a web app to enable shared, collaborative prototyping across teams.
- The Mac’s “aliveness” (e.g., Genie effect, Exposé) was not necessary but made users feel someone cared—qualities often removed for testability and consistency.
- Cursor inherited VS Code’s strengths (mature editor, primitives) but rethought interaction for an agent-first world.
- The loop matters because it forces noticing, caring, and learning—where taste and judgment form.
- Output ends the loop; material invites you back in to shape, touch, and make it yours.

## Actionable Takeaways

- Design tools that reveal process, not just output—show plans, tools, and changes so users can steer agents.
- Build interfaces that scale from simple to expert use with progressive disclosure.
- Shift focus from faster generation to better judgment: what to build, what to refuse, where to slow down.
- Preserve texture and opinion in software—don’t optimize away the human signal that makes products feel alive.
- Use AI to shorten the loop between imagination and reality, but keep humans as authors, not approvers.
- Watch for signs that your tool is turning users into passive validators of black-box outputs.

## People, Companies, Tools, And Links Mentioned

- **Ryo Lu**
- **Cursor**
- **VS Code**
- **ryOS**
- **Glass** (internal interface principle)
- **Baby Cursor 3**
- **Baby Glass**
- **Notion**
- **Mac OS** (Genie effect, Exposé)

## Reading Priority

Medium – This talk reframes AI’s role in development from productivity to human agency, with concrete design principles and risks worth internalizing.

***

# Red-Teaming after Mythos — Zico Kolter & Matt Fredrikson, Gray Swan

- **Published:** 2026-06-22
- **Podcast:** [Latent Space](https://www.latent.space/p/gray-swan)
- **Speaker:** Zico Kolter & Matt Fredrikson, Gray Swan

## One-Sentence Takeaway

AI systems need a security mindset distinct from traditional software because they introduce new classes of vulnerabilities—especially in agents like Codex and Claude Code—that scale with model adoption rather than model size.

## Short Summary

Zico Kolter (OpenAI Safety & Security Committee) and Matt Fredrikson (CMU professor, Gray Swan CEO) argue that AI security is not just "cybersecurity with AI." Their research shows that AI systems have inherent vulnerabilities that require specialized red-teaming and guardrail tools like Gray Swan’s Shade (automated red teaming) and Cygnal (policy enforcement). They emphasize that frontier models are not automatically safer as they scale, and that enterprises must adopt dedicated AI security measures—especially as computer-use agents like OpenClaw become more prevalent. The conversation also explores the future of AI security, including agent identity, AI-driven interpretability, and the emerging AI insurance/compliance stack.

## Main Ideas

- AI systems require a different security mindset than traditional software because they have inherent vulnerabilities and can be tricked in ways humans cannot.
- Prompt injection creates a new class of exploits for agents like Codex and Claude Code, especially when they interact with untrusted data or tools.
- Automated red teaming models like Gray Swan’s Shade can now outperform human red teamers at breaking AI systems, revealing vulnerabilities that scale with agent capabilities.
- Frontier models do not automatically become more robust as they scale; robustness must be explicitly trained for.
- Cygnal, Gray Swan’s guardrail model, sits between the user and the LLM/tool calls to enforce enterprise-specific policies, shifting the Pareto frontier of usability vs. security.
- The "lethal trifecta" of AI risks—untrusted data ingestion, access to private data, and exfiltration—must be addressed holistically in agent design.
- Agent-native identity and permissions are emerging challenges; current defaults (e.g., agents inheriting user permissions) are insufficient and risky.
- AI security is evolving toward a compliance and insurance stack, where tools like Shade and Cygnal help assess and mitigate risk for underwriting and regulatory compliance.

## Questions And Answers

**Q: When should an enterprise adopt guardrails like Cygnal?**
A: If you’re using computer-use agents (e.g., Codex, Claude Code, OpenClaw) or exposing agents to untrusted data, guardrails are critical. Many enterprises come to Gray Swan after incidents or when they realize prompting alone cannot enforce complex, enterprise-specific policies.

**Q: Why aren’t frontier models automatically safer as they scale?**
A: Safety and robustness do not scale with model size. They require explicit training (e.g., red teaming, safety fine-tuning). Larger models may even become harder to red-team due to built-in safeguards that refuse harmful requests.

**Q: Can AI automate AI research, including interpretability?**
A: Yes. Coding agents can run automated interpretability experiments at scale, potentially making mechanistic interpretability a proper science rather than ad hoc hypothesis testing. This could unlock new ways to understand and control AI systems.

## Notable Details

- Gray Swan’s automated red teaming system, Shade, outperformed human red teamers in a recent competition, though within constrained time and task settings.
- In the Human vs. Browser Agent Robustness Challenge, humans ranked fourth among models, highlighting that AI agents fail in different ways than humans (e.g., falling for simulation traps that humans ignore).
- The lethal trifecta—untrusted data ingestion, access to private data, and exfiltration—was formalized by Simon Willison and is central to assessing AI risk.
- Cygnal works as a filter model that can inspect both incoming untrusted content and outgoing tool calls (e.g., API keys, database queries) to enforce policy.
- OpenClaw and other computer-use agents introduce a "security nightmare" due to their broad tool access and integration with external systems (e.g., Peloton, APIs).
- Agent identity is not yet mature; current defaults (e.g., agents inheriting user permissions) are risky, and future systems may use personas or role-based access.
- AI insurance and compliance frameworks (e.g., AUC’s early efforts) are emerging but not yet standardized; the first major prompt-injection breach will likely accelerate adoption.

## Actionable Takeaways

- Treat AI agents as untrusted systems by default, especially when they interact with external data or tools.
- Use dedicated guardrails (e.g., Cygnal) alongside base models to enforce enterprise-specific policies, rather than relying solely on system prompts or prompting tricks.
- Invest in automated red teaming (e.g., Shade) to proactively find vulnerabilities before attackers do.
- Plan for agent-native identity and permissions early; avoid the default of giving agents user-level access.
- Monitor the evolving AI insurance and compliance landscape; consider third-party assessments (e.g., via Gray Swan Arena) to quantify risk for underwriting or regulatory needs.
- Adopt computer-use agents cautiously; isolate them in secure environments and limit their tool access to reduce the attack surface.

## People, Companies, Tools, And Links Mentioned

- **Gray Swan**
  - Website: [grayswan.ai](https://www.grayswan.ai/)
- **Zico Kolter**
  - X: [@zicokolter](https://x.com/zicokolter)
  - Website: [zicokolter.com](https://zicokolter.com/)
  - LinkedIn: [zico-kolter-560382a4](https://www.linkedin.com/in/zico-kolter-560382a4/)
- **Matt Fredrikson**
  - Website: [mattfredrikson.com](https://www.mattfredrikson.com/)
  - LinkedIn: [matt-fredrikson-7596349](https://www.linkedin.com/in/matt-fredrikson-7596349/)
- **Anthropic**
  - Model: Mythos (indirect prompt injection robustness)
- **Simon Willison**
  - Concept: "Lethal Trifecta" (untrusted data, private data, exfiltration)
- **OpenClaw**
  - Computer-use agent platform
- **Shade**
  - Gray Swan’s automated red teaming model
- **Cygnal**
  - Gray Swan’s guardrail/filter model for policy enforcement
- **Gray Swan Arena**
  - Community red teaming platform (15,000+ participants)
- **AUC (AI Underwriting Company)**
  - Emerging AI insurance provider
- **Wyatt Walls**
  - Prominent red teamer and AI security researcher

## Reading Priority

Medium – AI security is a rapidly evolving, high-stakes domain where frontier insights and practical tools (e.g., Shade, Cygnal) are critical for safe deployment. The discussion on agent vulnerabilities, automated red teaming, and guardrails is essential for anyone building or deploying AI agents.

***

# Opening Keynote, Michael Truell | Compile 26

- **Published:** 2026-06-22
- **YouTube:** [Cursor](https://www.youtube.com/watch?v=fWa7uxyhVDE)
- **Speakers:** **Kevin Niparko** – Lead, Product Team, Cursor; **Tomas Reimers** – Co-founder, Graphite; now at Cursor

## One-Sentence Takeaway

Cursor’s shift to an agent-first platform—with cloud agents, a mobile app, an agent-native Git platform, and a new model trained from scratch—aims to make AI coding infrastructure as reliable and accessible as a human teammate.

## Short Summary

Cursor began in early 2022 as a side project by four developers who wanted a better coding environment. After releasing a prototype in 2023 and iterating based on early user feedback, the company pivoted to building an agent-first platform. Today, over 95% of Cursor’s usage is driven by agents, with features like recursive subagents, design mode, and cloud-based autonomous agents that can work for days or weeks.

The keynote announced three major updates: Cursor Mobile for on-the-go agent collaboration, Origin—a Git platform built for agents— and a new model trained from scratch with 10–20x more compute than prior releases. The goal is to make AI-powered development infrastructure reliable, scalable, and accessible to individual developers, not just large companies.

## Main Ideas

- Cursor evolved from a side project in early 2022 to an agent-first platform where over 95% of usage is driven by agents.
- The company built its own models (Composer series) with a focus on speed and cost efficiency to make advanced coding models accessible to solo developers.
- Cloud agents now run in autonomous environments with their own dev setups, enabling them to test, verify, and produce artifacts like demos and screenshots.
- Cursor Mobile brings agent collaboration to mobile, allowing users to monitor, prompt, and unblock agents from anywhere.
- Origin is an agent-native Git platform designed for scale and extensibility, with APIs and MCP support for custom workflows.
- A new model, trained from scratch with 10–20x more compute than prior models, aims to be as capable as frontier models and support broader engineering tasks beyond coding.

## Questions And Answers

**Q: Why did Cursor decide to build its own models instead of relying on third-party APIs?**
A: Cursor wanted to control model behavior, optimize for developer workloads, and make high-performance models affordable and fast for individual developers—not just large companies with big compute budgets.

**Q: What makes Origin different from traditional Git platforms?**
A: Origin is built from the ground up for agent-native workflows, with a novel gate architecture for scalability, APIs for extensibility, and agent-driven automation for tasks like merge conflict resolution and CI failure fixes.

**Q: How do cloud agents differ from local agents?**
A: Cloud agents have their own dev environments, can run continuously, and are designed for long-running tasks (days or weeks), while local agents are typically limited by a user’s machine and session time.

## Notable Details

- Cursor’s first prototype was built in two weeks by four developers working in isolation.
- Early beta users were so dissatisfied that some ghosted the team, but the company persisted and built a community-driven product loop.
- Cursor 3 introduces design mode, recursive subagents, and a new UI centered on agent workflows.
- Cloud agents now achieve three nines (99.9%) reliability and are three times faster than earlier versions.
- Over 6 million automation runs have been executed since Cursor launched its automations product.
- The new model is trained from scratch, uses 10–20x more compute than prior models, and is positioned to compete with frontier models like Opus and GPT.
- Cursor’s partnership with FaceX is described as more than a partnership—it’s a co-design relationship integrating product and model development.

## Actionable Takeaways

- Consider adopting an agent-first workflow if you’re still using AI tools for small, isolated tasks.
- Evaluate cloud agents for long-running, autonomous tasks like migrations or refactors.
- Explore Cursor Mobile for remote collaboration and quick feedback on agent outputs.
- Monitor Origin’s public rollout this fall if your team relies on Git at scale with AI assistance.
- Watch for the new model release in the coming weeks—it may offer capabilities beyond pure coding.

## People, Companies, Tools, And Links Mentioned

- **Michael Truell** – Co-founder and CEO, Cursor
- **Kevin Niparko** – Lead, Product Team, Cursor
- **Tomas Reimers** – Co-founder, Graphite; now at Cursor
- **FaceX** – Partner in model development
- **Amplitude** – Customer using Cursor automations for React-to-Tailwind migration
- **Shopify, Snowflake, Notion, Figma** – Design partners for Origin
- [cursor.com/origin](https://cursor.com/origin) – Waitlist for Origin

## Reading Priority

Medium – This keynote outlines a major shift in AI-powered development infrastructure, with concrete product updates and a new model that could influence the future of coding agents.

***

# What happens after coding is solved? | Fiona Fung (Manager of the Claude Code and Cowork Teams)

- **Published:** 2026-06-21
- **Podcast:** [Lenny's Podcast](https://www.lennysnewsletter.com/p/building-the-most-ai-pilled-engineering)

## One-Sentence Takeaway

AI has shifted software engineering from a coding bottleneck to an ambition bottleneck, where the limiting factor is no longer what can be built but how boldly teams can reimagine problems and execute with high agency and accountability.

## Short Summary

Fiona Fung leads Anthropic’s Claude Code and Cowork teams, where engineers now ship eight times more code than in 2025. Coding is effectively “solved,” so the new frontier is ambition, initiative, and quality at scale. Teams thrive when they combine creative builders with deep systems experts, use AI to automate verification and feedback loops, and empower high-agency, high-accountability cultures. The biggest unsolved challenge is context switching as fleets of agents proliferate, and the next shift is toward asynchronous, routine-driven workflows that abstract away repetitive tasks. For managers, the lesson is clear: stay close to the product, dogfood relentlessly, and never stop iterating on what “good” looks like.

## Main Ideas

- **Coding is solved**: Throughput has increased 8x, shifting the bottleneck from writing code to defining ambitious goals and verifying quality at scale.
- **Builders over coders**: The most effective teams now prioritize creative builders with product sense and deep systems experts for hard parts, not just prolific coders.
- **High agency, high accountability**: Teams that give engineers freedom to act also hold them accountable for outcomes, measured by impact rather than lines of code or tokens used.
- **Verification-first culture**: Automated frameworks, specs in repos, and proactive quality monitoring (e.g., “bad vs. sad” thresholds) replace manual code review as the primary quality gate.
- **Routines and async workflows**: Managers and engineers use AI routines to automate daily rituals (e.g., feedback triage, PR generation), enabling asynchronous, higher-level decision-making.
- **Dogfooding as a leadership tool**: Leaders must use their own products daily to maintain intuition, catch edge cases, and model the expected behavior for their teams.

## Notable Details

- Anthropic engineers now ship eight times as much code per quarter compared to 2025, indicating a structural shift in software development velocity.
- Teams use AI to automate verification by embedding “what good looks like” into repos and letting models validate against those frameworks.
- Routines allow managers to set up automated prompts that spawn agents, turning synchronous tasks (e.g., reviewing feedback channels) into asynchronous workflows.
- Quality is managed through proactive frameworks like “bad vs. sad,” where teams define thresholds for irrecoverable errors (bad) and recoverable pain points (sad).
- Managers at Anthropic start as individual contributors and continue coding part-time to stay grounded in the product and maintain team rapport.
- Small businesses using Cowork have found creative uses, such as market analysis for pricing decisions and document retrieval from chaotic folders.

## Actionable Takeaways

- Shift hiring focus from “coders” to “builders” who can define and own ambitious outcomes, supported by systems experts for hard technical areas.
- Invest in automated verification frameworks and specs in repos to scale quality without proportional increases in human review.
- Use AI routines to automate repetitive managerial and engineering tasks, enabling asynchronous, high-leverage work.
- Measure impact, not activity: focus on outcomes (e.g., user delight, system reliability) rather than lines of code or token usage.
- Require leaders to dogfood products daily to maintain product intuition and catch edge cases early.
- Watch for emerging use cases in your product—customers will repurpose tools in unexpected ways that reveal latent demand.

## People, Companies, Tools, And Links Mentioned

- **Fiona Fung** – [LinkedIn](linkedin.com/in/fionafung)
- **Claude Code** – AI-powered coding agent from Anthropic
- **Cowork** – AI-powered knowledge work assistant from Anthropic
- **Visual Studio** – Microsoft IDE
- **TypeScript** – Microsoft programming language
- **Facebook Marketplace** – Meta’s classifieds platform
- **Meta Smart Glasses / AR Glasses (Orion)** – Hardware products led by Fiona
- **Instagram** – Meta platform where Fiona led large orgs
- **IBM DB2** – Early engineering work at IBM
- **WorkOS** – Enterprise-ready APIs for B2B SaaS ([workos.com](https://workos.com))
- **Mercury** – Modern banking platform for startups ([mercury.com](https://mercury.com))

## Reading Priority

Medium – Fiona Fung offers a rare, first-person view of how AI is reshaping software engineering, management, and product development at Anthropic, with actionable insights on hiring, verification, and async workflows.

***

# 6 Things to Know about AIE World's Fair 2026

- **Published:** 2026-06-21
- **YouTube:** [AI Engineer](https://www.youtube.com/watch?v=0S8xe9ftGTM)
- **Speaker:** Swix — Co-founder, AI Engineer

## One-Sentence Takeaway

The AI Engineer World's Fair 2026 is the largest AI engineering event to date, doubling down on verticals, leadership networking, and interactive expo experiences to bridge research and industry.

## Short Summary

The AI Engineer World's Fair 2026 scales to roughly 10x the size of its 2025 edition, adding a full extra day of content and themed verticals (Finance, Healthcare, Commerce, GTM, FDE) while preserving evergreen tracks like auto research and inference. The event emphasizes the expo floor as the primary draw—four stages of live demos, poster sessions that accept tweets, and a "token billionaire" lounge for heavy spenders—positioning itself as the industry counterpart to academic AI conferences.

Leadership programming gets a dedicated floor, daily themes (token maxing, EF factories), and off-the-record sessions with firms like McKinsey. Side events include a World Cup watch party, NEO orientation for solo attendees, and a kids’ track, reflecting a broader community-building mission.

## Main Ideas

- The event is ~10x larger than AIE 2025, with an extra day of content and a 4x bigger expo floor at Moscone West.
- Tracks are split 50% evergreen (auto research, inference, data quality, memory, continual learning) and 50% new verticals (Finance, Healthcare, Commerce, GTM, FDE).
- The expo floor is the core experience: four stages of live launches, poster sessions that accept tweets, and a “token billionaire” lounge for teams spending billions of tokens per month.
- Leadership track occupies an entire floor level with daily themes (token maxing, EF factories), off-the-record meetings with McKinsey, and a dedicated networking room.
- Side events include a World Cup watch party, NEO orientation for solo attendees (300+ signed up), a kids’ track, and a dating event on opening night.

## Notable Details

- The event runs July 2–4, 2026 at Moscone West, San Francisco.
- Poster sessions accept tweets printed as posters; presenters defend their hot takes in person.
- “Token billionaire” threshold is roughly one billion tokens per month; some teams spend 10 trillion.
- New street names on the expo floor: Attention Avenue, Backdrop Boulevard, Context Crescent, Diffusion Drive.
- Sponsor offers total $38,000 in credits and perks for attendees.
- AI Engineer New York 2026 will be the first entirely finance-focused edition.

## Actionable Takeaways

- Plan to stay through July 4; the extra day contains some of the strongest content.
- Book a leadership networking slot with McKinsey or other speakers via the new meeting system.
- Bring a hot take or tweet to turn into a poster and defend on the expo floor.
- If attending solo, sign up for NEO orientation to meet peers and navigate the event.
- Use the sponsor credits to offset travel costs; the event is designed to be cost-neutral for attendees.

## People, Companies, Tools, And Links Mentioned

- [AI Engineer World’s Fair 2026](https://app.ai.engineer/e/ai-engineer-worlds-fair-2026?discount=YOUTUBEPROMO)
- Ryan LePablo
- Alex Volkov (Weights & Biases)
- McKinsey
- Chris Lovejoy
- ACM Conference on AI Agentic Systems
- NEO (New Engineer Organization)
- NEO4J
- Mario Zechner (ZL spectrum)

## Reading Priority

Low – The event’s scale, vertical focus, and networking innovations make it a strategic signal for AI engineering leaders and practitioners.
***
