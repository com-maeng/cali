from django.apps import AppConfig


class RedisearchAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search_preview.redisearch_app'
