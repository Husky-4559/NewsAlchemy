window.addEventListener("DOMContentLoaded", () => {
	fetchNews("general");

	const searchButton = document.getElementById("search-button");
	const searchText = document.getElementById("search-text");

	if (searchButton && searchText) {
		searchButton.addEventListener("click", () => {
			const query = searchText.value;
			if (!query) return;
			fetchNews(query);
			curSelectedNav?.classList.remove("active");
			curSelectedNav = null;
		});
	}

	const loginLink = document.querySelector('a.nav-link[href*="login"]');
	const registerLink = document.querySelector('a.nav-link[href*="register"]');

	if (loginLink) {
		loginLink.addEventListener("click", (event) => {
			event.preventDefault();
			window.location.href = loginLink.href;
		});
	}

	if (registerLink) {
		registerLink.addEventListener("click", (event) => {
			event.preventDefault();
			window.location.href = registerLink.href;
		});
	}
});

async function fetchNews(query) {
	const url = `/fetch_news?category=${query}`;
	try {
		const res = await fetch(url);
		const data = await res.json();
		bindData(data);
	} catch (error) {
		console.error("Failed to fetch news:", error);
		// Log the response text for debugging
		try {
			const resText = await res.text();
			console.error("Response text:", resText);
		} catch (e) {
			console.error("Failed to read response text:", e);
		}
	}
}

function bindData(articles) {
	const cardsContainer = document.getElementById("news-container");
	cardsContainer.innerHTML = "";

	articles.forEach((article) => {
		const cardClone = document.createElement("div");
		cardClone.className = "col-lg-4 col-md-6 mb-4";
		fillDataInCard(cardClone, article);
		cardsContainer.appendChild(cardClone);
	});
}

function fillDataInCard(cardClone, article) {
	cardClone.innerHTML = `
        <div class="card h-100">
            <div class="card-body">
                <h5 class="card-title"><a href="${article.url}" target="_blank">${article.title}</a></h5>
                <p class="card-author"><strong>Author/Source:</strong> ${article.author}</p>
            </div>
        </div>
    `;
}

let curSelectedNav = null;
function onNavItemClick(category) {
	fetchNews(category);
	const navItem = document.querySelector(
		`a[onclick="onNavItemClick('${category}')"]`
	);
	curSelectedNav?.classList.remove("active");
	curSelectedNav = navItem;
	curSelectedNav.classList.add("active");
}
