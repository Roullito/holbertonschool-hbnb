// INDEX & LOGIN
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

    // Boutons détails sur index.html (cas statique ou généré dynamiquement)
    document.querySelectorAll('.details-button').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            window.location.href = `place.html?id=${id}`;
        });
    });

    // Formulaire de login (login.html)
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    // Filtre prix sur index.html
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

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
            fetchPlaces(token);
        }
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
    // (Ré)active les écouteurs sur les nouveaux boutons générés dynamiquement
    document.querySelectorAll('.details-button').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            window.location.href = `place.html?id=${id}`;
        });
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
    try {
        // Récup infos de la place
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            headers: token ? { "Authorization": `Bearer ${token}` } : {}
        });
        if (response.ok) {
            const place = await response.json();
            // gestion des amenities
            let amenities = "";
            if (Array.isArray(place.amenities)) {
                amenities = place.amenities.map(a => typeof a === "object" ? a.name : a).join(', ');
            }
            document.getElementById('place-details').innerHTML = `
                <h1 style="text-align:center; margin-bottom:2rem;">${place.title || place.name}</h1>
                <div class="place-card" style="margin:0 auto; max-width:850px; text-align:center;">
                    <p><b>Host:</b> ${place.host || place.owner_name || "Unknown"}</p>
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
});

// Affiche les reviews dynamiquement
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
                        <p><b>${review.author_name || review.user_name || "Anonymous"}:</b></p>
                        <p>${review.text || review.content || review.comment || "No comment."}</p>
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

// Affiche des étoiles du rating (integer 0-5)
function renderStars(note) {
    note = Math.round(Number(note)) || 0;
    return "★".repeat(note) + "☆".repeat(5 - note);
}
