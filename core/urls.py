from django.urls import path
from core import views

urlpatterns = [
    path('auth/register/', views.Register),
    path('auth/login/', views.Login),
    path('auth/me/', views.MyProfile),
    path('auth/logout/', views.Logout),

]
