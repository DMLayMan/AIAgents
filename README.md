# AI Daily Radar

一个用于**每天跟踪 AI 热点新闻和最新研究论文**的自动化仓库模板。

## 功能特性

- 📰 聚合多源 AI 新闻 RSS（可配置）
- 📄 抓取 arXiv 最新 AI 相关论文（按分类）
- 🧠 自动去重、截断摘要、生成日报 Markdown
- ⏰ 内置 GitHub Actions 每天定时运行

## 快速开始

### 1) 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) 本地运行

```bash
python scripts/run_daily.py
```

运行后会在 `reports/` 目录下生成当日文件，如：

- `reports/2026-02-24-ai-daily.md`

### 3) 配置抓取源

编辑 `config/sources.yaml`：

- `news_feeds`: 新闻 RSS 地址列表
- `arxiv.categories`: arXiv 分类（如 `cs.AI`, `cs.CL`）
- `arxiv.max_results_per_category`: 每个分类抓取条数

## 自动化（GitHub Actions）

仓库已包含 `.github/workflows/daily-radar.yml`，默认每天 UTC 01:30 执行：

- 拉取新闻与论文
- 生成 `reports/` 日报
- 自动提交到仓库

你可以按需修改 cron 表达式。

## 目录结构

```text
.
├── config/
│   └── sources.yaml
├── reports/
│   └── .gitkeep
├── scripts/
│   └── run_daily.py
├── src/
│   ├── __init__.py
│   └── ai_daily_radar.py
├── tests/
│   └── test_ai_daily_radar.py
├── .github/workflows/
│   └── daily-radar.yml
├── requirements.txt
└── README.md
```

## 后续可扩展

- 增加 LLM 自动摘要/中文翻译
- 推送到飞书/企业微信/Telegram/邮箱
- 关键词打分与热点趋势追踪
- 增加 Papers With Code、Hugging Face Trending 等来源
