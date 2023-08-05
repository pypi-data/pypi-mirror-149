from django.apps import AppConfig


class UserCrudlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_crudl'

    def ready(self):
        from .urls import urlpatterns
        from ..utils.app_config import update_urlpatterns

        update_urlpatterns(urlpatterns, "temba.urls")
