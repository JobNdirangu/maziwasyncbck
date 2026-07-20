from django.urls import path, include
from farmer import views
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register('feedback', views.FeedbackViewset, basename='feedback')
urlpatterns=[
    path('dashboard/', views.FarmerDashboard.as_view()),
    path('collections/', views.FarmerCollection.as_view()),
    path('notice/', views.FarmerNoticeView.as_view()),
    path('predict/', views.PredictDisease),

    

    path('', include(router.urls))
]