from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from api.urls import router as api_router
from rest_framework import routers
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.registry.extend(api_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)