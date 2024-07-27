window.addEventListener("DOMContentLoaded", () => {
	let currentPage = 1;
	let currentCategory = "general";

	fetchNews(currentCategory, currentPage);

	const searchButton = document.getElementById("search-button");
	const searchText = document.getElementById("search-text");
	const loadMoreButton = document.getElementById("load-more-button");

	if (searchButton && searchText) {
		searchButton.addEventListener("click", () => {
			const query = searchText.value;
			if (!query) return;
			currentCategory = query;
			currentPage = 1;
			fetchNews(currentCategory, currentPage, true);
		});
	}

	document.querySelectorAll(".nav-link").forEach((navLink) => {
		navLink.addEventListener("click", (event) => {
			const category = event.target.innerText.toLowerCase();
			if (
				["home", "sports", "entertainment", "technology"].includes(category)
			) {
				event.preventDefault();
				onNavItemClick(category);
			}
		});
	});

	if (loadMoreButton) {
		loadMoreButton.addEventListener("click", () => {
			currentPage++;
			fetchNews(currentCategory, currentPage);
		});
	}

	loadFavorites();
});

function onNavItemClick(category) {
	currentCategory = category;
	currentPage = 1;
	fetchNews(currentCategory, currentPage, true);
}

async function fetchNews(category, page, reset = false) {
	const url = `/fetch_news?category=${category}&page=${page}`;
	let res;
	try {
		res = await fetch(url);
		if (!res.ok) {
			throw new Error(`HTTP error! status: ${res.status}`);
		}
		const data = await res.json();
		bindData(data, reset);
	} catch (error) {
		console.error("Failed to fetch news:", error);
		try {
			const resText = await res.text();
			console.error("Response text:", resText);
		} catch (e) {
			console.error("Failed to read response text:", e);
		}
	}
}

function bindData(articles, reset = false) {
	const cardsContainer = document.getElementById("news-container");
	if (reset) {
		cardsContainer.innerHTML = "";
	}

	articles.forEach((article) => {
		const cardClone = document.createElement("div");
		cardClone.className = "col-lg-4 col-md-6 mb-4 news-card";
		fillDataInCard(cardClone, article);
		cardsContainer.appendChild(cardClone);
	});

	const loadMoreButton = document.getElementById("load-more-button");
	if (articles.length < 15) {
		loadMoreButton.style.display = "none";
	} else {
		loadMoreButton.style.display = "block";
	}
}

function fillDataInCard(cardClone, article) {
	cardClone.innerHTML = `
        <div class="card h-100">
            <div class="card-body">
                <h5 class="card-title"><a href="${
									article.url
								}" target="_blank">${article.title}</a></h5>
                <p class="card-author"><strong>Author/Source:</strong> ${
									article.author
								}</p>
                <button class="btn btn-primary" onclick="addToFavorites('${encodeURIComponent(
									article.title
								)}', '${encodeURIComponent(
		article.url
	)}')">Add to Favorites</button>
            </div>
        </div>
    `;
}

async function addToFavorites(title, url) {
	try {
		const response = await fetch(`/favorites`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				title: decodeURIComponent(title),
				url: decodeURIComponent(url),
			}),
		});

		if (response.ok) {
			const data = await response.json();
			if (data.success) {
				alert("Article added to favorites!");
				appendToFavorites(data.favorite);
			} else {
				if (data.message === "Article is already in favorites") {
					alert("This article is already in your favorites.");
				} else {
					alert("Failed to add article to favorites.");
				}
			}
		} else if (response.status === 401) {
			alert("You need to log in to add favorites.");
			window.location.href = "/auth/login";
		} else {
			alert("Failed to add article to favorites.");
		}
	} catch (error) {
		console.error("Error adding to favorites:", error);
		alert("An error occurred while adding the article to favorites.");
	}
}

async function loadFavorites() {
	try {
		const response = await fetch(`/favorites`);
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		const data = await response.json();
		if (data.success) {
			data.favorites.forEach((favorite) => appendToFavorites(favorite));
		} else {
			console.error("Failed to load favorites:", data.message);
		}
	} catch (error) {
		console.error("Error loading favorites:", error);
	}
}

function appendToFavorites(favorite) {
	const favoritesContainer = document.getElementById("favorites-container");
	if (!favoritesContainer) {
		console.error("Favorites container not found");
		return;
	}

	const favoriteCard = document.createElement("div");
	favoriteCard.className = "card my-3 reddit-style-card";
	favoriteCard.id = `favorite-${favorite.id}`;
	favoriteCard.innerHTML = `
        <div class="card-body">
            <h5>
                <a href="${favorite.url}" target="_blank">${favorite.title}</a>
            </h5>
            <button class="btn btn-danger" onclick="deleteFavorite(${favorite.id})">Delete</button>
        </div>
    `;
	favoritesContainer.appendChild(favoriteCard);
}

async function deleteFavorite(favoriteId) {
	try {
		const response = await fetch(`/favorites?id=${favoriteId}`, {
			method: "DELETE",
			credentials: "same-origin",
		});

		if (response.ok) {
			alert("Favorite deleted.");
			document.getElementById(`favorite-${favoriteId}`).remove();
		} else {
			alert("Failed to delete favorite.");
		}
	} catch (error) {
		console.error("Error deleting favorite:", error);
		alert("An error occurred while deleting the favorite.");
	}
}
