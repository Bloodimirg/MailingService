from django.core.cache import cache

from boat.models import Blog
from config.settings import CACHE_ENABLED


def get_posts_from_cache():
    """Получает данные по постам из кэша, если кэш пуст, получает данные из БД"""
    if not CACHE_ENABLED:
        return Blog.objects.all()
    key = "blog_list"

    blogs = cache.get(key)

    if blogs is not None:
        return blogs
    blogs = Blog.objects.all()
    cache.set(key, blogs)
    return blogs
