# 模型与 Agent 路由：问题定义、方法与评测

[论文目录](README.md) · [代码与数据资源](docs/resources.md) · [近期 arXiv 论文](RECENT.md)

本指南讨论独立模型之间的选择，以及任务执行过程中的模型调用与 Agent 分工。分类依据是决策时机和动作空间；监督学习、强化学习、检索和图表示属于实现方法，可以出现在不同类别中。

## 1. 问题定义

### 1.1 单次模型选择

给定输入 $q$ 和候选模型集合 $\mathcal{M}$，路由器在生成回答前选择模型。常见形式是估计质量 $\widehat{Q}(q,m)$ 与成本 $\widehat{C}(q,m)$，再作选择：

$$
m^*(q)=\arg\max_{m\in\mathcal{M}}\left[\widehat{Q}(q,m)-\lambda\widehat{C}(q,m)\right].
$$

这是便于比较方法的一种写法，不是所有论文共同采用的目标函数。质量可以由正确率、人工偏好或任务评分定义；也有工作使用预算约束或质量容忍度，而非加权目标。[RouteLLM](https://arxiv.org/abs/2406.18665)、[Hybrid LLM](https://arxiv.org/abs/2404.14618) 和 [CARROT](https://arxiv.org/abs/2502.03261) 分别展示了偏好监督、质量容忍度和成本—质量估计的处理方式。

[FORC](https://arxiv.org/abs/2308.06077) 是较早将性能预测与预算约束分配结合的工作。[BEST-Route](https://proceedings.mlr.press/v267/ding25d.html) 进一步联合选择模型与采样次数，因此其动作空间还包含测试时计算量。[Prompt-to-Leaderboard](https://proceedings.mlr.press/v267/frick25a.html) 则估计输入相关的人类偏好排名，为路由提供不同于平均榜单的质量信号。

### 1.2 级联与回答验证

级联先调用一个模型，再根据回答及其质量估计决定停止或升级。决策时可用的信息比单次预路由更多，代价是已经发生的生成和验证开销。[FrugalGPT](https://arxiv.org/abs/2305.05176) 学习级联策略；[AutoMix](https://arxiv.org/abs/2310.12963) 使用自验证信号与 POMDP 路由。这里需要区分答案质量、质量估计误差和升级代价。

### 1.3 序贯路由

多步任务中，模型选择可写为 $m_t\sim\pi(\cdot\mid h_t,b_t)$，其中 $h_t$ 表示可见交互历史，$b_t$ 表示剩余预算。当前输出可能改变后续观测、执行路径和所需能力，因此单步质量与终局成功并不等价。

序贯性有不同来源：[DialRouter](https://arxiv.org/abs/2604.12385) 研究回复对后续用户对话的影响；[BAAR](https://arxiv.org/abs/2602.21227) 研究交互任务中的逐步大小模型选择与预算；[MTRouter](https://aclanthology.org/2026.acl-long.2045/) 从历史轨迹学习模型的结果效用估计。用户对话轮次、内部模型调用次数和环境交互步数应分别记录。

[SeqRoute](https://arxiv.org/abs/2605.25424) 将会话预算纳入离线强化学习状态；[GMTRouter](https://arxiv.org/abs/2511.08590) 使用多轮交互图建模用户偏好。后者利用历史信息进行个性化，不宜仅凭“multi-turn”将其解释为长期任务回报优化。

另一种粒度是在自回归解码的每一步选择模型。[R2R](https://arxiv.org/abs/2505.21600) 学习哪些 token 需要调用较大模型；[FusionRoute](https://proceedings.mlr.press/v306/xiong26p.html) 除选择模型外，还学习对下一 token 分布的补充 logits。这是独立模型间的协同生成，与单个 MoE 模型内部的专家路由不同。评测时还需记录模型切换、共享上下文和解码同步开销。

### 1.4 模型与 Agent 编排

编排的动作空间还可能包含角色分配、任务分解、工具调用、并行执行与停止决策。[Router-R1](https://arxiv.org/abs/2506.09033) 在推理过程中调用并聚合其他模型；[MasRouter](https://aclanthology.org/2025.acl-long.757/) 联合选择协作方式、角色和模型；[E³-Orch](https://arxiv.org/abs/2608.04588) 在执行过程中组织里程碑、依赖关系和执行者分配。比较这些方法时，应先核对控制器实际决定的内容。

## 2. 主要方法及其信息来源

| 方法路线 | 典型输入或监督 | 代表工作 | 比较时需记录的条件 |
| --- | --- | --- | --- |
| 质量、偏好与成本预测 | 查询特征、回答评分、成对偏好 | FORC、RouteLLM、Hybrid LLM、CARROT、P2L | 标签来源、成本口径、模型池 |
| 在线分配 | 查询流、历史反馈、候选模型统计 | MixLLM | 探索成本、反馈可得性、分布变化 |
| 查询—模型表示 | 查询编码、模型表示、任务关系 | EmbedLLM、IRT-Router、RouterDC、GraphRouter、LLMRec | 新模型的观测要求与训练覆盖 |
| 能力画像与迁移 | 公开元信息或少量行为上下文 | UniRoute、CSCR、RouteProfile、RouteFM | 画像构建成本、未见任务与未见模型的划分 |
| 回答验证与级联 | 已生成回答、自验证或外部评分 | FrugalGPT、AutoMix、Self-REF、CRE-Router | 置信度误差、累计调用费用 |
| 解码级模型选择 | 生成前缀、token 分歧、模型输出分布 | R2R、FusionRoute | token 兼容性、切换开销、是否额外学习生成分布 |
| 路由误差控制 | 正确性标签、独立校准样本 | Conformal LLM Routing | 误差事件的定义、校准假设与适用分布 |
| 路由监督构建 | 部分反馈日志、重复采样、选择性反馈获取 | Causal LLM Routing、DARS、SaveRouter | 可识别性、标签方差、监督成本 |
| 轨迹结果与预算学习 | 交互历史、终局结果、剩余预算 | BAAR、MTRouter | 行为策略覆盖、延迟反馈、预算可行性 |
| 搜索与进展估计 | 对话分支、未来状态近似、任务进展 | DialRouter、ProgRouter | 模拟器或进展信号与真实结果的一致性 |
| 学习式编排 | 多轮调用轨迹、任务结果和成本奖励 | Router-R1、xRouter、ToolOrchestra、E³-Orch | 控制器能力、训练预算、可用工具与执行者 |
| 经验与技能建模 | 成败轨迹、技能描述、执行成本 | SkillOrchestra、RSI-Router | 路由策略和执行技能各自的贡献 |

各论文的原文和代码入口见 [README](README.md)。表中“方法路线”用于比较，不表示类别互斥。

## 3. 评测中需要区分的量

**静态选择与闭环执行。** [RouterBench](https://arxiv.org/abs/2403.12031) 和 [LLMRouterBench](https://aclanthology.org/2026.findings-acl.1881/) 提供模型输出与统一比较条件。[TwinRouterBench](https://arxiv.org/abs/2605.18859) 同时包含中间前缀的静态评测和真实 Agent 执行。静态结果可用于比较同一输入上的模型选择；执行路径变化带来的收益需要接续执行评测。

**评测对象与任务覆盖。** [RouterEval](https://aclanthology.org/2025.findings-emnlp.208/) 考察较大候选池中的路由与模型规模效应；[RouterArena](https://arxiv.org/abs/2510.00202) 提供跨领域、难度分层的路由器比较；[MMR-Bench](https://doi.org/10.1007/978-3-032-37083-9_34) 将模型选择扩展到多模态输入。[AgentSelect](https://arxiv.org/abs/2603.03761) 的候选是由骨干模型和工具集构成的完整 Agent 配置，[EC2-Bench](https://arxiv.org/abs/2610.17816) 则执行长程任务并分析边云协作的效果、资源使用和隐私暴露。它们对应不同的研究问题。

**当前结果与动作价值。** 从日志预测终局结果，依赖日志中的状态分布与模型选择策略。若同一类状态很少由不同模型执行，就需要额外分析来支持“在此处替换模型会改善结果”的判断。

**监督成本与统计含义。** [Causal LLM Routing](https://arxiv.org/abs/2505.16037) 研究仅观测被调用模型结果的日志；[DARS](https://arxiv.org/abs/2606.06924) 研究随机解码和查询改写造成的标签波动；[SaveRouter](https://arxiv.org/abs/2609.37402) 将反馈采集费用与后续服务节省一起计算。[Conformal LLM Routing](https://aclanthology.org/2026.acl-srw.70/) 控制的是满足其校准假设时、分配给小模型的查询中的错误率，不能直接扩展为对任意分布变化或整个 Agent 系统的安全保证。

**推理费用与完整系统开销。** 除工作模型费用外，还应记录路由器调用、上下文传递、验证、失败重试和缓存变化。训练与数据收集费用宜单独报告。延迟还受并行调度、模型加载和服务排队影响。

**迁移对象。** 未见查询、未见任务、未见模型、候选池变化和执行框架变化是不同设置。加入新模型时使用了多少标注或执行记录，应与迁移结果一起说明。

**模型池与比较协议。** 不同论文的模型、价格、提示、采样参数和评分器可能不同。成功率或费用降幅只有在这些条件明确时才便于解释。综述 [Dynamic Model Routing and Cascading](https://arxiv.org/html/2603.04445v3) 的评测章节讨论了相关可比性问题。

## 4. 阅读顺序

| 阶段 | 文献 | 目标 |
| --- | --- | --- |
| 领域概览 | Dynamic Model Routing and Cascading；Doing More with Less | 区分决策时机、输入信息和优化目标 |
| 单次选择与级联 | RouteLLM；Hybrid LLM；FrugalGPT；AutoMix | 比较生成前预测和生成后验证 |
| 表示与迁移 | EmbedLLM；IRT-Router；UniRoute；GraphRouter；RouteFM | 理解模型能力如何表示以及如何接入新候选 |
| 序贯决策 | BAAR；MTRouter；DialRouter；ProgRouter | 分析状态转移、长期反馈和资源约束 |
| 编排 | Router-R1；ToolOrchestra；SkillOrchestra；E³-Orch | 比较动作空间和学习信号 |
| 评测 | RouterBench；LLMRouterBench；TwinRouterBench | 将方法结论对应到实际评测条件 |

阅读记录建议包含问题设置、状态、动作、监督来源、模型池、评测协议和主要结果。对具体实验尚未检查的内容应保留为问题，不写成已确认的局限或结论。

本轮与 MilkThink-Lab 清单的[覆盖对照记录](docs/coverage.md)列出了新增文献的选择理由和发表信息修正。
