import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dss_consultancy.settings')
django.setup()

from core.models import NewsPost

news = NewsPost.objects.filter(status='published').first()
if news:
    print(f"SLUG: {news.slug}")
else:
    print("NO_PUBLISHED_NEWS")
