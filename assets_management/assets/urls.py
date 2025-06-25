from django.urls import path, include
from rest_framework.routers import  DefaultRouter
from .views import AssetsView, ViolationView, NotificationView, run_chk

router = DefaultRouter()

router.register(r'assts', AssetsView, basename='assets')
router.register(r'notification', NotificationView, basename='notification')
router.register(r'violation', ViolationView, basename='violation')

urlpatterns=[
    path('', include(router.urls)),
    path('run_chk/', run_chk, name='run_chk' ),

]