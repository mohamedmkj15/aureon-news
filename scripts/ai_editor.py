import json
import os
import sys
from pathlib import Path

import urllib.request
import urllib.error


ROOT = Path(__file__).resolve().parent.parent

NEWS_FILE = ROOT / "data" / "news.json"


SYSTEM_PROMPT = """
You are Aureon Editor.

You are an AI-assisted global news editor.

Your job is to transform information from multiple sources
into a concise, factual, original news summary.

Rules:

1. Never invent facts.
2. Never add information that is not supported.
3. Clearly distinguish confirmed information from uncertain information.
4. Do not copy source articles verbatim.
5. Preserve source attribution.
6. Do not exaggerate.
7. Do not use sensational headlines.
8. Keep the language concise and professional.
9. If sources disagree, mention the disagreement.
10. If information is insufficient, say that it is developing.

Return valid JSON only.

Required fields:

{
  "headline": "...",
  "summary": "...",
  "key_facts": [],
  "status": "confirmed|developing|unconfirmed",
  "confidence": 0
}
"""


def load_articles():

    with open(
        NEWS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_articles(articles):

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


def build_prompt(story):

    sources = []

    for article in story:

        sources.append({
            "source": article.get(
                "source",
                ""
            ),
            "title": article.get(
                "title",
                ""
            ),
            "summary": article.get(
                "summary",
                ""
            ),
            "url": article.get(
                "url",
                ""
            )
        })

    return json.dumps(
        {
            "task": "Analyze this news story.",
            "sources": sources
        },
        ensure_ascii=False
    )


def call_ai(prompt):

    api_url = os.getenv(
        "AI_API_URL"
    )

    api_key = os.getenv(
        "AI_API_KEY"
    )

    model = os.getenv(
        "AI_MODEL",
        "default"
    )

    if not api_url or not api_key:

        print(
            "AI credentials are not configured."
        )

        return None

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1
    }

    data = json.dumps(
        payload
    ).encode("utf-8")

    request = urllib.request.Request(
        api_url,
        data=data,
        headers={
            "Content-Type":
                "application/json",
            "Authorization":
                f"Bearer {api_key}"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=60
        ) as response:

            result = json.loads(
                response.read()
            )

            return result

    except urllib.error.HTTPError as error:

        print(
            "AI API error:",
            error.code
        )

        return None

    except Exception as error:

        print(
            "AI request failed:",
            error
        )

        return None


def group_by_story(articles):

    groups = {}

    for article in articles:

        story_id = article.get(
            "story_id",
            article["id"]
        )

        groups.setdefault(
            story_id,
            []
        ).append(article)

    return groups


def apply_editor_output(
    story,
    output
):

    if not output:
        return

    story[0]["ai"] = output

    story[0]["title"] = (
        output.get(
            "headline",
            story[0]["title"]
        )
    )

    story[0]["summary"] = (
        output.get(
            "summary",
            story[0]["summary"]
        )
    )

    story[0]["status"] = (
        output.get(
            "status",
            "developing"
        )
    )


def main():

    articles = load_articles()

    groups = group_by_story(
        articles
    )

    edited = 0

    for story_id, story in groups.items():

        if len(story) == 0:
            continue

        print(
            f"Editing {story_id}"
        )

        prompt = build_prompt(
            story
        )

        result = call_ai(
            prompt
          When multiple timestamps are available,
build a chronological timeline.

Do not invent timeline events.

Only use events supported by the provided sources.
        )

        if not result:
            continue

        apply_editor_output(
            story,
            result
        )

        edited += 1

    save_articles(
        articles
    )

    print(
        f"AI edited {edited} stories."
    )


if __name__ == "__main__":
    main()
