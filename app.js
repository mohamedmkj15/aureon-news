async function loadNews() {
    const container = document.getElementById("news-container");

    try {
        const response = await fetch("data/news.json");

        if (!response.ok) {
            throw new Error("Failed to load news.");
        }

        const articles = await response.json();

        renderNews(articles);

    } catch (error) {

        console.error("Aureon:", error);

        container.innerHTML = `
            <div class="error-message">
                Unable to load Aureon intelligence.
            </div>
        `;
    }
}


function renderNews(articles) {

    const container =
        document.getElementById("news-container");

    container.innerHTML = "";

    const params =
    new URLSearchParams(
        window.location.search
    );

const selectedCategory =
    params.get("category");

let visibleArticles =
    articles.filter(
        article => article.title
    );

if (selectedCategory) {

    visibleArticles =
        visibleArticles.filter(
            article =>
                article.category ===
                selectedCategory
        );
}

visibleArticles =
    visibleArticles.slice(0, 12);

    visibleArticles.forEach(article => {

        const card =
            document.createElement("article");

        card.className = "news-card";

        card.innerHTML = `

            <div class="news-meta">

                <span>
                    ${escapeHTML(
                        article.category || "WORLD"
                    )}
                </span>

                <span>
                    ${escapeHTML(
                        article.source || "AUREON"
                    )}
                </span>

            </div>

            <h3>
                ${escapeHTML(article.title)}
            </h3>

            <p>
                ${escapeHTML(
                    article.summary || ""
                )}
            </p>

            <a
                href="${safeURL(article.url)}"
                target="_blank"
                rel="noopener noreferrer"
                class="read-more"
            >
                Read source →
            </a>

        `;

        container.appendChild(card);
    });
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
            url.protocol === "https:" ||
            url.protocol === "http:"
        ) {
            return url.href;
        }

    } catch (error) {}

    return "#";
}


loadNews();
const searchInput =
    document.getElementById(
        "search-input"
    );

if (searchInput) {

    searchInput.addEventListener(
        "input",
        async function () {

            const query =
                this.value
                    .toLowerCase()
                    .trim();

            const response =
                await fetch(
                    "data/news.json"
                );

            const articles =
                await response.json();

            const results =
                articles.filter(article => {

                    const text =
                        `
                        ${article.title}
                        ${article.summary}
                        ${article.category}
                        ${article.source}
                        `
                        .toLowerCase();

                    return text.includes(query);
                });

            renderNews(results);
        }
    );
}
function formatDate(dateString) {

    if (!dateString) {
        return "Unknown time";
    }

    const date = <span>
    ${formatDate(article.published_at)}
</span>
        new Date(dateString);

    return new Intl.DateTimeFormat(
        "en",
        {
            dateStyle: "medium",
            timeStyle: "short"
        }
    ).format(date);
}
