from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from cooperative import views

router= DefaultRouter()
router.register('farmers', views.FarmerViewSet, basename='farmers' )
router.register('porters', views.PorterViewSet, basename='porters' )
router.register('notice', views.NoticeViewSet, basename='notice')
router.register('collection', views.MilkCollectionViewSet, basename='collection')


urlpatterns=[
    path('dashboard/', views.AdminDashboardView.as_view()),
    path('farmer/balance/', views.FarmersWithBal),
    path('payfarmer/', views.PayFarmer),
    path('callback', views.MpesaCallback),
    path('', include(router.urls))
]