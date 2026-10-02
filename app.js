async function loadNews() {
    try {
        const response = await fetch("data/news.json");

        if (!response.ok) {
            throw new Error("Unable to load news data.");
        }

        const news = await response.json();

        renderNews(news);

    } catch (error) {
        console.error("Aureon error:", error);
    }
}


function renderNews(news) {

    const container = document.getElementById("news-container");

    if (!container) {
        return;
    }

    container.innerHTML = "";

    news
        .slice(0, 12)
        .forEach(article => {

            const card = document.createElement("article");

            card.className = "news-card";

            card.innerHTML = `
                <div class="news-meta">
                    <span>${escapeHTML(article.category)}</span>
                    <span>${escapeHTML(article.source)}</span>
                </div>

                <h3>
                    ${escapeHTML(article.title)}
                </h3>

                <p>
                    ${escapeHTML(article.summary)}
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
            url.protocol === "http:" ||
            url.protocol === "https:"
        ) {
            return url.href;
        }

    } catch (_) {}

    return "#";
}


loadNews();
