// INDEX & LOGIN
document.addEventListener('DOMContentLoaded', () => {
    fetchPlaces(getCookie('token'));

    // 2. Affiche/masque le bouton login
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        if (!getCookie('token')) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
        }
    }

    // Boutons détails
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('details-button')) {
            const id = e.target.getAttribute('data-id');
            window.location.href = `place.html?id=${id}`;
        }
    });

    // login.html
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    // Filtre prix
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const maxPrice = event.target.value;
            let filtered = loadedPlaces;
            if (maxPrice !== "All") {
                filtered = loadedPlaces.filter(place => place.price <= Number(maxPrice));
            }
            displayPlaces(filtered);
        });
    }
});

async function loginUser(email, password) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            const data = await response.json();
            alert('Login failed: ' + (data.msg || response.statusText));
        }
    } catch (error) {
        console.error("Erreur :", error);
        alert('Login failed: Network error');
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

let loadedPlaces = [];

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/places/', {
            headers: token ? { "Authorization": `Bearer ${token}` } : {}
        });
        if (response.ok) {
            const places = await response.json();
            loadedPlaces = places;
            displayPlaces(places);
        } else {
            document.getElementById('places-list').innerHTML = "<p>Erreur lors du chargement des lieux.</p>";
        }
    } catch (error) {
        console.error("Erreur fetch:", error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    placesList.innerHTML = '';
    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.innerHTML = `
            <h3>${place.title || place.name}</h3>
            <p>Price per night: <b>€${place.price}</b></p>
            <button class="details-button" data-id="${place.id}">View Details</button>`;
        placesList.appendChild(card);
    });
}

// DETAILS (place.html)
document.addEventListener('DOMContentLoaded', async () => {
    if (!window.location.pathname.endsWith('place.html')) return;

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (!placeId) {
        document.getElementById('place-details').innerHTML = "<p>Erreur : pas d'ID trouvé dans l'URL</p>";
        return;
    }

    const token = getCookie('token');

    // Cache review si pas connecté
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    try {
        // Récup infos de la place
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            headers: token ? { "Authorization": `Bearer ${token}` } : {}
        });
        if (response.ok) {
            const place = await response.json();
            // gestion amenities
            let amenities = "";
            if (Array.isArray(place.amenities)) {
                amenities = place.amenities.map(a => typeof a === "object" ? a.name : a).join(', ');
            }
            document.getElementById('place-details').innerHTML = `
                <h1 style="text-align:center; margin-bottom:2rem;">${place.title || place.name}</h1>
                <div class="place-card" style="margin:0 auto; max-width:850px; text-align:center;">
                    <p><b>Host:</b> ${place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : "Unknown"}</p>
                    <p><b>Price per night:</b> €${place.price}</p>
                    <p><b>Description:</b> ${place.description || ""}</p>
                    <p><b>Amenities:</b> ${amenities}</p>
                </div>
            `;
            fetchAndDisplayReviews(placeId, token);
        } else {
            document.getElementById('place-details').innerHTML = "<p>Erreur : place introuvable</p>";
        }
    } catch (err) {
        document.getElementById('place-details').innerHTML = "<p>Erreur lors du chargement</p>";
    }

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const reviewText = document.getElementById('review-text').value;
            const reviewRating = document.getElementById('review-rating').value;
            await submitReview(token, placeId, reviewText, reviewRating, reviewForm);
        });
    }
});

// Affiche les reviews
async function fetchAndDisplayReviews(placeId, token) {
    try {
        const resp = await fetch(`http://localhost:5000/api/v1/reviews/places/${placeId}/reviews`, {
            headers: token ? { "Authorization": `Bearer ${token}` } : {}
        });
        const reviewsList = document.getElementById('reviews-list');
        if (resp.ok) {
            const reviews = await resp.json();
            if (reviews.length === 0) {
                reviewsList.innerHTML = `
                    <h2 class="reviews-title">Reviews</h2>
                    <p style='text-align:center; color:#aaa;'>No reviews yet.</p>
                `;
                return;
            }

            let reviewsHTML = `<h2 class="reviews-title">Reviews</h2>`;
            reviews.forEach(review => {
                reviewsHTML += `
                    <div class="review-card">
                        <p><b>${review.user_name || "Anonymous"}:</b></p>
                        <p>${review.text || "No comment."}</p>
                        <p>Rating: ${renderStars(review.rating)}</p>
                    </div>
                `;
            });
            reviewsList.innerHTML = reviewsHTML;
        } else {
            reviewsList.innerHTML = `
                <h2 class="reviews-title">Reviews</h2>
                <p>Erreur lors du chargement des avis.</p>
            `;
        }
    } catch (err) {
        document.getElementById('reviews-list').innerHTML = `
            <h2 class="reviews-title">Reviews</h2>
            <p>Erreur réseau reviews.</p>
        `;
    }
}

// REVIEWS

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function submitReview(token, placeId, reviewText, reviewRating, reviewForm) {
    try {
        const resp = await fetch('http://localhost:5000/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: Number(reviewRating),
                place_id: placeId
            })
        });

        if (resp.ok) {
            alert('Review submitted successfully!');
            reviewForm.reset();
            // Recharge les reviews pour afficher la nouvelle
            const placeId = getPlaceIdFromURL();
            const token = getCookie('token');
            fetchAndDisplayReviews(placeId, token);
        } else {
            const data = await resp.json();
            console.error('Error response:', data);
            alert('Failed to submit review: ' + JSON.stringify(data));
        }
    } catch (error) {
        alert('Failed to submit review: Network error');
    }
}

// Affiche des étoiles du rating
function renderStars(note) {
    note = Math.round(Number(note)) || 0;
    return "★".repeat(note) + "☆".repeat(5 - note);
}
