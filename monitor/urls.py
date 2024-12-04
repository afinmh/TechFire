from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('status', views.get_status, name='get_status'),
    path('update_status', views.update_status, name='update_status'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
