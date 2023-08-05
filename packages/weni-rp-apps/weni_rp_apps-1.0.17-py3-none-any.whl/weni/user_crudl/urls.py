from .views import UserCRUDL

urlpatterns = UserCRUDL().as_urlpatterns()
print(urlpatterns)