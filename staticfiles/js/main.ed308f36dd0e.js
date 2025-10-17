// Minimal placeholder JS
console.log('main.js loaded');

/**
 * Update the basket count in the navigation bar
 * This function fetches the current basket item count from the server
 * and updates the badge in the navbar
 */
function updateBasketCount() {
    // Check if the basket count element exists (only for authenticated users)
    const basketCountElement = document.getElementById('basket-count');
    if (!basketCountElement) {
        return; // User is not authenticated, skip
    }

    // Fetch basket count from the server
    fetch('/basket/count/')
        .then(response => response.json())
        .then(data => {
            // Update the badge with the item count
            basketCountElement.textContent = data.count;
            
            // Hide badge if count is 0
            if (data.count === 0) {
                basketCountElement.style.display = 'none';
            } else {
                basketCountElement.style.display = 'inline-block';
            }
        })
        .catch(error => {
            console.error('Error fetching basket count:', error);
        });
}

// Update basket count when the page loads
document.addEventListener('DOMContentLoaded', function() {
    updateBasketCount();
});

// Export the function so it can be called from other pages
window.updateBasketCount = updateBasketCount;


/**
 * Shows a toast notification message to the user (moved from base.html)
 */
let currentToast = null;
let toastTimeout = null;

function showToast(message, type = 'success') {
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) return;

    if (currentToast) {
        currentToast.remove();
        clearTimeout(toastTimeout);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-header">
            <strong class="me-auto text-primary">${type === 'success' ? 'Success' : 'Error'}</strong>
            <button type="button" class="btn-close" onclick="this.closest('.toast').remove()"></button>
        </div>
        <div class="toast-body">${message}</div>
    `;

    toastContainer.appendChild(toast);
    currentToast = toast;

    requestAnimationFrame(() => toast.classList.add('show'));

    toastTimeout = setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentNode) toast.remove();
            if (currentToast === toast) currentToast = null;
        }, 300);
    }, 3000);
}

window.showToast = showToast;

/**
 * Build a normalized toast message including title, variant and price.
 * Example: "Added 'The Three Graces' (Original piece) — $1,000,000.00"
 */
function buildToastMessage(title, variantLabel, price, action = 'Added') {
    let parts = [];
    if (title) parts.push(`'${title}'`);
    if (variantLabel) parts.push(`(${variantLabel})`);

    let pricePart = '';
    if (price || price === 0) {
        let p = Number(price);
        if (!isNaN(p)) {
            pricePart = `— $${p.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
        }
    }

    const main = parts.length ? parts.join(' ') : '';
    if (main) return `${action} ${main} ${pricePart}`.trim();
    return `${action}`;
}

window.buildToastMessage = buildToastMessage;

/**
 * Attach add-to-basket form handler if present on the page.
 * Centralizes the AJAX add flow and toast formatting.
 */
function initAddToBasketForm() {
    const form = document.getElementById('add-to-basket-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const btn = document.getElementById('add-to-basket-btn');
        if (btn) btn.disabled = true;

        // Copy top radio selection into hidden variant_id before sending
        const topSelected = document.querySelector('input[name="variant_top"]:checked');
        const hiddenVariantInput = document.getElementById('add-to-basket-variant-id');
        if (topSelected && hiddenVariantInput) {
            hiddenVariantInput.value = topSelected.value;
        }

        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let variantLabel = '';
                let variantPrice = null;
                // Primary: if the form contains an actual radio named variant_id (older markup), use it
                let selected = form.querySelector('input[name="variant_id"]:checked');
                if (!selected) {
                    // Fallback: use the top radio selectors
                    selected = document.querySelector('input[name="variant_top"]:checked');
                }
                if (selected) {
                    // attempt to find a label by id (top radios use id like top-variant-<pk>)
                    const lbl = document.querySelector(`label[for="${selected.id}"]`) || form.querySelector(`label[for="${selected.id}"]`) || selected.closest('label');
                    if (lbl) variantLabel = lbl.textContent.trim();

                    // Prefer data attributes on the radio for price/currency
                    if (selected.dataset && selected.dataset.price) {
                        variantPrice = selected.dataset.price || null;
                    } else {
                        // Fallback: try to read a DOM element that contains price
                        const inputPrice = document.getElementById(`variant-price-${selected.value}`);
                        if (inputPrice) variantPrice = inputPrice.value || null;
                    }
                }

                const artTitle = form.dataset.artTitle || document.title;
                const toastMsg = buildToastMessage(artTitle, variantLabel, variantPrice, 'Added');
                showToast(toastMsg, 'success');
                updateBasketCount();
            } else {
                showToast('Failed to add to basket. Please try again.', 'error');
            }
        })
        .catch(() => {
            showToast('An error occurred. Please try again.', 'error');
        })
        .finally(() => {
            if (btn) btn.disabled = false;
        });
    });
}

/**
 * Sync main price display (#main-price and #main-currency) from selected variant_top radios.
 */
function initVariantPriceSync() {
    const updateMainPrice = () => {
        const sel = document.querySelector('input[name="variant_top"]:checked');
        const mainPriceEl = document.getElementById('main-price');
        const mainCurrencyEl = document.getElementById('main-currency');
        if (!sel || !mainPriceEl) return;
        const p = sel.dataset.price;
        const c = sel.dataset.currency || (mainCurrencyEl ? mainCurrencyEl.textContent : '');
        if (p !== undefined && p !== null && p !== '') {
            // format number to 2 decimals and include thousands separators
            const num = Number(p);
            if (!isNaN(num)) {
                mainPriceEl.textContent = num.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
            } else {
                mainPriceEl.textContent = p;
            }
        }
        if (mainCurrencyEl && c) mainCurrencyEl.textContent = c;
    };

    // update on change
    document.addEventListener('change', function (e) {
        if (e.target && e.target.name === 'variant_top') updateMainPrice();
    });

    // update on load
    document.addEventListener('DOMContentLoaded', updateMainPrice);
}

// initialize price sync alongside form handler
document.addEventListener('DOMContentLoaded', function() {
    initVariantPriceSync();
});

/**
 * Hydration fallback for artwork list page.
 * Some browsers (or navigation patterns) load a cached snapshot that can
 * omit server-rendered dynamic blocks. If the featured block or filters
 * are missing after navigation, fetch the list page and patch the DOM
 * non-destructively.
 */
function hydrateArtworkListIfNeeded() {
    try {
        const featured = document.getElementById('featured-artworks');
        const filters = document.getElementById('artwork-filters-form');
        // if both exist, nothing to do
        if (featured && filters) return;

        // build the URL for the current list (preserve current querystring)
        const url = new URL(window.location.href);
        // ensure we're on the artwork list route (quick safety)
        if (!url.pathname.endsWith('/artworks/') && !url.pathname.endsWith('/artworks')) return;

        fetch(url.toString(), { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.text())
            .then(html => {
                // parse returned HTML and extract the parts we need
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const remoteFeatured = doc.getElementById('featured-artworks');
                const remoteFilters = doc.getElementById('artwork-filters-form');

                if (remoteFeatured && !featured) {
                    // insert featured block at the same position as in template: before the filters row
                    const containerRow = document.querySelector('.container > .row.mb-4');
                    if (containerRow) {
                        containerRow.parentNode.insertBefore(remoteFeatured, containerRow.nextSibling);
                    } else {
                        // fallback: append to top of container
                        const container = document.querySelector('.container');
                        if (container) container.insertBefore(remoteFeatured, container.firstChild);
                    }
                }

                if (remoteFilters && !filters) {
                    // find the card that previously contained the filters and insert
                    const card = document.querySelector('.card .card-body');
                    if (card) {
                        // replace inner HTML of card-body with the remote content of the form area
                        const remoteForm = remoteFilters.cloneNode(true);
                        // try to find the form wrapper inside card-body
                        const existingForm = card.querySelector('form');
                        if (existingForm) {
                            existingForm.parentNode.replaceChild(remoteForm, existingForm);
                        } else {
                            card.appendChild(remoteForm);
                        }
                    }
                }
            })
            .catch(err => {
                // non-fatal
                console.debug('hydrateArtworkListIfNeeded error:', err);
            });
    } catch (e) {
        console.debug('hydrateArtworkListIfNeeded exception', e);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    hydrateArtworkListIfNeeded();
});

/**
 * Basket quantity helpers
 */
function updateQuantity(itemId) {
    const form = document.querySelector(`#basket-item-${itemId} .update-quantity-form`);
    if (form) form.submit();
}

function incrementQuantity(itemId) {
    const input = document.getElementById(`quantity-${itemId}`);
    if (!input) return;
    const currentValue = parseInt(input.value) || 0;
    const maxValue = parseInt(input.max) || 9999;
    if (currentValue < maxValue) {
        input.value = currentValue + 1;
        updateQuantity(itemId);
    }
}

function decrementQuantity(itemId) {
    const input = document.getElementById(`quantity-${itemId}`);
    if (!input) return;
    const currentValue = parseInt(input.value) || 0;
    if (currentValue > 1) {
        input.value = currentValue - 1;
        updateQuantity(itemId);
    } else if (currentValue === 1) {
        if (confirm('Remove this item from your basket?')) {
            input.value = 0;
            updateQuantity(itemId);
        }
    }
}

// Attach input change handlers for quantity inputs (delegated on DOMContentLoaded)
document.addEventListener('DOMContentLoaded', function() {
    initAddToBasketForm();

    document.querySelectorAll('input[name="quantity"]').forEach(input => {
        input.addEventListener('change', function() {
            const parts = this.id.split('-');
            const itemId = parts[1];
            if (itemId) updateQuantity(itemId);
        });
    });
});
