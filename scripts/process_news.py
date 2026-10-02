import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
NEWS_FILE = ROOT / "data" / "news.json"


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "after",
    "over",
    "will",
    "have",
    "has"
}


def tokenize(text):

    words = re.findall(
        r"[a-zA-Z0-9]+",
        text.lower()
    )

    return {
        word
        for word in words
        if len(word) > 2
        and word not in STOPWORDS
    }


def similarity(a, b):

    words_a = tokenize(a)
    words_b = tokenize(b)

    if not words_a or not words_b:
        return 0

    intersection = words_a & words_b
    union = words_a | words_b

    return len(intersection) / len(union)


def process_articles(articles):

    for article in articles:

        text = (
            article["title"]
            + " "
            + article.get("summary", "")
        )

        article["keywords"] = list(
            tokenize(text)
        )[:20]

        article["status"] = "developing"

    return articles


def main():

    with open(
        NEWS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        articles = json.load(file)

    articles = process_articles(
        articles
    )

    with open(
        NEWS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            articles,
            file,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Processed {len(articles)} articles."
    )


if __name__ == "__main__":
    main()
