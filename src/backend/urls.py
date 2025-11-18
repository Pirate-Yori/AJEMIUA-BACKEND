from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from api.urls import router as api_router
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers,permissions
from django.conf.urls.static import static

from django.urls import include, path

schema_view = get_schema_view(
   openapi.Info(
      title="AJEMIUA-BACKEND-API",
      default_version='v1',
      description="This API is use to manage the backend of the AJEMIUA-PROJECT",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="jimmybreak44@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True, #Bro fo t'authentifier
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.registry.extend(api_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
    path("", include("accounts.urls", namespace="users")),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)