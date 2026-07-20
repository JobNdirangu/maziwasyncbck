from django.urls import path
from collector import views

urlpatterns = [
    path('dashboard/' ,views.PorterDashboard),
    path('milk-collections/add', views.AddMilkCollection),
    path('collections/my', views.MyCollections.as_view()),
    path('notice/', views.PorterNoticeView.as_view() )


]
