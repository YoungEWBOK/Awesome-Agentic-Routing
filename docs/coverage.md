# Coverage review — 2026-11-06

[Paper index](../README.md) · [Resource notes](resources.md)

The initial 30-paper collection was compared with [MilkThink-Lab / Awesome-Routing-LLMs](https://github.com/MilkThink-Lab/Awesome-Routing-LLMs). This review adds 26 papers within the existing eight categories. Selection focuses on missing problem formulations, methodological lines, and evaluation settings; it is not a complete import of the reference bibliography.

## Additions

| Coverage gap | Added papers | Contribution to the collection |
| --- | --- | --- |
| Early constrained model choice and adaptive inference compute | [FORC](https://arxiv.org/abs/2308.06077), [BEST-Route](https://proceedings.mlr.press/v267/ding25d.html), [Prompt-to-Leaderboard](https://proceedings.mlr.press/v267/frick25a.html) | Meta-model assignment, joint model/sample-budget selection, and prompt-specific preference scores |
| Model representations and unseen candidates | [EmbedLLM](https://arxiv.org/abs/2410.02223), [IRT-Router](https://aclanthology.org/2025.acl-long.761/), [UniRoute](https://arxiv.org/abs/2502.08773), [CSCR](https://arxiv.org/abs/2508.12491) | Reusable embeddings, interpretable ability/difficulty models, and transfer across candidate pools |
| Partial feedback and the cost of supervision | [Causal LLM Routing](https://arxiv.org/abs/2505.16037), [DARS](https://arxiv.org/abs/2606.06924), [SaveRouter](https://arxiv.org/abs/2609.37402) | Observational-policy learning, stochastic quality estimates, and sparse feedback acquisition |
| Verification and calibrated selection | [Self-REF](https://proceedings.mlr.press/v267/chuang25b.html), [CRE-Router](https://arxiv.org/abs/2606.27457), [Conformal LLM Routing](https://aclanthology.org/2026.acl-srw.70/) | Confidence-token deferral, pre-routing plus escalation, and selective error control |
| User history and shared session budgets | [GMTRouter](https://arxiv.org/abs/2511.08590), [SeqRoute](https://arxiv.org/abs/2605.25424) | Personalized routing and offline session-budget allocation; distinct uses of multi-turn data |
| Routing during decoding | [R2R](https://arxiv.org/abs/2505.21600), [FusionRoute](https://proceedings.mlr.press/v306/xiong26p.html) | Token-level selection between separate models; distinct from model-internal MoE routing |
| Agent selection and collaboration design | [Heterogeneous Swarms](https://arxiv.org/abs/2502.04510), [AgentRouter](https://aclanthology.org/2026.acl-long.33/), [Agent-as-a-Router](https://arxiv.org/abs/2606.22902) | Collaboration-graph search, graph-guided agent selection, and experience-accumulating task routing |
| Broader routing evaluation | [RouterEval](https://aclanthology.org/2025.findings-emnlp.208/), [RouterArena](https://arxiv.org/abs/2510.00202), [MMR-Bench](https://doi.org/10.1007/978-3-032-37083-9_34), [AgentSelect](https://arxiv.org/abs/2603.03761), [EC2-Bench](https://arxiv.org/abs/2610.17816) | Large model pools, multimodal inputs, complete agent configurations, and edge-cloud trajectories |
| Serving infrastructure | [vLLM Semantic Router](https://arxiv.org/abs/2603.04444) | Deployment-oriented composition of routing signals and selection policies |

## Source corrections

- **RouterEval** is published in [Findings of EMNLP 2025](https://aclanthology.org/2025.findings-emnlp.208/), not the main proceedings.
- **Conformal LLM Routing** is an [ACL 2026 Student Research Workshop](https://aclanthology.org/2026.acl-srw.70/) paper.
- **RouterArena** is an ICLR **2026** paper; see the [conference paper](https://openreview.net/forum?id=9HsaIi4ngF) and [accepted-paper listing](https://iclr.cc/Downloads/2026).
- **AgentRouter** has an [ACL 2026 publication](https://aclanthology.org/2026.acl-long.33/). **MMR-Bench** has an [ECCV 2026 proceedings version](https://doi.org/10.1007/978-3-032-37083-9_34); its expanded V2 data release uses a different evaluation pool.
- **AgentSelect** moved from `Ancientshi/AgentMatch` to [Ancientshi/AgentSelect](https://github.com/Ancientshi/AgentSelect).
- The [BEST-Route author repository](https://github.com/microsoft/best-route-llm) also contains **Hybrid LLM**; its previously missing code entry has been filled.

## Interpretation notes

GMTRouter uses interaction history for preference modeling. SeqRoute studies budget allocation from offline sessions. These settings differ from learning a model-switching policy through live task execution. Agent-as-a-Router accumulates feedback across streaming tasks, while AgentSelect recommends complete agent configurations. Heterogeneous Swarms changes model weights as well as collaboration roles.

Other papers in the reference collection remain candidates for later review. This pass prioritizes coverage of distinct routing questions over multiple closely related implementations. Network-routing applications, distillation-only work, and unrelated domain applications were not imported. Non-inclusion is not a quality judgment.

New entries were checked against primary paper metadata and abstracts, with selected method or evaluation details inspected. Code links are included only where the authorship and paper association could be established. This review did not reproduce experiments.
