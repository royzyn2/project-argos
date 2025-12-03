# **“百眼巨人计划” (Project Argos)：量化策略研发与风控SOP**

版本： 4.0 (生产环境终极版)  
状态： 现行有效  
目标： 为“百眼巨人”量化体系确立一套从策略构思到实盘上线的标准化工程流。

## **1\. 核心方针：“量化工厂”体系 (The Quant Factory)**

我们拒绝“拍脑袋”式的选股。我们构建的是一条**流水线**（工厂），产出的是**高胜率信号**（产品）。

本手册是这座工厂的**生产规范**。任何新策略——无论是“困境反转”还是“趋势动量”——都必须在统一的架构下开发，并必须通过标准化的极端压力测试，方可上线。

### **研发六部曲**

1. **顶层设计 (Definition)：** 明确的数学逻辑与交易假设。  
2. **工程落地 (Implementation)：** 标准化的数据输入与 Python 脚本。  
3. **极限施压 (Validation)：** 针对策略弱点的回测与“证伪”过程。  
4. **实盘部署 (Production)：** AI 赋能的信号生成与风控。  
5. **每日内参 (Reporting)：** 多维度元分析与深度研报生成。  
6. **运维与调度 (Operations)：** 数据更新与自动化任务流。

## **第一阶段：顶层设计（立项协议）**

**目标：** 拒绝模糊。如果一个策略无法用数学公式表达，它就不能进入开发流程。

在写第一行代码前，必须签署**策略要素表 (Strategy Card)**。这就是该策略的“产品说明书”。

| 核心要素 | 说明 | 精度标准 |
| :---- | :---- | :---- |
| **投资逻辑 (Philosophy)** | 赚谁的钱？（Alpha 来源） | *例：* “利用机构在大跌中错杀优质资产的恐慌情绪进行均值回归。” |
| **选股池 (Universe)** | 战场在哪里？ | *例：* “美股全市场，剔除市值 \< 20亿及日均成交额 \< 500万的标的。” |
| **触发信号 (The Signal)** | 具体的买入点。 | *例：* “股价跌破布林带下轨 且 RSI(14) \< 30。” |
| **风控滤网 (The Filter)** | 安全垫（排除垃圾股）。 | *例：* “剔除 净债务/EBITDA \> 4倍 或 营收连续两个季度负增长的公司。” |
| **多因子打分 (The Score)** | 优中选优的逻辑 (0-100分)。 | *例：* “50% 权重看估值折扣率，50% 权重看盈利质量。” |

### **📝 填报范例：激进复利者 (Aggressive Compounder)**

以下为一个合格的策略要素表填写示范：

| 核心要素 | 填报内容 | 精度标准 (数学定义) |
| :---- | :---- | :---- |
| **投资逻辑** | 捕捉“强者恒强”的动量效应。寻找股价走势如画线般平滑，且背后有营收同步增长支撑的标的，规避无业绩的炒作。 | Alpha \=极高的价格线性度 (Low Volatility Trend) \+ 业绩一致性 |
| **选股池** | 美股流动性充沛的成长股。 | Market Cap \> $500M 且 Avg Volume (20d) \> $10M |
| **触发信号** | 股价呈45度角稳定拉升，没有剧烈波动。 | Log-Linearity (2 Year) \> 0.90 (R平方) 且 Annualized Slope \> 20% |
| **风控滤网** | 剔除纯概念炒作（价格涨但业绩没跟上）。 | Correlation(Revenue, NetIncome) \> 0.7 (过去8个季度业绩需同步增长) |
| **多因子打分** | 侧重走势的“平滑度”而非单纯的“快”。 | 40% Linearity \+ 40% Slope \+ 20% Fundamental\_Consistency |

## **第二阶段：工程落地（编码规范）**

**目标：** 模块化与防错。我们采用 **“数据中台 \+ 策略插件”** 的架构，严禁代码逻辑的重复建设。

### **1\. 全链路架构蓝图 (Full-Stack Architecture Blueprint)**

这是包含基础设施、配置中心、日志系统和研发沙箱的**终极生产环境视图**。

project\_argos/  
├── .cursorrules            \# \[AI指令\] Cursor 的行为准则  
├── .env                    \# \[机密\] 存放 API Keys (绝对不上传git)  
├── .gitignore              \# \[Git忽略\] 忽略 data/, logs/, .env  
├── requirements.txt        \# \[依赖\] pandas, numpy, google-genai...  
│  
├── config/                 \# \[配置中心\] (+)  
│   ├── settings.yaml       \# 全局参数 (如默认回测资金、滑点设置)  
│   └── secrets\_loader.py   \# 安全加载 .env 的工具  
│  
├── logs/                   \# \[日志中心\] (+)  
│   ├── execution.log       \# 每日运行流水  
│   └── errors.log          \# 报警日志  
│  
├── notebooks/              \# \[研发沙箱\] (+)  
│   ├── research\_template.ipynb  \# 策略研究模板  
│   └── prototype\_compounder.ipynb  
│  
├── data/                   \# \[数据中台 \- 输入与中间件\]  
│   ├── market\_data/        \# \[L1\] 日线行情 (Parquet) \- 每日全量  
│   ├── fundamental\_data/   \# \[L1\] 财务宽表 (Parquet) \- 每日增量  
│   ├── meta\_data/          \# \[元数据\] 股票池与日历 (CSV)  
│   ├── results/            \# \[中间件\] 策略初筛名单 (CSV)  
│   ├── warehouse/          \# \[L2\] AI深度原料 (JSON) \- 按需  
│   └── reports/            \# \[L2\] AI原始分析 (JSON)  
│  
├── output/                 \# \[交付物\]  
│   └── daily\_briefings/    \# 人类可读的 Markdown/PDF 内参  
│  
├── experiments/            \# \[回测归档\] 按版本保存的历史回测记录  
│   ├── COMPOUNDER/  
│   │   └── v1\_baseline\_20231101/  
│   └── ...  
│  
├── prompts/                \# \[AI大脑\] 策略配置文件 (.js)  
│   ├── Aggressive\_Compounder.js  
│   ├── Fallen\_Angel.js  
│   └── ...  
│  
├── src/  
│   ├── \_\_init\_\_.py  
│   │  
│   ├── utils/              \# \[工具库\] 通用函数 (+)  
│   │   ├── math\_tools.py   \# 计算 CAGR, Sharpe  
│   │   ├── date\_tools.py   \# 处理 TTM, FY/CY 对齐  
│   │   └── logger.py       \# 统一日志配置  
│   │  
│   ├── engine/             \# \[基础设施\]  
│   │   ├── data\_loader.py  
│   │   ├── backtester.py   \# 调度中心  
│   │   ├── reporting.py  
│   │   └── warehouse\_builder.py \# \[ETL\]  
│   │  
│   ├── strategies/         \# \[策略逻辑\] (Python)  
│   │   ├── base\_strategy.py  
│   │   ├── compounder.py  
│   │   └── fallen\_angel.py  
│   │  
│   └── analysis/           \# \[AI分析\]  
│       ├── llm\_runner.py   \# API 调用  
│       └── briefing\_gen.py \# 报告生成  
│  
├── tests/                  \# \[单元测试\] (+)  
│   ├── test\_data\_loader.py \# 确保 PIT 逻辑正确  
│   └── test\_backtester.py  
│  
└── main.py                 \# \[总指挥\] 全局入口

### **2\. 策略开发的“填空题”模式**

策略脚本不应包含数据读取代码，它应该是一个继承自 BaseStrategy 的类，只需要实现核心逻辑函数。

\# src/strategies/compounder.py  
from src.utils.math\_tools import calculate\_linearity

class AggressiveCompounder(BaseStrategy):  
    """  
    开发人员只需要关注：选什么、怎么分、怎么买。  
    不需要关注：数据怎么读、回测怎么跑。  
    """  
      
    def define\_universe(self, df):  
        \# 1\. 定义股票池  
        return df\[df\['market\_cap'\] \> 5e8\]

    def calculate\_signals(self, df):  
        \# 2\. 计算特有指标 (使用 utils 工具库)  
        df\['linearity'\] \= calculate\_linearity(df\['close'\])  
        df\['growth\_yoy'\] \= (df\['revenue\_ttm'\] / df\['revenue\_ttm'\].shift(4)) \- 1  
        return df

    def generate\_score(self, df):  
        \# 3\. 打分逻辑  
        return (df\['linearity'\] \* 0.5) \+ (df\['growth\_yoy'\] \* 0.5)

### **3\. 财务数据处理规范 (Financial Data Hygiene)**

我们的输入是包含多个季度历史的**时间序列 (Time Series)**。在使用这些数据时，开发人员必须警惕以下“陷阱”。本节不是强制命名，而是**强制防错**。

**核心风险提示：**

* **⚠️ 估值陷阱 (Valuation Trap):** 严禁使用 **单季数据 (Quarterly)** 直接除以 **总市值** 来计算 PE 或 PS。这会导致估值被低估 75%。  
  * *规范：* 涉及估值计算，必须先计算 \_ttm (Rolling 4Q Sum) 或对单季数据进行年化处理。  
  * *变量建议：* 计算出的衍生指标建议加上 \_ttm 后缀以示区分（如 revenue\_ttm）。  
* **⚠️ 增长率错配 (Growth Rate Mismatch):** 策略必须明确定义“增长”的口径。  
  * *YoY (同比):* 消除季节性影响，适合大多数策略。  
  * *QoQ (环比):* 仅适用于捕捉**极端爆发 (Surge)** 或 **困境反转**。注意：QoQ 极易受季节性（如零售业Q4）干扰，必须慎用。  
* **⚠️ 预期数据 (Consensus):** 如果策略逻辑涉及“超预期”，必须显式调用 estimate 数据列。  
  * *前瞻估值:* 使用 market\_cap / net\_income\_estimated\_next\_12m 对成长股进行定价。

### **4\. PIT (Point-in-Time) 字段映射规范**

**核心痛点：** 拥有财报发布日期（Filling Date）是巨大的优势，但**用错列**依然会导致回测失效。绝不能使用“报告期结束日”（Period End）作为信号触发日。

**工程规范：** 在合并价格数据与基本面数据时，必须使用**实际公告日**进行对齐。这一步应在 src/engine/data\_loader.py 中**统一实现**，禁止策略脚本私自处理数据合并。

* **禁止使用：** period\_end\_date (例如：Q1的 3月31日。此时数据根本没发，用了就是作弊)。  
* **强制使用：** filling\_date / acceptedDate / reportDate (例如：实际发财报的 4月22日)。

\# src/engine/data\_loader.py (共享代码库)

def align\_fundamentals\_precise(price\_df, fund\_df):  
    """  
    全系统统一的对齐逻辑，确保所有策略都遵守 PIT 规范  
    """  
    fund\_df\['filling\_date'\] \= pd.to\_datetime(fund\_df\['filling\_date'\])  
    merged \= pd.merge\_asof(price\_df.sort\_values('date'),   
                           fund\_df.sort\_values('filling\_date'),   
                           left\_on='date',   
                           right\_on='filling\_date',   
                           direction='backward')  
    return merged

### **5\. 标准化输出接口 (Standard Output Interface)**

这是连接 **数学筛选** 和 **回测/AI** 的唯一桥梁。我们强制规定：**一个策略对应一个 CSV 文件**。

**文件物理规范：**

* 命名：data/results/{strategy\_name}.csv  
* 隔离性：每个 CSV 只包含该策略筛选出的候选股票。

**Schema 规范（表头必须完全一致）：** 虽然文件独立，但列名必须统一，以便下游引擎读取。

| 必须列名 | 数据类型 | 填写说明 |
| :---- | :---- | :---- |
| ticker | String | 股票代码 (如 AAPL) |
| date | Date | 信号触发日期 (如 2023-11-20) |
| strategy\_name | String | **AI 路由键**。必须与 Prompt 配置文件名前缀一致。(如 "COMPOUNDER") |
| backtest\_type | String | **回测路由键**。填 CALENDAR (日历回测) 或 EVENT (事件回测)。 |
| raw\_score | Float | 0-100 的算法初筛分。 |
| primary\_metric | String | **AI 核心论据**。如 "0.95 (Linearity)" 或 "-35% (Drawdown)"。 |
| secondary\_metric | String | AI 辅助论据。如 "25% (EPS Growth)"。 |

### **6\. 数据熔断机制 (Data Circuit Breakers)**

**规范：** src/engine/data\_loader.py 必须包含统一的熔断逻辑。

* **空值熔断：** 如果某列核心指标（如 PE\_Ratio）的缺失率 \> 20%，脚本应**报错停止**，而不是输出错误结果。  
* **极值过滤：** 剔除价格为 0 或 负数的异常 tick。

### **7\. “自适应评分”开发范式**

**铁律：** 严禁使用绝对阈值进行打分（因为不同行业水位不同）。必须使用**分位数排名 (Percentile Ranking)** 或 **动态归一化**。

## **第三阶段：极限施压（回测与证伪）**

**目标：** “证伪”策略。我们的目的不是证明它能赚钱，而是**拼命证明它会亏钱**。如果它在这种攻击下还没死，才允许上线。

### **1\. 实验版本控制 (Experiment Versioning)**

**核心痛点：** “我改了参数，回测结果变好了，但我不记得旧参数的结果去哪了。” **解决方案：** 引入 **“实验快照 (Experiment Snapshot)”** 机制。

**输出路径规范：** 每次运行回测，系统不应覆盖旧文件，而应创建带有 **时间戳** 和 **实验ID** 的新文件夹。

experiments/  
├── COMPOUNDER/                  \# 策略大类  
│   ├── v1\_baseline\_20251101/    \# \[旧版本\] 基准测试  
│   │   ├── candidates.csv       \# 当时的选股名单  
│   │   ├── backtest\_report.md   \# 当时的体检报告  
│   │   └── config\_snapshot.json \# 当时的参数配置 (重要\!)  
│   │  
│   └── v2\_strict\_moat\_20251128/ \# \[新版本\] 收紧护城河参数  
│       ├── candidates.csv  
│       ├── backtest\_report.md  
│       └── config\_snapshot.json

**操作建议：** 在运行回测脚本时，强制要求输入 \--tag 参数。 python main.py \--strategy COMPOUNDER \--tag "v2\_strict\_moat"

### **2\. 自动化分流调度 (Auto-Dispatch)**

回测引擎 (src/engine/backtester.py) 会遍历 data/results/ 下的所有 CSV 文件，逐一进行测试。

**调度伪代码：**

def run\_all\_backtests():  
    \# 1\. 获取所有结果文件  
    csv\_files \= glob.glob("data/results/\*.csv")  
      
    for csv\_path in csv\_files:  
        print(f"正在测试策略文件: {csv\_path} ...")  
          
        \# 2\. 读取第一行，判断回测类型 (Self-Describing)  
        df \= pd.read\_csv(csv\_path)  
        mode \= df\['backtest\_type'\].iloc\[0\]  
          
        \# 3\. 分流执行  
        if mode \== 'CALENDAR':  
            report \= run\_calendar\_test(df)  
        elif mode \== 'EVENT':  
            report \= run\_event\_study(df)  
              
        \# 4\. 保存该策略的独立报告  
        save\_report(report)

### **协议 A：“盲式穿越测试” (Blind Time Travel)**

**适用：** backtest\_type \== CALENDAR

**核心逻辑：**

1. **随机抽样：** 选取历史上的随机时间点（如 2021-06-15）。  
2. **盲测：** 仅利用该时间点及之前的数据生成信号。  
3. **追踪：** 计算 T+3月, T+6月的超额收益。

### **协议 B：“极端行情压力测试” (The Kryptonite Test)**

**适用：** 所有策略（必测）。

**核心逻辑：** 必须测试策略在其“克星”环境下的表现。

**压力测试矩阵（必测项）：**

| 策略流派 | “至暗时刻” (测试环境) | 测试时间窗 | 验收标准 (Pass Criteria) |
| :---- | :---- | :---- | :---- |
| **成长 / 动量策略** | **加息/杀估值周期** | *2022年 Q1* | 最大回撤 \< 30% |
| **深度价值策略** | **流动性危机/熔断** | *2020年 3月* | 反弹速度 \> 大盘 |
| **小市值 / 黑马策略** | **流动性枯竭期** | *2018年 Q4* | 选出的票成交额是否足以进出？ |
| **高股息 / 收息策略** | **通胀飙升期** | *2022-2023年* | 总回报是否跑赢通胀？ |

### **协议 C：参数鲁棒性协议 (Parameter Robustness Protocol)**

**适用：** 所有策略（必测）。

**核心逻辑：** 防止过拟合。将核心参数上下浮动 10%，观察结果是否剧烈波动。

* **验收标准：** 胜率和回撤的变动幅度 \< 15%。

### **协议 D：事件对齐回测协议 (Event-Aligned Backtest Protocol)**

**适用：** backtest\_type \== EVENT

**核心逻辑：** 采用 **“T+N 归一化”** 回测法。将所有股票的财报发布日对齐为 $T\_0$，计算 $T\_{+1}$ 至 $T\_{+60}$ 的累计超额收益 (CAR)。

### **5\. 回测结果交付与决策标准 (Backtest Deliverables & Decision Matrix)**

回测不是为了看个热闹，而是为了下决定。每次回测结束，系统必须生成一份标准化的 **“策略体检报告 (Report Card)”**。

#### **A. 交付物 (The Report Card)**

每个策略回测必须输出以下核心指标：

| 维度 | 指标名称 (Metric) | 含义 |
| :---- | :---- | :---- |
| **收益性** | **Alpha (超额收益)** | 策略年化收益 \- 行业基准年化收益。 |
| **稳定性** | **Win Rate (胜率)** | 赚钱交易次数 / 总交易次数。 |
| **风险性** | **Max Drawdown (最大回撤)** | 历史最惨的一次亏损幅度。 |
| **机会** | **MFE (最大潜在收益)** | 买入后最高冲到了多少（衡量卖飞了没）。 |
| **痛苦** | **MAE (最大不利回撤)** | 持仓期间最大浮亏是多少（衡量能不能拿住）。 |
| **鲁棒性** | **Sensitivity (敏感度)** | 参数变动 10% 时，收益率变动了多少。 |

#### **B. 决策矩阵 (Decision Matrix)**

拿到体检报告后，请严格对照下表进行操作：

| 场景 | 关键特征 | 判决 (Verdict) | 执行动作 (Action) |
| :---- | :---- | :---- | :---- |
| **✅ 通过 (PASS)** | Alpha \> 5% AND MaxDD \< 25% AND WinRate \> 50% | **上线 (Deploy)** | 进入 Phase 4，配置 AI 监控，小资金实盘。 |
| **⚠️ 需优化 (OPTIMIZE)** | Alpha \> 10% (很赚钱) BUT MaxDD \> 40% (回撤大) | **风控修正** | 策略逻辑成立，但需加入**止损模块**或**降低仓位**。 |
| **❌ 淘汰 (FAIL)** | Alpha \< 0% (跑输大盘) OR MaxDD \> 50% (爆仓风险) | **丢弃 (Discard)** | 逻辑证伪。不要试图优化参数来“救”它，直接扔掉。 |
| **🚫 异常 (DEBUG)** | Sharpe \> 3.0 (太完美) OR WinRate \> 90% | **作弊嫌疑** | **严禁上线**。99%是用了未来函数（如用了当季未发布的EPS）。检查 PIT 代码。 |

## **第四阶段：实盘部署（AI 投委会）**

**目标：** 利用 AI 模拟“资深基金经理”的定性分析。

我们采取 **“独立评分卡 (Independent Scorecards)”** 架构。AI 分析是高度定制化的，**绝不搞一刀切**。

### **1\. 数据ETL与仓库构建 (Data Warehouse Builder)**

在 AI 分析开始前，必须先进行 **数据补全**。因为量化筛选只用到了结构化数据，而 AI 分析需要大量的非结构化文本。

**模块功能:** src/engine/warehouse\_builder.py **触发条件:** 当 backtester.py 的筛选结果生成 CSV 后，自动触发。

**执行流程:**

1. **读取名单:** 读取 data/results/compounder.csv 中的 Top 30 股票。  
2. **调用 API (FMP):** 针对这些股票，批量下载：  
   * Transcript: 最近 4 个季度的业绩会文字记录。  
   * Segment Revenue: 按产品线的营收明细。  
   * Key Metrics: 详细的财务比率。  
3. **落地存储:** 将数据标准化为 JSON，存入 data/warehouse/{ticker}/ 目录。

### **2\. AI 架构与 I/O 流程 (AI Architecture & I/O)**

**输入 (Inputs):**

1. **策略清单 (Trigger):** data/results/{strategy\_name}.csv (例如 compounder.csv)。  
2. **深度数据 (Context):** data/warehouse/{ticker}/ 下的所有 JSON 文件。  
3. **分析大脑 (Instruction):** prompts/{Strategy\_Name}.js (例如 Aggressive\_Compounder.js)。

**处理逻辑 (Process):** src/analysis/llm\_runner.py 会遍历 CSV 中的每一行，加载对应的 JSON Prompt，填入仓库中的深度数据，发送给 Gemini。

**输出 (Outputs):** 生成独立的 JSON 分析报告，严禁合并不同策略的结果。

* **路径:** data/reports/{strategy\_name}/{ticker}\_{date}.json  
* **内容:** 包含 final\_score, moat\_verdict, valuation\_check, kill\_risk。

### **3\. 配置文件规范 (Config Specification)**

每个策略必须在 prompts/ 目录下拥有一个专属的 **JSON 配置文件**。

**标准化结构：** 所有配置文件必须包含以下四个顶级 Key，但内容可以完全不同：

1. persona: 定义 AI 的身份（是价值投资者还是困境反转专家？）。  
2. guidingPrinciples: 定义风控红线（例如：是否容忍高 PE？）。  
3. task\_instructions: 定义具体的分析任务（例如：分析护城河还是分析库存？）。  
4. output\_schema: 定义输出的 JSON 结构。

### **3\. AI 时间旅行协议 (Time Travel Protocol for AI)**

**痛点：** 如果你把 2024 年的年报喂给 AI 叫它分析 2022 年的买入机会，AI 会因为“剧透”而给出错误的分析。

**强制规范 (The Snapshot Rule)：** 在进行 AI 回测时，严禁直接投喂全量数据。必须由 src/analysis/llm\_runner.py 执行 **“时间切片 (Time Slicing)”**。

1. **确定观察日 (Observation Date):** 假设我们在回测 2022-06-15 的信号。  
2. **数据裁剪 (Data Pruning):**  
   * 读取 master\_financials.parquet。  
   * **过滤逻辑：** df \= df\[df\['filing\_date'\] \<= '2022-06-15'\]。  
   * **后果：** 任何在该日期之后发布的数据（哪怕是第二天发布的），对 AI 来说都是“不存在的”。  
3. **快照生成 (Context Generation):**  
   * 将裁剪后的数据生成一个临时的 context\_snapshot\_20220615.json。  
   * 仅将此快照发送给 Gemini API。

*这是防止 AI “作弊”的唯一物理手段。*

## **第五阶段：内参生成 (Briefing Generation)**

**目标：** 将零散的 AI JSON 报告，汇总为人类可读的 **投资决策支持文档 (Daily Briefing)**。

这一步不再是数据处理，而是 **“元分析 (Meta-Analysis)”**。

### **1\. 报告架构 (The Briefing Structure)**

src/analysis/briefing\_gen.py 负责读取所有 data/reports/ 下的新鲜 JSON，并生成一份 Markdown。

报告必须包含三个部分：

#### **Part A: 市场上帝视角 (The Meta-Dashboard)**

不要只给我看个股，先告诉我 AI 的整体情绪。

* **机会分布 (Opportunity Spread):** \* *Chart:* 直方图展示 Gemini 的打分分布。是正态分布？还是全是 9 分（说明 AI 坏了）？还是全是 3 分（说明市场极差）？  
* **行业热力图 (Sector Heatmap):** \* *Chart:* 哪个 Sector 出现的高分股最多？（例如：今天全是医疗股，说明资金在防御）。  
* **策略拥挤度 (Strategy Crowd):** \* Compounder 选出了 20 个，但 Fallen Angel 选出了 0 个？（暗示牛市中后期）。

#### **Part B: 精英榜单 (The Ranked Menu)**

这是最简单的“点菜菜单”，按 Gemini Score 降序排列。**按策略分表展示**。

**【Aggressive Compounder 精选】** | 排名 | 代码 | 得分 | AI 一句话点评 (One-Liner) | | :--- | :--- | :--- | :--- | | 1 | **APP** | **9.8** | 广告技术护城河极深，估值即使在上涨后仍合理。 | | ... | ... | ... | ... |

**【Fallen Angel 精选】** | 排名 | 代码 | 得分 | AI 一句话点评 (One-Liner) | | :--- | :--- | :--- | :--- | | 1 | **HIMS** | **9.2** | 并非单纯的反弹，毛利率结构性改善确认。 | | ... | ... | ... | ... |

#### **Part C: 深度研报 (The Deep Dives)**

**这是 AI 价值的核心。** 不要只给一行字。根据 JSON 中的 output\_schema 渲染出完整的逻辑。

**股票代码：APP (AppLovin)**

* **核心业务：** 移动应用营销与变现平台。  
* **护城河分析 (Moat):** 10/10。AXON 引擎的数据网络效应构成了极高的转换成本。  
* **估值分析 (Valuation):** Undervalued。虽然 PE 看起来高，但考虑到 PEG \< 0.8，处于 Early Cycle。  
* **潜在风险 (Downside):** 移动广告市场的隐私政策变化 (IDFA)。  
* **潜在爆发点 (Upside):** 进军 CTV (Connected TV) 市场超预期。

## **第六阶段：运维与调度 (Operations & Scheduling)**

**目标：** 定义“数据怎么更新”以及“脚本什么时候跑”。

### **1\. 数据维护逻辑 (Maintenance Strategy)**

**原则：** “L1 全量，L2 按需”。

| 数据层级 | 包含内容 | 维护频率 | 维护策略 |
| :---- | :---- | :---- | :---- |
| **L1 (基础层)** | 日线行情 (Prices) 基础财务 (Financials) | **每日更新** | market\_data: 增量追加 (Append) fundamental\_data: 覆盖更新 (Merge) |
| **L2 (深度层)** | 电话会纪要 (Transcripts) 产品线明细 (Segments) | **按需加载** | 仅当股票出现在 results/\*.csv 中时，才下载其数据并存入 warehouse/。 |

### **2\. 每日任务流 (The Daily Cron Job)**

建议设定如下的自动化时间表（以美东时间为例）：

* **16:30 (收盘后):** 交易所闭市。  
* **17:00 (Step 1):** 运行 update\_market\_data.py。  
  * *动作:* 从 API 拉取当日 OHLCV，追加到 Parquet 文件。  
* **17:30 (Step 2):** 运行 run\_strategies.py (Main Engine)。  
  * *动作:* 加载 L1 数据，运行所有策略脚本，生成 data/results/\*.csv。  
* **17:45 (Step 3):** 运行 warehouse\_builder.py (ETL)。  
  * *动作:* 读取 CSV，识别出 Top 30 候选股。检查 data/warehouse/，如果缺 L2 数据，立即下载。  
* **18:00 (Step 4):** 运行 llm\_runner.py (AI Analysis)。  
  * *动作:* 读取 CSV 和 L2 数据，并行调用 Gemini，生成 JSON 报告。  
* **18:30 (Step 5):** 运行 briefing\_gen.py。  
  * *动作:* 汇总 JSON，生成 Markdown 内参，推送到你的邮箱/Slack。

## **总结：验收标准 (Definition of Done)**

只有同时满足以下 4 点，策略才具备“实盘资格”：

1. **\[策略要素表\]** 已归档，逻辑自洽。  
2. 遵循 **\[架构蓝图 v4.0\]**，代码模块化，包含 config 和 utils。  
3. 通过 **\[基础协议 (A或D)\]** \+ **\[压力协议 (B)\]** \+ **\[鲁棒协议 (C)\]** 测试，且结果符合 **\[决策矩阵\]** 的“PASS”标准。  
4. **\[配置了专属的 AI JSON 脚本\]**，且通过了 **\[AI 时间旅行\]** 检查。

*此时，方可将其加入 Cron Job（自动调度任务），正式实盘运行。*