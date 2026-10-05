async function loadStory() {

    const params =
        new URLSearchParams(
            window.location.search
        );

    const storyId =
        params.get("id");

    const container =
        document.getElementById(
            "story-container"
        );

    if (!storyId) {

        container.innerHTML =
            "<h1>Story not found.</h1>";

        return;
    }

    try {

        const response =
            await fetch(
                "data/news.json"
            );

        const articles =
            await response.json();

        const article =
            articles.find(
                item =>
                    item.story_id === storyId ||
                    item.id === storyId
            );

        if (!article) {

            container.innerHTML =
                "<h1>Story not found.</h1>";

            return;
        }

        container.innerHTML = `

            <div class="story-category">
                ${escapeHTML(
                    article.category || "WORLD"
                )}
            </div>

            <h1 class="story-title">
                ${escapeHTML(article.title)}
            </h1>

            <p class="story-summary">
                ${escapeHTML(article.summary || "")}
            </p>

            <div class="story-source">

                Source:
                ${escapeHTML(
                    article.source || "Unknown"
                )}

            </div>

            <a
                href="${safeURL(article.url)}"
                target="_blank"
                rel="noopener noreferrer"
                class="read-more"
            >
                Read original source →
            </a>

        `;

    } catch (error) {

        console.error(error);

        container.innerHTML =
            "<h1>Unable to load story.</h1>";
    }
}


function escapeHTML(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function safeURL(value) {

    try {

        const url = new URL(value);

        if (
            url.protocol === "http:" ||
            url.protocol === "https:"
        ) {
            return url.href;
        }

    } catch (error) {}

    return "#";
}


loadStory("sources": [
    {
        "name": "Source A",
        "url": "https://example.com"
    },
    {
        "name": "Source B",
        "url": "https://example.com"
    }
]);
