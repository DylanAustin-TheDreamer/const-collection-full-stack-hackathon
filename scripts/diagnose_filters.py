import os
import sys
sys.path.append(r"C:\Users\Ryan_\Desktop\vscode-projects\const-collection-full-stack-hackathon")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.test import Client
from collections_app.models import Collection, ArtVariant, Art
from django.db.models import Q

print('Collections count:', Collection.objects.count())
print('Sample collections:', list(Collection.objects.values('pk','name')[:10]))
print('Art count:', Art.objects.count())
format_choices = ArtVariant.MEDIUM_CHOICES
print('Format choices:', format_choices)

# Featured
featured_qs = Art.objects.filter(is_featured=True).filter(Q(is_available=True) | Q(variants__is_available=True)).distinct()
print('Featured count (per view criteria):', featured_qs.count())
for a in featured_qs[:5]:
    print(' -', a.pk, a.title, 'is_available=', a.is_available, 'variants_available=', a.variants.filter(is_available=True).count())

# Use test client to render the artwork list page
c = Client()
r = c.get('/artworks/')
print('GET /artworks/ status:', r.status_code)
content = r.content.decode('utf-8', errors='replace')
print('Contains "Featured"?:', 'Featured' in content)
print('Contains "select id=\"collection\""?:', 'id="collection"' in content)
print('\n--- HTML SNIPPET ---\n')
print(content[:2000])
