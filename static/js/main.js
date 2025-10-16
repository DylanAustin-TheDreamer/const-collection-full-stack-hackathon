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
