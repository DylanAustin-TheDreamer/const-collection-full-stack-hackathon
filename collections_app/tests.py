from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Collection, Art, ArtVariant
from owner_app.models import ArtistProfile


def create_artwork_equivalent(title, artist, **kwargs):
    """Helper for tests: create an Art and one ArtVariant (original) when
    a test would previously create an Artwork. Accepts kwargs like medium,
    width_cm, height_cm, depth_cm, price, currency, description,
    is_available, is_featured, year_created.
    """
    coll, _ = Collection.objects.get_or_create(
        artist=artist,
        name='Test',
    )
    art_fields = {
        'collection': coll,
        'title': title,
        'medium': kwargs.get('medium', ''),
        'width_cm': kwargs.get('width_cm'),
        'height_cm': kwargs.get('height_cm'),
        'depth_cm': kwargs.get('depth_cm'),
        'price': kwargs.get('price'),
        'currency': kwargs.get('currency', 'USD'),
        'description': kwargs.get('description', ''),
        'is_available': kwargs.get('is_available', False),
        'is_featured': kwargs.get('is_featured', False),
        'year_created': kwargs.get('year_created'),
    }
    # remove keys with None so model defaults apply
    art_fields = {k: v for k, v in art_fields.items() if v is not None}
    art = Art.objects.create(**art_fields)
    # create an original variant when a price is provided and available
    if kwargs.get('is_available') and kwargs.get('price') is not None:
        ArtVariant.objects.create(
            art=art,
            medium=ArtVariant.ORIGINAL,
            is_available=True,
            price=kwargs.get('price'),
            currency=kwargs.get('currency', 'USD'),
        )
    else:
        # create placeholders for completeness
        ArtVariant.objects.get_or_create(art=art, medium=ArtVariant.POSTER)
        ArtVariant.objects.get_or_create(art=art, medium=ArtVariant.DIGITAL)
    return art


# ============================================================================
# ARTWORK MODEL TESTS
# Tests for the Artwork model fields, methods, and validation
# ============================================================================

class ArtworkModelTest(TestCase):
    """
    Test suite for the Artwork model.
    Ensures that price, size, and medium fields work correctly.
    """
    
    def setUp(self):
        """
        Set up test data before each test method.
        Creates a test user, artist profile, and artwork.
        """
        # Create an artist profile (ArtistProfile doesn't have a user field)
        self.artist = ArtistProfile.objects.create(
            name='Test Artist',
            email='testartist@example.com',
            phone_number='123-456-7890',
            bio='Test bio for artist'
        )
        
        # Create a test Art with an available original variant
        coll, _ = Collection.objects.get_or_create(
            artist=self.artist,
            name='Test',
        )
        self.artwork = Art.objects.create(
            collection=coll,
            title='Test Artwork',
            medium='Oil on Canvas',
            width_cm=Decimal('50.00'),
            height_cm=Decimal('70.00'),
            depth_cm=Decimal('3.00'),
            price=Decimal('1500.00'),
            currency='USD',
            description='A beautiful test artwork',
            is_available=True,
        )
        ArtVariant.objects.create(
            art=self.artwork,
            medium=ArtVariant.ORIGINAL,
            is_available=True,
            price=Decimal('1500.00'),
            currency='USD',
        )
    
    def test_artwork_creation(self):
        """
        Test that an artwork can be created with all required fields.
        Verifies price, size, and medium are stored correctly.
        """
        self.assertEqual(self.artwork.title, 'Test Artwork')
        self.assertEqual(self.artwork.artist, self.artist)
        # Test medium field
        self.assertEqual(self.artwork.medium, 'Oil on Canvas')
        # Test size fields
        self.assertEqual(self.artwork.width_cm, Decimal('50.00'))
        self.assertEqual(self.artwork.height_cm, Decimal('70.00'))
        self.assertEqual(self.artwork.depth_cm, Decimal('3.00'))
        # Test price field
        self.assertEqual(self.artwork.price, Decimal('1500.00'))
        self.assertEqual(self.artwork.currency, 'USD')
    
    def test_artwork_string_representation(self):
        """
        Test the __str__ method returns the correct format.
        Should display: "Title by Artist"
        """
        expected_string = f"{self.artwork.title} by {self.artist}"
        self.assertEqual(str(self.artwork), expected_string)
    
    def test_get_size_display_2d_artwork(self):
        """
        Test get_size_display() method for 2D artworks.
        Should return formatted string: "Width x Height cm"
        """
        # Create a 2D artwork (no depth)
        artwork_2d = create_artwork_equivalent(
            '2D Artwork', self.artist,
            medium='Watercolor',
            width_cm=Decimal('30.00'),
            height_cm=Decimal('40.00'),
            price=Decimal('500.00'),
            is_available=True,
        )
        
        # Test size display format
        expected_size = "30.00 x 40.00 cm"
        self.assertEqual(artwork_2d.get_size_display(), expected_size)
    
    def test_get_size_display_3d_artwork(self):
        """
        Test get_size_display() method for 3D artworks.
        Should return formatted string: "Width x Height x Depth cm"
        """
        # Test 3D artwork size display format
        expected_size = "50.00 x 70.00 x 3.00 cm"
        self.assertEqual(self.artwork.get_size_display(), expected_size)
    
    def test_get_size_display_no_dimensions(self):
        """
        Test get_size_display() when dimensions are not provided.
        Should return "Size not specified"
        """
        # Create artwork without dimensions
        artwork_no_size = create_artwork_equivalent(
            'No Size Artwork', self.artist,
            medium='Digital',
            price=Decimal('200.00'),
            is_available=True,
        )
        
        self.assertEqual(
            artwork_no_size.get_size_display(),
            "Size not specified",
        )
    
    def test_get_price_display(self):
        """
        Test get_price_display() method formats price correctly.
        Should return formatted string with currency: "USD 1,500.00"
        """
        expected_price = "USD 1,500.00"
        self.assertEqual(self.artwork.get_price_display(), expected_price)
    
    def test_get_price_display_no_price(self):
        """
        Test get_price_display() when price is not set.
        Should return "Price not available"
        """
        # Create artwork without price
        artwork_no_price = create_artwork_equivalent(
            'No Price Artwork', self.artist,
            medium='Sketch',
            is_available=False,
        )
        
        self.assertEqual(
            artwork_no_price.get_price_display(),
            "Price not available",
        )
    
    def test_artwork_medium_field(self):
        """
        Test that medium field accepts various art mediums.
        Verifies the medium field stores different types correctly.
        """
        # Test various medium types
        mediums = [
            'Oil on Canvas',
            'Acrylic',
            'Watercolor',
            'Digital Art',
            'Mixed Media',
            'Photography'
        ]
        
        for medium in mediums:
            artwork = create_artwork_equivalent(
                f'Artwork {medium}', self.artist,
                medium=medium,
                price=Decimal('100.00'),
                is_available=True,
            )
            self.assertEqual(artwork.medium, medium)
    
    def test_artwork_availability(self):
        """
        Test artwork availability flag.
        Ensures is_available field works correctly.
        """
        # Test available artwork
        self.assertTrue(self.artwork.is_available)
        
        # Create unavailable artwork
        unavailable_artwork = create_artwork_equivalent(
            'Unavailable Artwork', self.artist,
            medium='Sculpture',
            price=Decimal('5000.00'),
            is_available=False,
        )
        
        self.assertFalse(unavailable_artwork.is_available)
    
    def test_artwork_featured_flag(self):
        """
        Test artwork featured flag.
        Ensures is_featured field works correctly.
        """
        # Default should be not featured
        self.assertFalse(self.artwork.is_featured)
        
        # Create featured artwork
        featured_artwork = create_artwork_equivalent(
            'Featured Artwork', self.artist,
            medium='Oil Painting',
            price=Decimal('3000.00'),
            is_featured=True,
            is_available=True,
        )
        
        self.assertTrue(featured_artwork.is_featured)


# ============================================================================
# ARTWORK VIEW TESTS
# Tests for artwork views to ensure price, size, and medium are displayed
# ============================================================================

class ArtworkListViewTest(TestCase):
    """
    Test suite for the artwork_list view.
    Ensures artworks are listed with price, size, and medium.
    """
    
    def setUp(self):
        """Set up test data for view tests."""
        # Create test artist (no user field in ArtistProfile)
        self.artist = ArtistProfile.objects.create(
            name='View Test Artist',
            email='viewtest@example.com'
        )
        
        # Create multiple test artworks
        self.artwork1 = create_artwork_equivalent(
            'Artwork 1', self.artist,
            medium='Oil on Canvas',
            width_cm=Decimal('40.00'),
            height_cm=Decimal('60.00'),
            price=Decimal('1000.00'),
            is_available=True,
        )

        self.artwork2 = create_artwork_equivalent(
            'Artwork 2', self.artist,
            medium='Acrylic',
            width_cm=Decimal('50.00'),
            height_cm=Decimal('70.00'),
            price=Decimal('1500.00'),
            is_available=True,
        )

        # Create unavailable artwork (should not appear in list)
        self.artwork3 = create_artwork_equivalent(
            'Unavailable Artwork', self.artist,
            medium='Watercolor',
            price=Decimal('500.00'),
            is_available=False,
        )
        
        self.client = Client()
    
    def test_artwork_list_view_status_code(self):
        """
        Test that the artwork list view returns HTTP 200 OK.
        """
        response = self.client.get(reverse('collections_app:artwork_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_artwork_list_view_template(self):
        """
        Test that the correct template is used for artwork list.
        """
        response = self.client.get(reverse('collections_app:artwork_list'))
        self.assertTemplateUsed(response, 'Vistor_pages/artwork_list.html')
    
    def test_artwork_list_shows_available_artworks(self):
        """
        Test that only available artworks are shown in the list.
        Verifies filtering by is_available=True.
        """
        response = self.client.get(reverse('collections_app:artwork_list'))
        artworks = response.context['artworks']
        
        # Should contain 2 available artworks
        self.assertEqual(artworks.count(), 2)
        self.assertIn(self.artwork1, artworks)
        self.assertIn(self.artwork2, artworks)
        # Should NOT contain unavailable artwork
        self.assertNotIn(self.artwork3, artworks)
    
    def test_artwork_list_contains_price_data(self):
        """
        Test that artwork list context contains price information.
        Ensures price data is available for template rendering.
        """
        response = self.client.get(reverse('collections_app:artwork_list'))
        artworks = response.context['artworks']
        
        for artwork in artworks:
            # Each artwork should have a price
            self.assertIsNotNone(artwork.price)
            # Should be able to call get_price_display()
            self.assertIsNotNone(artwork.get_price_display())
    
    def test_artwork_list_contains_size_data(self):
        """
        Test that artwork list context contains size information.
        Ensures size data is available for template rendering.
        """
        response = self.client.get(reverse('collections_app:artwork_list'))
        artworks = response.context['artworks']
        
        for artwork in artworks:
            # Should be able to call get_size_display()
            size_display = artwork.get_size_display()
            self.assertIsNotNone(size_display)
    
    def test_artwork_list_contains_medium_data(self):
        """
        Test that artwork list context contains medium information.
        Ensures medium data is available for template rendering.
        """
        response = self.client.get(reverse('collections_app:artwork_list'))
        artworks = response.context['artworks']
        
        for artwork in artworks:
            # Each artwork should have medium info
            self.assertIsNotNone(artwork.medium)
    
    def test_artwork_list_search_functionality(self):
        """
        Test search functionality filters artworks correctly.
        Verifies search by title, medium, or artist works.
        """
        # Search by title
        response = self.client.get(
            reverse('collections_app:artwork_list'),
            {'search': 'Artwork 1'}
        )
        artworks = response.context['artworks']
        self.assertEqual(artworks.count(), 1)
        self.assertIn(self.artwork1, artworks)
        
        # Search by medium
        response = self.client.get(
            reverse('collections_app:artwork_list'),
            {'search': 'Acrylic'}
        )
        artworks = response.context['artworks']
        self.assertEqual(artworks.count(), 1)
        self.assertIn(self.artwork2, artworks)
    
    def test_artwork_list_price_filter(self):
        """
        Test price range filtering works correctly.
        Verifies min_price and max_price filters.
        """
        # Filter by minimum price
        response = self.client.get(
            reverse('collections_app:artwork_list'),
            {'min_price': '1200'}
        )
        artworks = response.context['artworks']
        self.assertEqual(artworks.count(), 1)
        self.assertIn(self.artwork2, artworks)
        
        # Filter by maximum price
        response = self.client.get(
            reverse('collections_app:artwork_list'),
            {'max_price': '1200'}
        )
        artworks = response.context['artworks']
        self.assertEqual(artworks.count(), 1)
        self.assertIn(self.artwork1, artworks)


class ArtworkDetailViewTest(TestCase):
    """
    Test suite for the artwork_detail view.
    Ensures individual artwork displays price, size, and medium correctly.
    """
    
    def setUp(self):
        """Set up test data for detail view tests."""
        self.artist = ArtistProfile.objects.create(
            name='Detail Test Artist',
            email='detailtest@example.com'
        )
        
        self.artwork = create_artwork_equivalent(
            'Detail Test Artwork', self.artist,
            medium='Mixed Media',
            width_cm=Decimal('100.00'),
            height_cm=Decimal('150.00'),
            depth_cm=Decimal('5.00'),
            price=Decimal('2500.00'),
            currency='USD',
            description='Detailed artwork description',
            year_created=2024,
            is_available=True,
        )
        
        self.client = Client()
    
    def test_artwork_detail_view_status_code(self):
        """
        Test that the artwork detail view returns HTTP 200 OK.
        """
        response = self.client.get(
            reverse('collections_app:artwork_detail', args=[self.artwork.pk])
        )
        self.assertEqual(response.status_code, 200)
    
    def test_artwork_detail_view_template(self):
        """
        Test that the correct template is used for artwork detail.
        """
        response = self.client.get(
            reverse('collections_app:artwork_detail', args=[self.artwork.pk])
        )
        self.assertTemplateUsed(response, 'Vistor_pages/artwork_detail.html')
    
    def test_artwork_detail_shows_price(self):
        """
        Test that artwork detail page displays price correctly.
        Verifies price_display is in context and formatted properly.
        """
        response = self.client.get(
            reverse('collections_app:artwork_detail', args=[self.artwork.pk])
        )
        
        # Check artwork is in context
        self.assertEqual(response.context['artwork'], self.artwork)
        
        # Check price_display is in context
        self.assertIn('price_display', response.context)
        self.assertEqual(response.context['price_display'], 'USD 2,500.00')
        
        # Check price appears in response content
        self.assertContains(response, '2,500.00')
    
    def test_artwork_detail_shows_size(self):
        """
        Test that artwork detail page displays size correctly.
        Verifies size_display is in context and formatted properly.
        """
        response = self.client.get(
            reverse('collections_app:artwork_detail', args=[self.artwork.pk])
        )
        
        # Check size_display is in context
        self.assertIn('size_display', response.context)
        self.assertEqual(
            response.context['size_display'],
            '100.00 x 150.00 x 5.00 cm'
        )
        
        # Check size appears in response content
        self.assertContains(response, '100.00')
        self.assertContains(response, '150.00')
    
    def test_artwork_detail_shows_medium(self):
        """
        Test that artwork detail page displays medium correctly.
        Verifies medium field is accessible and displayed.
        """
        response = self.client.get(
            reverse('collections_app:artwork_detail', args=[self.artwork.pk])
        )
        
        # Check medium is accessible
        self.assertEqual(response.context['artwork'].medium, 'Mixed Media')
        
        # Check medium appears in response content
        self.assertContains(response, 'Mixed Media')
    
    def test_artwork_detail_not_found(self):
        """
        Test that accessing non-existent artwork returns 404.
        """
        response = self.client.get(
            reverse('collections_app:artwork_detail', args=[99999])
        )
        self.assertEqual(response.status_code, 404)


class FeaturedArtworksViewTest(TestCase):
    """
    Test suite for the featured_artworks view.
    Ensures featured artworks display with price, size, and medium.
    """
    
    def setUp(self):
        """Set up test data for featured artworks tests."""
        self.artist = ArtistProfile.objects.create(
            name='Featured Artist',
            email='featured@example.com'
        )
        
        # Create featured artwork
        self.featured_artwork = create_artwork_equivalent(
            'Featured Artwork', self.artist,
            medium='Oil Painting',
            width_cm=Decimal('80.00'),
            height_cm=Decimal('100.00'),
            price=Decimal('5000.00'),
            is_available=True,
            is_featured=True,
        )

        # Create non-featured artwork
        self.regular_artwork = create_artwork_equivalent(
            'Regular Artwork', self.artist,
            medium='Watercolor',
            price=Decimal('500.00'),
            is_available=True,
            is_featured=False,
        )
        
        self.client = Client()
    
    def test_featured_artworks_view_status_code(self):
        """
        Test that the featured artworks view returns HTTP 200 OK.
        """
        response = self.client.get(reverse('collections_app:featured_artworks'))
        self.assertEqual(response.status_code, 200)
    
    def test_featured_artworks_only_shows_featured(self):
        """
        Test that only featured artworks are displayed.
        Verifies filtering by is_featured=True.
        """
        response = self.client.get(reverse('collections_app:featured_artworks'))
        artworks = response.context['featured_artworks']
        
        # Should only contain featured artwork
        self.assertEqual(artworks.count(), 1)
        self.assertIn(self.featured_artwork, artworks)
        self.assertNotIn(self.regular_artwork, artworks)
    
    def test_featured_artworks_display_price_size_medium(self):
        """
        Test that featured artworks show price, size, and medium.
        Ensures all required buyer information is available.
        """
        response = self.client.get(reverse('collections_app:featured_artworks'))
        artworks = response.context['featured_artworks']
        
        for artwork in artworks:
            # Test price is available
            self.assertIsNotNone(artwork.price)
            self.assertIsNotNone(artwork.get_price_display())
            
            # Test size is available
            self.assertIsNotNone(artwork.get_size_display())
            
            # Test medium is available
            self.assertIsNotNone(artwork.medium)


# ============================================================================
# EXISTING TESTS (kept for compatibility)
# ============================================================================

class CollectionsAppSmokeTest(TestCase):
    def test_imports(self):
        from . import models
        self.assertIsNotNone(models)
