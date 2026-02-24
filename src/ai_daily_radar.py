from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Item:
    title: str
    link: str
    source: str
    published: str
    summary: str


def load_sources(config_path: str | Path) -> dict:
    import yaml

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _trim(text: str, max_len: int = 180) -> str:
    raw = " ".join((text or "").split())
    return raw if len(raw) <= max_len else f"{raw[: max_len - 3]}..."


def _unique(items: Iterable[Item]) -> list[Item]:
    seen: set[str] = set()
    output: list[Item] = []
    for it in items:
        key = (it.title or "").strip().lower()
        if key and key not in seen:
            seen.add(key)
            output.append(it)
    return output


def fetch_news(feed_urls: list[str], per_feed_limit: int = 8) -> list[Item]:
    result: list[Item] = []
    for url in feed_urls:
        import feedparser

        parsed = feedparser.parse(url)
        source = parsed.feed.get("title", url)
        for entry in parsed.entries[:per_feed_limit]:
            result.append(
                Item(
                    title=entry.get("title", "(no title)"),
                    link=entry.get("link", ""),
                    source=source,
                    published=entry.get("published", ""),
                    summary=_trim(entry.get("summary", "")),
                )
            )
    return _unique(result)


def fetch_arxiv(categories: list[str], max_results_per_category: int = 8) -> list[Item]:
    result: list[Item] = []
    for cat in categories:
        url = (
            "https://export.arxiv.org/api/query?"
            f"search_query=cat:{cat}&start=0&max_results={max_results_per_category}"
            "&sortBy=submittedDate&sortOrder=descending"
        )
        import feedparser

        parsed = feedparser.parse(url)
        for entry in parsed.entries:
            authors = ", ".join(a.get("name", "") for a in entry.get("authors", []))
            summary = _trim(entry.get("summary", ""))
            with_authors = f"作者: {authors}. 摘要: {summary}" if authors else f"摘要: {summary}"
            result.append(
                Item(
                    title=entry.get("title", "(no title)").replace("\n", " ").strip(),
                    link=entry.get("link", ""),
                    source=f"arXiv:{cat}",
                    published=entry.get("published", ""),
                    summary=with_authors,
                )
            )
    return _unique(result)


def render_report(news: list[Item], papers: list[Item], report_date: date | None = None) -> str:
    d = report_date or date.today()
    lines = [
        f"# AI Daily Radar - {d.isoformat()}",
        "",
        f"- 新闻条目: {len(news)}",
        f"- 论文条目: {len(papers)}",
        "",
        "## 📰 AI 热点新闻",
        "",
    ]

    if not news:
        lines.append("_今日无新闻数据_")
    else:
        for idx, item in enumerate(news, 1):
            lines.extend(
                [
                    f"### {idx}. {item.title}",
                    f"- 来源: {item.source}",
                    f"- 时间: {item.published or 'N/A'}",
                    f"- 链接: {item.link}",
                    f"- 摘要: {item.summary or 'N/A'}",
                    "",
                ]
            )

    lines.extend(["## 📄 最新研究论文", ""])
    if not papers:
        lines.append("_今日无论文数据_")
    else:
        for idx, item in enumerate(papers, 1):
            lines.extend(
                [
                    f"### {idx}. {item.title}",
                    f"- 来源: {item.source}",
                    f"- 时间: {item.published or 'N/A'}",
                    f"- 链接: {item.link}",
                    f"- 摘要: {item.summary or 'N/A'}",
                    "",
                ]
            )
    return "\n".join(lines).strip() + "\n"


def run(config_path: str | Path = "config/sources.yaml", output_dir: str | Path = "reports") -> Path:
    cfg = load_sources(config_path)
    news = fetch_news(cfg.get("news_feeds", []))
    arxiv_cfg = cfg.get("arxiv", {})
    papers = fetch_arxiv(
        arxiv_cfg.get("categories", []),
        int(arxiv_cfg.get("max_results_per_category", 8)),
    )

    content = render_report(news, papers)
    today = date.today().isoformat()
    output_path = Path(output_dir) / f"{today}-ai-daily.md"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return output_path
