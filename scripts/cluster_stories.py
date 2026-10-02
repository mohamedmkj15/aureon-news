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
    "has",
    "new"
}


def words(text):

    tokens = re.findall(
        r"[a-zA-Z0-9]+",
        text.lower()
    )

    return {
        token
        for token in tokens
        if len(token) >= 4
        and token not in STOPWORDS
    }


def similarity(text_a, text_b):

    a = words(text_a)
    b = words(text_b)

    if not a or not b:
        return 0

    return len(a & b) / len(a | b)


def build_clusters(articles):

    clusters = []
    assigned = set()

    for article in articles:

        if article["id"] in assigned:
            continue

        cluster = [article]

        assigned.add(article["id"])

        for candidate in articles:

            if candidate["id"] in assigned:
                continue

            score = similarity(
                article["title"],
                candidate["title"]
            )

            if score >= 0.35:

                cluster.append(candidate)

                assigned.add(
                    candidate["id"]
                )

        clusters.append(cluster)

    return clusters


def main():

    with open(
        NEWS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        articles = json.load(file)

    clusters = build_clusters(
        articles
    )

    cluster_lookup = {}

    for index, cluster in enumerate(
        clusters,
        start=1
    ):

        story_id = (
            f"story-{index:06d}"
        )

        for article in cluster:

            cluster_lookup[
                article["id"]
            ] = story_id

    for article in articles:

        article["story_id"] = (
            cluster_lookup[
                article["id"]
            ]
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
        f"Created {len(clusters)} story clusters."
    )


if __name__ == "__main__":
    main()
