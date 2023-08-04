from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage, name="homepage" ),
    path('dashboard/',views.dashboard, name="dashboard" ),
    path('logout/',views.logout_view, name="logout" ),
    path('register/',views.register, name="register" ),
    path('about/',views.aboutview, name="about_page" ),
    path('profile/', views.profile_view, name="profile"),
]