import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import feedparser


ROOT = Path(__file__).resolve().parent.parent

SOURCES_FILE = ROOT / "data" / "sources.json"
NEWS_FILE = ROOT / "data" / "news.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )


def create_id(url):
    return hashlib.sha256(
        url.encode("utf-8")
    ).hexdigest()[:16]


def parse_date(entry):
    published = entry.get("published_parsed")

    if published:
        dt = datetime(
            *published[:6],
            tzinfo=timezone.utc
        )

        return dt.isoformat()

    return datetime.now(timezone.utc).isoformat()


def collect_source(source):

    feed = feedparser.parse(source["rss"])

    articles = []

    for entry in feed.entries[:20]:

        url = entry.get("link")

        if not url:
            continue

        title = entry.get("title", "").strip()

        if not title:
            continue

        summary = (
            entry.get("summary")
            or entry.get("description")
            or ""
        )

        article = {
            "id": create_id(url),
            "title": title,
            "summary": summary,
            "category": source["category"],
            "source": source["name"],
            "url": url,
            "published_at": parse_date(entry)
        }

        articles.append(article)

    return articles


def main():

    sources = load_json(SOURCES_FILE)

    try:
        existing = load_json(NEWS_FILE)
    except FileNotFoundError:
        existing = []

    existing_ids = {
        article["id"]
        for article in existing
    }

    new_articles = []

    for source in sources:

        print(
            f"Collecting: "
            f"{source['name']}"
        )

        try:

            articles = collect_source(source)

            for article in articles:

                if article["id"] not in existing_ids:

                    new_articles.append(article)
                    existing_ids.add(article["id"])

        except Exception as error:

            print(
                f"Source failed: "
                f"{source['name']} "
                f"→ {error}"
            )

    combined = (
        new_articles
        + existing
    )

    combined.sort(
        key=lambda article:
            article.get("published_at", ""),
        reverse=True
    )

    combined = combined[:500]

    save_json(
        NEWS_FILE,
        combined
    )

    print(
        f"Added {len(new_articles)} "
        f"new articles."
    )


if __name__ == "__main__":
    main()
