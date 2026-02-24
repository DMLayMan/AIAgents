from datetime import date

from src.ai_daily_radar import Item, _trim, render_report


def test_trim_should_truncate_long_text():
    text = "a" * 300
    out = _trim(text, max_len=20)
    assert out.endswith("...")
    assert len(out) == 20


def test_render_report_basic():
    news = [
        Item(
            title="News A",
            link="https://example.com/news-a",
            source="ExampleNews",
            published="2026-02-24",
            summary="summary",
        )
    ]
    papers = [
        Item(
            title="Paper A",
            link="https://arxiv.org/abs/1234.5678",
            source="arXiv:cs.AI",
            published="2026-02-24",
            summary="paper summary",
        )
    ]

    report = render_report(news, papers, report_date=date(2026, 2, 24))
    assert "AI Daily Radar - 2026-02-24" in report
    assert "## 📰 AI 热点新闻" in report
    assert "## 📄 最新研究论文" in report
    assert "News A" in report
    assert "Paper A" in report
