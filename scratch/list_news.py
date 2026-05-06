import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dss_consultancy.settings')
django.setup()

from core.models import NewsPost

news_posts = NewsPost.objects.filter(status='published')
for n in news_posts:
    print(f"SLUG: {n.slug}")
