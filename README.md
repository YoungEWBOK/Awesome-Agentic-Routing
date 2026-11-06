# Awesome Agentic Routing

A curated reading list on choosing **which model or agent should act next**, under evolving task state, quality requirements, and resource constraints.

[中文阅读路线](READING_GUIDE.zh-CN.md) · [Recent arXiv candidates](RECENT.md) · [Contributing and update policy](CONTRIBUTING.md) · [Machine-readable catalog](data/curated.json)

Maintained by [YoungEWBOK](https://github.com/YoungEWBOK). Initial collection: **2023–2026**. Last editorial review: **2026-11-06**. **20 selected papers.**

## Scope

The core is routing **during** agent execution: selecting models, agents, or intelligent tools as the interaction changes. We also include the routing/cascading foundations and evaluation work needed to understand it. Model-internal MoE routing, network/PCB routing, and generic agent frameworks without a routing contribution are outside the main scope.

| Decision | What changes? | Starting points |
| --- | --- | --- |
| Query routing | The model answering one input | RouteLLM, GraphRouter |
| Cascading | Whether to stop or escalate after an answer | FrugalGPT |
| Sequential routing | The next model, given history and budget | BAAR, MTRouter, DialRouter |
| Orchestration | Calls, roles, subtasks, and their dependencies | Router-R1, MasRouter, ToolOrchestra, E³-Orch |
| Evaluation | Whether a local replacement preserves final success | TwinRouterBench |

These are reading categories, not mutually exclusive definitions. User dialogue turns, internal model calls, and environment interaction steps must be distinguished.

## Start here

1. **Dynamic Model Routing and Cascading** — read the design space and evaluation sections.
2. **RouteLLM + FrugalGPT** — compare deciding before versus after generation.
3. **BAAR + MTRouter** — understand path dependence, budgets, and outcome prediction.
4. **SkillOrchestra** — compare explicit capability knowledge with learned routing policies.
5. **TwinRouterBench** — examine static labels versus live downstream execution.
6. **Router-R1 → ToolOrchestra → E³-Orch** — expand into learned orchestration.

## How to read this list

Selection reflects problem relevance, conceptual value, and inspectable evidence, not a numerical ranking or a guarantee of reproducibility. Each entry explains its contribution and a question worth checking. Initial review depth is metadata/abstract plus selected method sections; these are not reproduction reports.

**Publication labels:** explicit venues are backed by a linked publication source or attributed to the authors' arXiv notice. **arXiv version** means we cite that version and have not independently established a publication venue; it does not assert the work has never been peer reviewed. Dates are first-release years, which may differ from venue years.

## Surveys

### Doing More with Less

**[Doing More with Less: A Survey on Routing Strategies for Resource Optimisation in Large Language Model-Based Systems](https://arxiv.org/abs/2502.00409)**

Clovis Varangot-Reille et al. · 2025 · arXiv version; venue not independently verified

- **Why read:** Frames routing as resource-aware model selection and organizes similarity, supervised, reinforcement-learning, and generative approaches.
- **Read critically:** Which objectives and generation-time information does each family assume?

### Dynamic Model Routing and Cascading

**[Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey](https://arxiv.org/abs/2603.04445)**

Yasmin Moslem et al. · 2026 · [TMLR 2026 (author-reported acceptance)](https://arxiv.org/abs/2603.04445)

- **Why read:** Provides a useful design space: when a decision happens, what it observes, and how it is computed; includes evaluation failure modes.
- **Read critically:** Does an apparent improvement survive differences in model pools, cost definitions, and evaluation protocols?

## Foundations: model selection and cascading

### FrugalGPT

**[FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance](https://arxiv.org/abs/2305.05176)**

Lingjiao Chen et al. · 2023 · arXiv version; venue not independently verified

- **Why read:** A foundational model-cascade approach: decide when an answer is sufficient and when another model is worth its cost.
- **Read critically:** Account for earlier calls and the answer scorer; escalation is not free.

### RouteLLM

**[RouteLLM: Learning to Route LLMs with Preference Data](https://arxiv.org/abs/2406.18665)**

Isaac Ong et al. · 2024 · [ICLR 2025](https://openreview.net/pdf/900c2f5b71fd9d4dc34d8f299cce9a11336d30b4.pdf)

- **Why read:** Learns strong-versus-weak model routing from preference data; a clear entry point into routing supervision and transfer.
- **Read critically:** Does preference-based single-query selection remain appropriate when intermediate outputs affect later steps?

### GraphRouter

**[GraphRouter: A Graph-based Router for LLM Selections](https://arxiv.org/abs/2410.03834)**

Tao Feng et al. · 2024 · arXiv version; venue not independently verified

- **Why read:** Represents tasks, queries, and models in a heterogeneous graph, supporting inductive model selection.
- **Read critically:** What observations are required to introduce a new model? Query-level induction alone does not establish trajectory-level transfer.

## Sequential and budget-aware agentic routing

### BAAR

**[Budget-Aware Agentic Routing via Boundary-Guided Training](https://arxiv.org/abs/2602.21227)**

Caiqi Zhang et al. · 2026 · arXiv version; venue not independently verified

- **Why read:** Studies step-wise small/large model selection with path dependence, sparse terminal rewards, and explicit task budgets.
- **Read critically:** Separate soft cost penalties from hard inference budgets, and inspect the two-model setting.

### MTRouter

**[MTRouter: Cost-Aware Multi-Turn LLM Routing with History-Model Joint Embeddings](https://arxiv.org/abs/2604.23530)**

Yiqun Zhang et al. · 2026 · [ACL 2026](https://aclanthology.org/2026.acl-long.2045/)

- **Why read:** Jointly embeds interaction history and candidate models, learning outcome estimates from logged multi-turn trajectories.
- **Read critically:** How much alternative-model coverage exists at the same state? Outcome regression is not automatically a counterfactual value estimate.

### DialRouter

**[From Myopic Selection to Long-Horizon Awareness: Sequential LLM Routing for Multi-Turn Dialogue](https://arxiv.org/abs/2604.12385)**

Jiarui Zhang et al. · 2026 · arXiv version; venue not independently verified

- **Why read:** Uses dialogue-tree search to learn routing with long-horizon awareness and retrieval-based future-state approximation.
- **Read critically:** These are user-dialogue turns: examine the user simulator and reward model before extending conclusions to tool execution.

### ProgRouter

**[ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs](https://arxiv.org/abs/2608.25992)**

Songyuan Li et al. · 2026 · [Findings of EMNLP 2026 (author-reported acceptance)](https://arxiv.org/abs/2608.25992)

- **Why read:** Predicts task progress to guide online model choices under quality, time, and operating-cost considerations.
- **Read critically:** What validates the progress signal? Online decision-making should not be confused with online policy training.

## Multi-model and multi-agent orchestration

### Router-R1

**[Router-R1: Teaching LLMs Multi-Round Routing and Aggregation via Reinforcement Learning](https://arxiv.org/abs/2506.09033)**

Haozhen Zhang et al. · 2025 · [NeurIPS 2025 (author-reported acceptance)](https://arxiv.org/abs/2506.09033)

- **Why read:** Trains an LLM to interleave reasoning, external model calls, and answer aggregation using outcome and cost rewards.
- **Read critically:** Multi-round refers to internal calls; inspect router overhead, stopping, and the information supplied about models.

### xRouter

**[xRouter: Training Cost-Aware LLMs Orchestration System via Reinforcement Learning](https://arxiv.org/abs/2510.08439)**

Cheng Qian et al. · 2025 · arXiv version; venue not independently verified

- **Why read:** Treats external models as callable tools and trains a router to answer directly or invoke them with cost-aware reinforcement learning.
- **Read critically:** Which orchestration behaviors actually emerge, and which depend on router capacity and training data?

### ToolOrchestra

**[ToolOrchestra: Elevating Intelligence via Efficient Model and Tool Orchestration](https://arxiv.org/abs/2511.21689)**

Hongjin Su et al. · 2025 · arXiv version; venue not independently verified

- **Why read:** Extends learned orchestration to a mix of general models, specialized models, and ordinary tools.
- **Read critically:** Separate gains from the orchestration policy, available tools, model pool, and training resources.

### MasRouter

**[MasRouter: Learning to Route LLMs for Multi-Agent Systems](https://aclanthology.org/2025.acl-long.757/)**

Yanwei Yue et al. · 2025 · [ACL 2025](https://aclanthology.org/2025.acl-long.757/)

- **Why read:** Jointly considers collaboration mode, agent roles, and LLM assignment through a cascaded controller.
- **Read critically:** Distinguish constructing a multi-agent system from repeatedly rerouting after environment feedback.

### E³-Orch

**[E$^3$-Orch: Towards Effective, Efficient, and Extensible Agentic Orchestration with Reinforcement Learning](https://arxiv.org/abs/2608.04588)**

Junnan Liu et al. · 2026 · arXiv version; venue not independently verified

- **Why read:** Uses milestone-plan-act orchestration and execution feedback for dependency-aware delegation and parallel execution.
- **Read critically:** Inspect credit assignment, executor descriptions, and transfer to unseen executor configurations; the authors mark it work in progress.

## Capability representation and experience

### SkillOrchestra

**[SkillOrchestra: Learning to Route Agents via Skill Transfer](https://arxiv.org/abs/2602.19672)**

Jiayu Wang et al. · 2026 · arXiv version; venue not independently verified

- **Why read:** Builds a reusable skill handbook from experience, representing skill demand, agent competence, and execution cost explicitly.
- **Read critically:** How are skill profiles supported by trajectories, and how robust are they to new tasks or changed agents?

### RSI-Router

**[RSI-Router: Evolving Subtask-Level LLM Routing and Skills for Cost-Efficient Agents](https://arxiv.org/abs/2609.34712)**

Hao Li et al. · 2026 · arXiv version; venue not independently verified

- **Why read:** Evolves subtask-level model assignments together with model-specific skills from accumulated execution experience.
- **Read critically:** Disentangle routing improvements from improvements to worker skills and prompts.

### Harness-Native Agentic Routing

**[Agentic Routing: The Harness-Native Data Flywheel](https://arxiv.org/abs/2607.11399)**

Xinchen Liu et al. · 2026 · arXiv version; venue not independently verified

- **Why read:** Connects routing to execution state and environment feedback, with traces reused for subsequent routing and model learning.
- **Read critically:** Treat the data-flywheel argument as a research hypothesis to inspect; compare concrete evidence with the broader systems vision.

## Benchmarks and evaluation

### RouterBench

**[RouterBench: A Benchmark for Multi-LLM Routing System](https://arxiv.org/abs/2403.12031)**

Qitian Jason Hu et al. · 2024 · arXiv version; venue not independently verified

- **Why read:** Provides reusable inference outcomes and a framework for comparing multi-model routing quality and cost.
- **Read critically:** Static per-query outcomes do not directly show whether intermediate model replacement preserves downstream success.

### LLMRouterBench

**[LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing](https://arxiv.org/abs/2601.07206)**

Hao Li et al. · 2026 · arXiv version; venue not independently verified

- **Why read:** Re-examines routing methods with a large shared model/task pool and analyses of complementarity and the oracle gap.
- **Read critically:** Inspect simple comparison methods and model-pool selection before attributing gains to router complexity.

### TwinRouterBench

**[TwinRouterBench: Fast Static and Live Dynamic Evaluation for Realistic Agentic LLM Routing](https://arxiv.org/abs/2605.18859)**

Pei Yang et al. · 2026 · arXiv version; venue not independently verified

- **Why read:** Combines static intermediate-prefix routing evaluation with live agent execution for downstream validation.
- **Read critically:** Inspect label-construction protocols and the size and separation of the live evaluation split.

## Biweekly arXiv discovery

[The workflow](.github/workflows/arxiv-update.yml) checks on Fridays at **09:17 Asia/Shanghai (01:17 UTC)** and searches when at least 14 local calendar days have elapsed since the previous successful search. It can also be run manually from Actions. The first scheduled search after initialization on 2026-11-06 is expected on **2026-11-20**. GitHub may delay scheduled jobs.

New matching papers are published to [RECENT.md](RECENT.md), with version-aware deduplication and a seven-day discovery overlap. Existing candidates are refreshed for revisions. The curated list is edited after reading; the automation does not certify scientific quality or promote candidates automatically. It uses the public arXiv API and GitHub's built-in workflow token, with no paid model API or extra secret required.

A successful search updates its date even when it finds no new candidates. Failed or incomplete searches leave the last successful date unchanged. See [maintenance instructions](CONTRIBUTING.md) for limitations and recovery.
