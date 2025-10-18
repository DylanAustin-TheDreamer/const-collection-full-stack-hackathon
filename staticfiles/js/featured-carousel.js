// Simple carousel logic for featured artworks
(function () {
  function initFeaturedCarousel() {
    const carousel = document.getElementById('featured-carousel');
    if (!carousel) return;

    const track = carousel.querySelector('.featured-track');
    const prev = carousel.querySelector('[data-action="prev"]');
    const next = carousel.querySelector('[data-action="next"]');

    function scrollByCards(direction) {
      if (!track) return;
      const wrapper = track.querySelector('.featured-card-wrapper');
      // Use index-based navigation to avoid skipping cards due to rounding or partial visibility.
      const cards = Array.from(track.querySelectorAll('.featured-card-wrapper'));
      if (!cards.length) return;

      // Find the card whose left edge is nearest to current scrollLeft
      const currentScroll = track.scrollLeft;
      let currentIndex = 0;
      let smallestDelta = Infinity;
      cards.forEach(function (card, idx) {
        const cardLeft = Math.round(card.offsetLeft);
        const delta = Math.abs(cardLeft - currentScroll);
        if (delta < smallestDelta) {
          smallestDelta = delta;
          currentIndex = idx;
        }
      });

      const increment = direction === 'next' ? 1 : -1;
      const nextIndex = (currentIndex + increment + cards.length) % cards.length;
      const targetCard = cards[nextIndex];
      const target = Math.round(targetCard.offsetLeft);

      track.scrollTo({ left: target, behavior: 'smooth' });
    }

  if (prev) prev.addEventListener('click', function () { scrollByCards('prev'); resetAutoplay(); });
  if (next) next.addEventListener('click', function () { scrollByCards('next'); resetAutoplay(); });

    // Optional: allow arrow keys when hovering the carousel
    carousel.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { scrollByCards('prev'); resetAutoplay(); }
      if (e.key === 'ArrowRight') { scrollByCards('next'); resetAutoplay(); }
    });

    // Autoplay: advance every 6 seconds
    let autoplayInterval = 6000; // ms
    let autoplayTimer = null;

    function startAutoplay() {
      if (autoplayTimer) return;
      autoplayTimer = setInterval(function () {
        scrollByCards('next');
      }, autoplayInterval);
    }

    function stopAutoplay() {
      if (!autoplayTimer) return;
      clearInterval(autoplayTimer);
      autoplayTimer = null;
    }

    function resetAutoplay() {
      stopAutoplay();
      // restart after a short delay to avoid immediate auto-scroll after manual action
      setTimeout(startAutoplay, 1000);
    }

    // Pause on hover/focus
    carousel.addEventListener('mouseenter', stopAutoplay);
    carousel.addEventListener('mouseleave', startAutoplay);
    carousel.addEventListener('focusin', stopAutoplay);
    carousel.addEventListener('focusout', startAutoplay);

    // Start autoplay initially
    startAutoplay();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFeaturedCarousel);
  } else {
    initFeaturedCarousel();
  }
})();
