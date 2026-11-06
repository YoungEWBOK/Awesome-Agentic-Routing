# Awesome Agentic Routing

Research on model selection, LLM routing, cascades, and agent orchestration.

[中文阅读指南](READING_GUIDE.zh-CN.md) · [Code and other resources](docs/resources.md) · [Recent arXiv papers](RECENT.md) · [Contributing](CONTRIBUTING.md)

30 papers · 2023–2026 · Updated 2026-11-06

## Contents

- [Surveys](#surveys)
- [Query routing: quality and cost prediction](#query-routing-quality-and-cost-prediction)
- [Query routing: representations and transfer](#query-routing-representations-and-transfer)
- [Cascading and response verification](#cascading-and-response-verification)
- [Sequential and budget-aware routing](#sequential-and-budget-aware-routing)
- [Model and agent orchestration](#model-and-agent-orchestration)
- [Benchmarks and evaluation](#benchmarks-and-evaluation)
- [Software and infrastructure](#software-and-infrastructure)

## Scope and notation

The list covers routing across independent models and agents, from single-query selection to decisions within multi-step tasks. Papers are grouped by their main decision setting; a method may also be relevant to other sections.

**Venue** links to the publication record when available. **†** indicates acceptance reported by the authors. **arXiv** identifies the manuscript version when no venue is recorded here. **Code** links to author implementations; **—** means no public implementation was located in the checked sources. Dates refer to the linked records, not necessarily the first preprint.

## Surveys

Surveys of model selection, cascading, and inference efficiency.

| Paper | Venue | Method / setting | Code |
| --- | --- | --- | --- |
| **Dynamic Model Routing and Cascading**<br>[Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey](https://arxiv.org/abs/2603.04445) | [TMLR 2026 †](https://arxiv.org/abs/2603.04445) | Decision timing, information, and learning paradigms<br><sub>Multi-LLM inference</sub> | — |
| **Doing More with Less**<br>[Doing More with Less: A Survey on Routing Strategies for Resource Optimisation in Large Language Model-Based Systems](https://arxiv.org/abs/2502.00409) | [JAIR 2026](https://doi.org/10.1613/jair.1.19801) | Routing taxonomy; resource objectives<br><sub>LLM-based systems</sub> | — |
| **Efficient Multi-LLM Inference Survey**<br>[Towards Efficient Multi-LLM Inference: Characterization and Analysis of LLM Routing and Hierarchical Techniques](https://arxiv.org/abs/2506.06579) | arXiv 2025 | Routing and hierarchical inference<br><sub>Resource-constrained inference</sub> | — |

## Query routing: quality and cost prediction

The router selects a model before response generation, using predicted quality, cost, or latency.

| Paper | Venue | Method / setting | Code |
| --- | --- | --- | --- |
| **CARROT**<br>[CARROT: A Cost Aware Rate Optimal Router](https://arxiv.org/abs/2502.03261) | [ICLR 2025 Workshop: FM-Wild](https://openreview.net/pdf/52c8d7de010331caa34d891ce83ffd12f8b5ada0.pdf) | Joint cost/quality estimation; minimax analysis<br><sub>Single-query routing</sub> | [GitHub](https://github.com/somerstep/CARROT) |
| **MixLLM**<br>[MixLLM: Dynamic Routing in Mixed Large Language Models](https://arxiv.org/abs/2502.18482) | [NAACL 2025](https://aclanthology.org/2025.naacl-long.545/) | Contextual bandits with quality/cost prediction<br><sub>Online query streams</sub> | — |
| **Hybrid LLM**<br>[Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing](https://arxiv.org/abs/2404.14618) | [ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/b47d93c99fa22ac0b377578af0a1f63a-Abstract-Conference.html) | Difficulty prediction with a quality-tolerance threshold<br><sub>Single-query text generation</sub> | — |
| **RouteLLM**<br>[RouteLLM: Learning to Route LLMs with Preference Data](https://arxiv.org/abs/2406.18665) | [ICLR 2025](https://openreview.net/pdf/900c2f5b71fd9d4dc34d8f299cce9a11336d30b4.pdf) | Preference-supervised strong/weak model selection<br><sub>Single-query text generation</sub> | [GitHub](https://github.com/lm-sys/RouteLLM) |

## Query routing: representations and transfer

These methods study query-model compatibility, capability profiles, or adaptation to new candidate models.

| Paper | Venue | Method / setting | Code |
| --- | --- | --- | --- |
| **RouteFM**<br>[Pretrain Once, Route Anywhere: Towards a Foundation Model for LLM Routing](https://arxiv.org/abs/2609.37362) | arXiv 2026 | Episodic pretraining over candidate behavioral context<br><sub>Cross-task, cross-pool, and multimodal transfer</sub> | [GitHub](https://github.com/LAMDA-Model-Reuse/RouteFM) |
| **RouteProfile**<br>[RouteProfile: Graph-Based Profiling for Cold-Start LLM Routing](https://arxiv.org/abs/2605.00180) | arXiv 2026 | Graph-based integration of public model profiles<br><sub>Cold start; new-model integration</sub> | [GitHub](https://github.com/ulab-uiuc/RouteProfile) |
| **LLMRec**<br>[Let the LLM Stick to Its Strengths: Learning to Route Economical LLM](https://proceedings.neurips.cc/paper_files/paper/2025/hash/305a5630c29aaca434e3415fc4638eb2-Abstract-Conference.html) | [NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/305a5630c29aaca434e3415fc4638eb2-Abstract-Conference.html) | Recommendation model with capability and context features<br><sub>Single-query routing; new tasks/models</sub> | — |
| **GraphRouter**<br>[GraphRouter: A Graph-based Router for LLM Selections](https://arxiv.org/abs/2410.03834) | [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/41b6674c28a9b93ec8d22a53ca25bc3b-Abstract-Conference.html) | Task-query-model graph; utility and cost edge prediction<br><sub>Single-query routing; new models</sub> | [GitHub](https://github.com/ulab-uiuc/GraphRouter) |
| **RouterDC**<br>[RouterDC: Query-Based Router by Dual Contrastive Learning for Assembling Large Language Models](https://arxiv.org/abs/2409.19886) | [NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/7a641b8ec86162fc875fb9f6456a542f-Abstract-Conference.html) | Query/model embeddings with dual contrastive losses<br><sub>Single-query routing; distribution shift</sub> | [GitHub](https://github.com/shuhao02/RouterDC) |

## Cascading and response verification

The policy observes an answer or confidence signal before deciding whether to stop or call another model.

| Paper | Venue | Method / setting | Code |
| --- | --- | --- | --- |
| **AutoMix**<br>[AutoMix: Automatically Mixing Language Models](https://arxiv.org/abs/2310.12963) | [NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/ecda225cb187b40ea8edc1f46b03ffda-Abstract-Conference.html) | Self-verification with a POMDP escalation policy<br><sub>Context-grounded question answering</sub> | [GitHub](https://github.com/automix-llm/automix) |
| **FrugalGPT**<br>[FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance](https://arxiv.org/abs/2305.05176) | [TMLR 2024](https://openreview.net/forum?id=cSimKw5p6R) | Learned model cascades with answer scoring<br><sub>Query answering and text tasks</sub> | [GitHub](https://github.com/stanford-futuredata/FrugalGPT) |

## Sequential and budget-aware routing

Model choices are made during a dialogue or task trajectory. Previous outputs and remaining resources affect later decisions.

| Paper | Venue | Method / setting | Code |
| --- | --- | --- | --- |
| **BAAR**<br>[Budget-Aware Agentic Routing via Boundary-Guided Training](https://arxiv.org/abs/2602.21227) | arXiv 2026 | Boundary-guided SFT and policy optimization<br><sub>Long-horizon interactive tasks</sub> | — |
| **DialRouter**<br>[From Myopic Selection to Long-Horizon Awareness: Sequential LLM Routing for Multi-Turn Dialogue](https://arxiv.org/abs/2604.12385) | arXiv 2026 | MCTS supervision; retrieved future-state approximation<br><sub>Multi-turn user dialogue</sub> | — |
| **MTRouter**<br>[MTRouter: Cost-Aware Multi-Turn LLM Routing with History-Model Joint Embeddings](https://arxiv.org/abs/2604.23530) | [ACL 2026](https://aclanthology.org/2026.acl-long.2045/) | History-model embeddings with an outcome estimator<br><sub>ScienceWorld; tool-assisted HLE</sub> | [GitHub](https://github.com/ZhangYiqun018/MTRouter) |
| **ProgRouter**<br>[ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs](https://arxiv.org/abs/2608.25992) | [Findings of EMNLP 2026 †](https://arxiv.org/abs/2608.25992) | Progress prediction with online model allocation<br><sub>Code, math, and long-form QA workflows</sub> | — |

## Model and agent orchestration

The controller chooses model or tool calls, agent roles, or subtask assignments. The action space varies across papers.

| Paper | Venue | Method / setting | Code |
| --- | --- | --- | --- |
| **E³-Orch**<br>[E³-Orch: Towards Effective, Efficient, and Extensible Agentic Orchestration with Reinforcement Learning](https://arxiv.org/abs/2608.04588) | arXiv 2026 | Milestone-plan-act RL with tree-structured rollouts<br><sub>Multi-agent task decomposition and execution</sub> | — |
| **Harness-Native Agentic Routing**<br>[Agentic Routing: The Harness-Native Data Flywheel](https://arxiv.org/abs/2607.11399) | arXiv 2026 | Harness-state routing with reusable execution records<br><sub>Agent execution; singleton and ensemble routing</sub> | [GitHub](https://github.com/TokenRhythm/opensquilla) |
| **RSI-Router**<br>[RSI-Router: Evolving Subtask-Level LLM Routing and Skills for Cost-Efficient Agents](https://arxiv.org/abs/2609.34712) | arXiv 2026 | Joint evolution of subtask routing and worker skills<br><sub>Interactive and coding agents</sub> | — |
| **SkillOrchestra**<br>[SkillOrchestra: Learning to Route Agents via Skill Transfer](https://arxiv.org/abs/2602.19672) | arXiv 2026 | Skill handbook with agent competence and cost profiles<br><sub>Model routing and tool-using agents</sub> | [GitHub](https://github.com/jiayuww/SkillOrchestra) |
| **MasRouter**<br>[MasRouter: Learning to Route LLMs for Multi-Agent Systems](https://aclanthology.org/2025.acl-long.757/) | [ACL 2025](https://aclanthology.org/2025.acl-long.757/) | Cascaded controllers for collaboration, roles, and models<br><sub>Multi-agent code and reasoning tasks</sub> | [GitHub](https://github.com/yanweiyue/masrouter) |
| **Router-R1**<br>[Router-R1: Teaching LLMs Multi-Round Routing and Aggregation via Reinforcement Learning](https://arxiv.org/abs/2506.09033) | [NeurIPS 2025 †](https://arxiv.org/abs/2506.09033) | RL over reasoning, model calls, and answer aggregation<br><sub>General and multi-hop QA</sub> | [GitHub](https://github.com/ulab-uiuc/Router-R1) |
| **ToolOrchestra**<br>[ToolOrchestra: Elevating Intelligence via Efficient Model and Tool Orchestration](https://arxiv.org/abs/2511.21689) | arXiv 2025 | RL over model and tool calls<br><sub>HLE; tau2-Bench; FRAMES</sub> | [GitHub](https://github.com/NVlabs/ToolOrchestra) |
| **xRouter**<br>[xRouter: Training Cost-Aware LLMs Orchestration System via Reinforcement Learning](https://arxiv.org/abs/2510.08439) | arXiv 2025 | Cost-aware RL with external models as tools<br><sub>Multi-model task solving</sub> | [GitHub](https://github.com/SalesforceAIResearch/xRouter) |

## Benchmarks and evaluation

Evaluation resources for query-level selection and routing within agent trajectories.

| Paper | Venue | Method / setting | Code |
| --- | --- | --- | --- |
| **LLMRouterBench**<br>[LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing](https://arxiv.org/abs/2601.07206) | [Findings of ACL 2026](https://aclanthology.org/2026.findings-acl.1881/) | Shared task/model pool and unified router comparison<br><sub>Text, reasoning, code, and tool-use tasks</sub> | [GitHub](https://github.com/ynulihao/LLMRouterBench) |
| **TwinRouterBench**<br>[TwinRouterBench: Fast Static and Live Dynamic Evaluation for Realistic Agentic LLM Routing](https://arxiv.org/abs/2605.18859) | arXiv 2026 | Static intermediate prefixes and live agent execution<br><sub>Step-level routing; coding agents</sub> | [GitHub](https://github.com/CommonstackAI/TwinRouterBench) |
| **RouterBench**<br>[RouterBench: A Benchmark for Multi-LLM Routing System](https://arxiv.org/abs/2403.12031) | arXiv 2024 | Precomputed model outcomes and routing evaluation<br><sub>Single-query multi-model routing</sub> | [GitHub](https://github.com/withmartian/routerbench) |

## Software and infrastructure

Shared implementations and evaluation pipelines for routing research.

| Paper | Venue | Method / setting | Code |
| --- | --- | --- | --- |
| **LLMRouter**<br>[LLMRouter: Unified Infrastructure for Developing, Evaluating, and Deploying LLM Routers](https://arxiv.org/abs/2608.06867) | arXiv 2026 | Modular routing components and xRouteBench<br><sub>Single-turn, multi-turn, and personalized routing</sub> | [GitHub](https://github.com/ulab-uiuc/LLMRouter) |

## Reading and updates

The [Chinese reading guide](READING_GUIDE.zh-CN.md) compares problem formulations, supervision, and evaluation. [Resource notes](docs/resources.md) include code provenance and available data, models, and project pages.

[Recent arXiv papers](RECENT.md) are collected every two weeks. This feed is screened by keywords and kept separate from the main list; code links and publication changes are checked manually. The schedule and maintenance commands are documented in [CONTRIBUTING.md](CONTRIBUTING.md).

## Related collections

- [MilkThink-Lab / Awesome-Routing-LLMs](https://github.com/MilkThink-Lab/Awesome-Routing-LLMs) — a broader routing bibliography; its categorized tables informed the organization of this list.

Corrections and paper suggestions are welcome through issues or pull requests.
