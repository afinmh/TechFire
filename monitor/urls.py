from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('gambar', views.gambar, name='gambar'),
    path('status', views.get_status, name='get_status'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('api/login/', views.api_login, name='api_login'),
    path("update_status/", views.update_status, name="update_status"),
    path('api/sensor-data/', views.sensor_data_api, name='sensor_data_api'),
    path('api/fire-images/', views.fire_image_api, name='fire_image_api'),
    path('api/upload-fire-image/', views.fire_image_upload, name='fire_image_upload'),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)